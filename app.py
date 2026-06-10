"""
Confessionário Anônimo de Problemas - Backend Refatorizado
============================================================
Sistema completo de relatos anônimos com suporte a categorias,
busca de semelhantes, respostas e persistência de dados.

Execução:
    python app.py

Acesso:
    http://localhost:8000
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, asdict, field
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Any
from urllib.parse import urlparse

HOST = "localhost"
PORT = 8000
BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "dados.json"


@dataclass
class Resposta:
    """Representa uma resposta anônima a um relato."""
    
    id: str
    relato_id: str
    texto: str
    data: str


@dataclass
class Relato:
    """Representa um relato anônimo enviado por uma pessoa."""
    
    id: str
    texto: str
    categoria: str
    data: str
    respostas: List[Dict[str, Any]] = field(default_factory=list)


class ConfessionarioApp:
    """Gerencia relatos anônimos, classificação, busca, respostas e persistência."""

    def __init__(self) -> None:
        self.relatos: List[Relato] = []
        self.palavras_chave: Dict[str, tuple] = {
            "Ansiedade": (
                "ansiedade", "medo", "pânico", "crise", "preocupação",
                "futuro", "insegurança", "nervoso", "cansado", "estresse"
            ),
            "Família": (
                "família", "pai", "mãe", "irmão", "irmã", "casa",
                "briga", "parentes", "casamento", "conflito", "herança"
            ),
            "Estudos": (
                "estudo", "escola", "faculdade", "prova", "nota",
                "trabalho", "professor", "curso", "aprendizado", "fracasso"
            ),
            "Amizades": (
                "amigo", "amiga", "amizade", "sozinho", "rejeitado",
                "grupo", "confiança", "perdoar", "traição", "isolamento"
            ),
            "Fé": (
                "fé", "deus", "oração", "orar", "rezar", "igreja",
                "pecado", "perdão", "espiritual", "religião", "culpa"
            ),
            "Relacionamento": (
                "amor", "namorado", "namorada", "cônjuge", "paixão",
                "coração", "beijo", "casamento", "divórcio", "ciúmes"
            ),
            "Saúde": (
                "doença", "doente", "hospital", "médico", "medicamento",
                "saúde", "cura", "diagnóstico", "sintoma", "tratamento"
            ),
            "Carreira": (
                "emprego", "trabalho", "demissão", "promoção", "salário",
                "chefe", "colega", "profissão", "desemprego", "entrevista"
            ),
        }
        self._carregar_dados()

    def adicionar_relato(self, texto: str) -> Dict[str, Any]:
        """Remove dados pessoais, classifica, armazena e persiste um novo relato."""
        texto_limpo = self._anonimizar_texto(texto)
        categoria = self._classificar_relato(texto_limpo)
        
        relato = Relato(
            id=str(uuid.uuid4()),
            texto=texto_limpo,
            categoria=categoria,
            data=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
        self.relatos.append(relato)
        self._salvar_dados()

        semelhantes = self.buscar_semelhantes(texto_limpo, categoria)
        estatisticas = self.gerar_estatisticas()

        return {
            "relato": asdict(relato),
            "semelhantes": len(semelhantes),
            "categoria": categoria,
            "mensagem": "Você não está sozinho.",
            "estatisticas": estatisticas,
        }

    def adicionar_resposta(self, relato_id: str, texto: str) -> Dict[str, Any]:
        """Adiciona uma resposta anônima a um relato específico."""
        relato = next((r for r in self.relatos if r.id == relato_id), None)
        if not relato:
            return {"erro": "Relato não encontrado."}

        texto_limpo = self._anonimizar_texto(texto)
        resposta = Resposta(
            id=str(uuid.uuid4()),
            relato_id=relato_id,
            texto=texto_limpo,
            data=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
        
        relato.respostas.append(asdict(resposta))
        self._salvar_dados()

        return {
            "resposta": asdict(resposta),
            "mensagem": "Sua resposta foi publicada.",
        }

    def buscar_semelhantes(self, texto: str, categoria: str | None = None) -> List[Relato]:
        """Encontra relatos parecidos por categoria e palavras em comum."""
        texto_normalizado = self._normalizar(texto)
        termos = set(texto_normalizado.split())
        resultados: List[Relato] = []

        for relato in self.relatos:
            relato_termos = set(self._normalizar(relato.texto).split())
            intersecao = termos.intersection(relato_termos)
            mesma_categoria = categoria is not None and relato.categoria == categoria

            if mesma_categoria or len(intersecao) >= 2:
                resultados.append(relato)

        return resultados[:10]

    def gerar_estatisticas(self) -> Dict[str, Any]:
        """Gera percentuais por categoria e números gerais da comunidade."""
        total = len(self.relatos)
        categorias = {cat: 0 for cat in self.palavras_chave.keys()}
        categorias["Outros"] = 0

        for relato in self.relatos:
            categorias[relato.categoria] = categorias.get(relato.categoria, 0) + 1

        percentuais = {
            cat: round((qtd / total) * 100) if total else 0
            for cat, qtd in categorias.items()
        }

        return {
            "total_relatos": total,
            "categorias": categorias,
            "percentuais": percentuais,
        }

    def listar_relatos(self, categoria: str | None = None) -> List[Dict[str, Any]]:
        """Retorna relatos em formato seguro, opcionalmente filtrados por categoria."""
        relatos = self.relatos
        if categoria and categoria in self.palavras_chave:
            relatos = [r for r in relatos if r.categoria == categoria]
        
        return [asdict(r) for r in reversed(relatos)]

    def obter_relato(self, relato_id: str) -> Dict[str, Any] | None:
        """Obtém um relato específico com todas suas respostas."""
        relato = next((r for r in self.relatos if r.id == relato_id), None)
        return asdict(relato) if relato else None

    def obter_categorias(self) -> Dict[str, str]:
        """Retorna lista de categorias disponíveis."""
        return {cat: f"{len([r for r in self.relatos if r.categoria == cat])} relatos" 
                for cat in self.palavras_chave.keys()}

    def _carregar_dados(self) -> None:
        """Carrega dados persistidos ou cria dados de exemplo."""
        if DATA_FILE.exists():
            try:
                dados = json.loads(DATA_FILE.read_text(encoding="utf-8"))
                for item in dados:
                    self.relatos.append(Relato(
                        id=item["id"],
                        texto=item["texto"],
                        categoria=item["categoria"],
                        data=item["data"],
                        respostas=item.get("respostas", []),
                    ))
            except (json.JSONDecodeError, KeyError):
                self._criar_exemplos()
        else:
            self._criar_exemplos()

    def _salvar_dados(self) -> None:
        """Persiste dados em JSON."""
        dados = [asdict(r) for r in self.relatos]
        DATA_FILE.write_text(json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8")

    def _criar_exemplos(self) -> None:
        """Popula com relatos de exemplo para demonstração."""
        exemplos = [
            ("Tenho medo do futuro e sinto muita ansiedade.", "Ansiedade"),
            ("Não consigo perdoar alguém da minha família.", "Família"),
            ("Estou cansado de fingir que estou bem.", "Ansiedade"),
            ("Tenho dificuldade de rezar todos os dias.", "Fé"),
            ("Sinto que não sou bom o suficiente nos estudos.", "Estudos"),
            ("Tenho medo de decepcionar meus pais.", "Família"),
            ("Perdi a confiança em uma amizade importante.", "Amizades"),
            ("Minha rotina de oração está muito fraca.", "Fé"),
            ("A escola me deixa inseguro e pressionado.", "Estudos"),
            ("Tenho vergonha de falar sobre meus problemas.", "Ansiedade"),
        ]

        for texto, _ in exemplos:
            self.relatos.append(Relato(
                id=str(uuid.uuid4()),
                texto=self._anonimizar_texto(texto),
                categoria=self._classificar_relato(texto),
                data=datetime.utcnow().isoformat(timespec="seconds") + "Z",
            ))
        
        self._salvar_dados()

    def _classificar_relato(self, texto: str) -> str:
        """Classifica relato baseado em palavras-chave simples e auditáveis."""
        texto_normalizado = self._normalizar(texto)
        pontuacao: Dict[str, int] = {}

        for categoria, palavras in self.palavras_chave.items():
            pontuacao[categoria] = sum(1 for p in palavras if p in texto_normalizado)

        categoria, pontos = max(pontuacao.items(), key=lambda x: x[1])
        return categoria if pontos > 0 else "Outros"

    def _anonimizar_texto(self, texto: str) -> str:
        """Remove padrões de e-mail, telefone e nomes diretos."""
        texto = texto.strip()
        texto = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[email removido]", texto)
        texto = re.sub(r"(?:\+?\d{1,3}\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}[-\s]?\d{4}", "[telefone removido]", texto)
        texto = re.sub(r"\b(meu nome é|me chamo|sou o|sou a|meu|minha)\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÀ-ÿ-]+", r"\1 [nome removido]", texto, flags=re.IGNORECASE)
        return texto[:1500]

    def _normalizar(self, texto: str) -> str:
        """Prepara texto para classificação e comparação."""
        texto = texto.lower()
        texto = re.sub(r"[^a-zà-ÿ0-9\s]", " ", texto)
        return re.sub(r"\s+", " ", texto).strip()


# Instância global
app = ConfessionarioApp()


class ServidorHandler(BaseHTTPRequestHandler):
    """Handler HTTP para API REST e entrega do frontend."""

    def _adicionar_headers_cors(self) -> None:
        """Adiciona headers CORS e segurança a todas as respostas."""
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS, DELETE")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")

    def do_OPTIONS(self) -> None:  # noqa: N802
        """Responde requisições OPTIONS para CORS."""
        self.send_response(204)
        self._adicionar_headers_cors()
        self.end_headers()

    def do_GET(self) -> None:  # noqa: N802
        """Trata requisições GET: arquivos estáticos e endpoints da API."""
        caminho = urlparse(self.path).path
        query = urlparse(self.path).query

        if caminho in ("/", "/index.html"):
            self._enviar_arquivo(BASE_DIR / "index.html", "text/html; charset=utf-8")
        elif caminho == "/api/relatos":
            categoria = self._extrair_parametro(query, "categoria")
            relatos = app.listar_relatos(categoria)
            self._enviar_json({"relatos": relatos})
        elif caminho.startswith("/api/relatos/"):
            relato_id = caminho.replace("/api/relatos/", "")
            relato = app.obter_relato(relato_id)
            if relato:
                self._enviar_json(relato)
            else:
                self._enviar_json({"erro": "Relato não encontrado."}, 404)
        elif caminho == "/api/estatisticas":
            self._enviar_json(app.gerar_estatisticas())
        elif caminho == "/api/categorias":
            self._enviar_json({"categorias": app.obter_categorias()})
        else:
            self._enviar_json({"erro": "Rota não encontrada."}, 404)

    def do_POST(self) -> None:  # noqa: N802
        """Trata requisições POST: criar relatos e respostas."""
        caminho = urlparse(self.path).path

        if not self._validar_content_length():
            return

        corpo = self._ler_corpo()
        if corpo is None:
            return

        try:
            dados = json.loads(corpo)
        except json.JSONDecodeError:
            self._enviar_json({"erro": "JSON inválido."}, 400)
            return

        if caminho == "/api/relatos":
            self._criar_relato(dados)
        elif caminho.startswith("/api/relatos/") and caminho.endswith("/respostas"):
            relato_id = caminho.replace("/api/relatos/", "").replace("/respostas", "")
            self._criar_resposta(relato_id, dados)
        else:
            self._enviar_json({"erro": "Rota não encontrada."}, 404)

    def _criar_relato(self, dados: Dict[str, Any]) -> None:
        """Cria um novo relato."""
        texto = str(dados.get("texto", "")).strip()
        
        if len(texto) < 8:
            self._enviar_json({"erro": "Escreva um relato com pelo menos 8 caracteres."}, 400)
            return
        
        if len(texto) > 1500:
            self._enviar_json({"erro": "Relato muito longo (máximo 1500 caracteres)."}, 400)
            return

        resposta = app.adicionar_relato(texto)
        self._enviar_json(resposta, 201)

    def _criar_resposta(self, relato_id: str, dados: Dict[str, Any]) -> None:
        """Cria uma nova resposta para um relato."""
        texto = str(dados.get("texto", "")).strip()
        
        if len(texto) < 5:
            self._enviar_json({"erro": "Escreva uma resposta com pelo menos 5 caracteres."}, 400)
            return
        
        if len(texto) > 1000:
            self._enviar_json({"erro": "Resposta muito longa (máximo 1000 caracteres)."}, 400)
            return

        resposta = app.adicionar_resposta(relato_id, texto)
        
        if "erro" in resposta:
            self._enviar_json(resposta, 404)
        else:
            self._enviar_json(resposta, 201)

    def _enviar_arquivo(self, caminho: Path, content_type: str) -> None:
        """Envia um arquivo estático com cabeçalhos seguros."""
        if not caminho.exists():
            self._enviar_json({"erro": "Arquivo não encontrado."}, 404)
            return

        conteudo = caminho.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(conteudo)))
        self._adicionar_headers_cors()
        self.end_headers()
        self.wfile.write(conteudo)

    def _enviar_json(self, dados: Dict[str, Any] | List, status: int = 200) -> None:
        """Serializa e envia respostas JSON."""
        conteudo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self._adicionar_headers_cors()
        self.end_headers()
        self.wfile.write(conteudo)

    def _validar_content_length(self) -> bool:
        """Valida Content-Length antes de ler o corpo."""
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            if tamanho > 5_000_000:  # 5 MB máximo
                self._enviar_json({"erro": "Corpo muito grande."}, 413)
                return False
            return True
        except (ValueError, TypeError):
            self._enviar_json({"erro": "Content-Length inválido."}, 400)
            return False

    def _ler_corpo(self) -> str | None:
        """Lê o corpo da requisição de forma segura."""
        try:
            tamanho = int(self.headers.get("Content-Length", 0))
            corpo = self.rfile.read(tamanho).decode("utf-8")
            return corpo if corpo else "{}"
        except Exception:
            self._enviar_json({"erro": "Erro ao ler corpo."}, 400)
            return None

    @staticmethod
    def _extrair_parametro(query: str, nome: str) -> str | None:
        """Extrai parâmetro de query string."""
        for parte in query.split("&"):
            if "=" in parte:
                chave, valor = parte.split("=", 1)
                if chave == nome:
                    return valor
        return None

    def log_message(self, formato: str, *args: Any) -> None:
        """Logs do servidor em português."""
        print(f"[{datetime.now().strftime('%H:%M:%S')}] {formato % args}")


def iniciar_servidor() -> None:
    """Inicia o servidor HTTP com suporte a múltiplas requisições."""
    servidor = ThreadingHTTPServer((HOST, PORT), ServidorHandler)
    print("=" * 60)
    print("🔐 Confessionário Anônimo de Problemas")
    print("=" * 60)
    print(f"✅ Servidor iniciado com sucesso!")
    print(f"🌐 Acesse: http://{HOST}:{PORT}")
    print(f"📁 Dados salvos em: {DATA_FILE}")
    print("=" * 60)
    print("Pressione Ctrl+C para parar o servidor.")
    print("=" * 60)
    
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  Servidor interrompido.")


if __name__ == "__main__":
    iniciar_servidor()
