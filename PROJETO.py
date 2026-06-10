"""
Confessionário Anônimo de Problemas
-----------------------------------
Backend didático em Python puro para receber relatos anônimos, classificar
conteúdos, encontrar relatos semelhantes e gerar estatísticas emocionais.

Execute com:
    python PROJETO.py

Depois acesse:
    http://localhost:8000
"""

from __future__ import annotations

import json
import re
import uuid
from dataclasses import dataclass, asdict
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Dict, List, Tuple, Any
from urllib.parse import urlparse

HOST = "localhost"
PORTA = 8000
BASE_DIR = Path(__file__).resolve().parent


@dataclass
class Relato:
    """Representa um relato anônimo enviado por uma pessoa."""

    id: str
    texto: str
    categoria: str
    data: str


class Confessionario:
    """Gerencia relatos anônimos, classificação, busca e estatísticas."""

    def __init__(self) -> None:
        self.relatos: List[Relato] = []
        self.palavras_chave: Dict[str, Tuple[str, ...]] = {
            "Ansiedade": (
                "ansiedade",
                "medo",
                "pânico",
                "crise",
                "preocupação",
                "futuro",
                "insegurança",
                "nervoso",
                "cansado",
            ),
            "Família": (
                "família",
                "pai",
                "mãe",
                "irmão",
                "irmã",
                "casa",
                "briga",
                "parentes",
                "casamento",
            ),
            "Estudos": (
                "estudo",
                "escola",
                "faculdade",
                "prova",
                "nota",
                "trabalho",
                "professor",
                "curso",
            ),
            "Amizades": (
                "amigo",
                "amiga",
                "amizade",
                "sozinho",
                "rejeitado",
                "grupo",
                "confiança",
                "perdoar",
            ),
            "Fé": (
                "fé",
                "deus",
                "oração",
                "orar",
                "rezar",
                "igreja",
                "pecado",
                "perdão",
                "espiritual",
            ),
        }
        self._carregar_relatos_iniciais()

    def adicionar_relato(self, texto: str) -> Dict[str, Any]:
        """Remove dados pessoais simples, classifica e armazena um novo relato."""
        texto_limpo = self._anonimizar_texto(texto)
        categoria = self._classificar_relato(texto_limpo)
        relato = Relato(
            id=str(uuid.uuid4()),
            texto=texto_limpo,
            categoria=categoria,
            data=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        )
        self.relatos.append(relato)

        semelhantes = self.buscar_semelhantes(texto_limpo, categoria)
        estatisticas = self.gerar_estatisticas()

        return {
            "relato": asdict(relato),
            "semelhantes": len(semelhantes),
            "categoria": categoria,
            "mensagem": "Você não está sozinho.",
            "estatisticas": estatisticas,
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

        return resultados

    def gerar_estatisticas(self) -> Dict[str, Any]:
        """Gera percentuais por categoria e números gerais da comunidade."""
        total = len(self.relatos)
        categorias = {categoria: 0 for categoria in (*self.palavras_chave.keys(), "Outros")}

        for relato in self.relatos:
            categorias[relato.categoria] = categorias.get(relato.categoria, 0) + 1

        percentuais = {
            categoria: round((quantidade / total) * 100) if total else 0
            for categoria, quantidade in categorias.items()
        }

        return {
            "total_relatos": total,
            "categorias": categorias,
            "percentuais": percentuais,
        }

    def listar_relatos(self) -> List[Dict[str, Any]]:
        """Retorna os relatos em formato seguro para a interface."""
        return [asdict(relato) for relato in reversed(self.relatos)]

    def _carregar_relatos_iniciais(self) -> None:
        """Popula o MVP com relatos fictícios para demonstrar agrupamentos."""
        exemplos = [
            "Tenho medo do futuro e sinto muita ansiedade.",
            "Não consigo perdoar alguém da minha família.",
            "Estou cansado de fingir que estou bem.",
            "Tenho dificuldade de rezar todos os dias.",
            "Sinto que não sou bom o suficiente nos estudos.",
            "Tenho medo de decepcionar meus pais.",
            "Perdi a confiança em uma amizade importante.",
            "Minha rotina de oração está muito fraca.",
            "A escola me deixa inseguro e pressionado.",
            "Tenho vergonha de falar sobre meus problemas.",
        ]

        for exemplo in exemplos:
            categoria = self._classificar_relato(exemplo)
            self.relatos.append(
                Relato(
                    id=str(uuid.uuid4()),
                    texto=self._anonimizar_texto(exemplo),
                    categoria=categoria,
                    data=datetime.utcnow().isoformat(timespec="seconds") + "Z",
                )
            )

    def _classificar_relato(self, texto: str) -> str:
        """Classifica o relato com base em palavras-chave simples e auditáveis."""
        texto_normalizado = self._normalizar(texto)
        pontuacao: Dict[str, int] = {}

        for categoria, palavras in self.palavras_chave.items():
            pontuacao[categoria] = sum(1 for palavra in palavras if palavra in texto_normalizado)

        categoria, pontos = max(pontuacao.items(), key=lambda item: item[1])
        return categoria if pontos > 0 else "Outros"

    def _anonimizar_texto(self, texto: str) -> str:
        """Remove padrões comuns de e-mail, telefone e menções diretas de nomes."""
        texto = texto.strip()
        texto = re.sub(r"[\w\.-]+@[\w\.-]+\.\w+", "[email removido]", texto)
        texto = re.sub(r"(?:\+?\d{1,3}\s?)?(?:\(?\d{2}\)?\s?)?\d{4,5}[-\s]?\d{4}", "[telefone removido]", texto)
        texto = re.sub(r"\b(meu nome é|me chamo|sou o|sou a)\s+[A-ZÁÉÍÓÚÂÊÔÃÕÇ][\wÀ-ÿ-]+", r"\1 [nome removido]", texto, flags=re.IGNORECASE)
        return texto[:1200]

    def _normalizar(self, texto: str) -> str:
        """Prepara texto para classificação e comparação simples."""
        texto = texto.lower()
        texto = re.sub(r"[^a-zà-ÿ0-9\s]", " ", texto)
        return re.sub(r"\s+", " ", texto).strip()


confessionario = Confessionario()


class ServidorConfessionario(BaseHTTPRequestHandler):
    """Servidor HTTP minimalista para API e entrega do frontend."""

    def do_GET(self) -> None:  # noqa: N802 - assinatura exigida por BaseHTTPRequestHandler
        rota = urlparse(self.path).path

        if rota in ("/", "/index.html"):
            self._enviar_arquivo(BASE_DIR / "index.html", "text/html; charset=utf-8")
        elif rota == "/api/relatos":
            self._enviar_json({"relatos": confessionario.listar_relatos()})
        elif rota == "/api/estatisticas":
            self._enviar_json(confessionario.gerar_estatisticas())
        else:
            self._enviar_json({"erro": "Rota não encontrada."}, status=404)

    def do_POST(self) -> None:  # noqa: N802 - assinatura exigida por BaseHTTPRequestHandler
        rota = urlparse(self.path).path

        if rota != "/api/relatos":
            self._enviar_json({"erro": "Rota não encontrada."}, status=404)
            return

        tamanho = int(self.headers.get("Content-Length", 0))
        corpo = self.rfile.read(tamanho).decode("utf-8")

        try:
            dados = json.loads(corpo or "{}")
        except json.JSONDecodeError:
            self._enviar_json({"erro": "JSON inválido."}, status=400)
            return

        texto = str(dados.get("texto", "")).strip()
        if len(texto) < 8:
            self._enviar_json({"erro": "Escreva um relato com pelo menos 8 caracteres."}, status=400)
            return

        resposta = confessionario.adicionar_relato(texto)
        self._enviar_json(resposta, status=201)

    def _enviar_arquivo(self, caminho: Path, content_type: str) -> None:
        """Envia um arquivo estático com cabeçalhos seguros para o MVP."""
        if not caminho.exists():
            self._enviar_json({"erro": "Arquivo não encontrado."}, status=404)
            return

        conteudo = caminho.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(conteudo)

    def _enviar_json(self, dados: Dict[str, Any], status: int = 200) -> None:
        """Serializa respostas JSON e habilita CORS para testes locais."""
        conteudo = json.dumps(dados, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(conteudo)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(conteudo)

    def log_message(self, formato: str, *args: Any) -> None:
        """Mantém logs do servidor claros e em português."""
        print(f"[Confessionário] {self.address_string()} - {formato % args}")


def iniciar_servidor() -> None:
    """Inicia o servidor local com suporte a múltiplas requisições."""
    servidor = ThreadingHTTPServer((HOST, PORTA), ServidorConfessionario)
    print("Confessionário Anônimo de Problemas iniciado com sucesso.")
    print(f"Acesse: http://{HOST}:{PORTA}")
    servidor.serve_forever()


if __name__ == "__main__":
    iniciar_servidor()
