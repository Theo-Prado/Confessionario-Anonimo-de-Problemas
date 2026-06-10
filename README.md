# Confessionário Anônimo de Problemas

## 🎯 Visão Geral

O **Confessionário Anônimo de Problemas** é uma plataforma web moderna onde usuários podem compartilhar relatos anônimos sobre dificuldades pessoais e responder com solidariedade a outros. O sistema categoriza automaticamente os relatos e permite que a comunidade se sinta apoiada.

> ⚠️ **Importante:** Este projeto não oferece terapia nem aconselhamento profissional. É uma ferramenta de apoio comunitário anônimo.

## ✨ Funcionalidades Principais

### 📝 Relatos Anônimos
- Envio de relatos privados sem dados pessoais
- Anonimização automática de emails, telefones e nomes
- Limite de 1500 caracteres por relato
- Validação de conteúdo (mínimo 8 caracteres)

### 🏷️ Categorização Automática
- **Ansiedade** - Medos, pânico, estresse, insegurança
- **Família** - Conflitos familiares, briga, relacionamento
- **Estudos** - Dificuldades escolares, notas, pressão
- **Amizades** - Solidão, traição, rejeitamento
- **Fé** - Questões espirituais, religião, culpa
- **Relacionamento** - Amor, paixão, ciúmes, divórcio
- **Saúde** - Doenças, tratamentos, diagnósticos
- **Carreira** - Emprego, demissão, profissão

### 💬 Sistema de Respostas
- Responda com solidariedade a qualquer relato
- Respostas anônimas (sem identificação)
- Histórico de respostas persistido
- Validação de respostas (5-1000 caracteres)

### 📊 Estatísticas Comunitárias
- Percentuais por categoria em tempo real
- Contagem de relatos por problema
- Busca de relatos semelhantes
- Dashboard com gráficos responsivos

### 💾 Persistência de Dados
- Armazenamento em JSON local (`dados.json`)
- Sincronização automática após cada ação
- Recuperação de dados entre sessões

### 🎨 Interface Moderna
- Design glassmorphism responsivo
- Tema escuro com gradientes suaves
- Animações fluidas e intuitivas
- Totalmente acessível (aria-labels)

## 🛠️ Tecnologias

| Componente | Tecnologia |
|-----------|-----------|
| **Backend** | Python 3 (biblioteca padrão) |
| **Servidor** | `http.server` + `ThreadingHTTPServer` |
| **Frontend** | HTML5 + CSS3 + JavaScript puro |
| **Persistência** | JSON |
| **APIs** | REST puro (sem frameworks) |

## 📁 Estrutura do Projeto

```
/
├── app.py              # Backend principal (Python)
├── index.html          # Frontend (HTML + CSS + JS)
├── dados.json          # Armazenamento persistido (gerado automaticamente)
└── README.md           # Esta documentação
```

## 🚀 Como Executar

### Pré-requisitos
- Python 3.8+
- Navegador web moderno

### Instalação e Execução

1. **Verifique a versão do Python:**
   ```bash
   python --version
   ```

2. **Execute o servidor:**
   ```bash
   python app.py
   ```

3. **Acesse no navegador:**
   ```
   http://localhost:8000
   ```

### Saída Esperada
```
============================================================
🔐 Confessionário Anônimo de Problemas
============================================================
✅ Servidor iniciado com sucesso!
🌐 Acesse: http://localhost:8000
📁 Dados salvos em: /caminho/para/dados.json
============================================================
Pressione Ctrl+C para parar o servidor.
============================================================
```

## 📚 Exemplos de Uso

### Exemplo 1: Enviar Relato
```
Relato enviado:
"Tenho dificuldade de manter uma rotina de oração."

Resposta:
✅ Categoria detectada: Fé
✅ Relatos semelhantes: 3
✅ Mensagem: "Você não está sozinho."
```

### Exemplo 2: Responder com Solidariedade
```
Relato original:
"Tenho medo do futuro e fico ansioso."

Sua resposta:
"Entendo sua ansiedade. Já passei por isso também. 
Recomendo praticar meditação."

✅ Resposta publicada anonimamente
```

### Exemplo 3: Visualizar Estatísticas
```
Problemas mais comuns:
- Ansiedade: 35%
- Família: 25%
- Estudos: 15%
- Amizades: 10%
- Fé: 8%
- Relacionamento: 5%
- Saúde: 2%
```

## 🏗️ Arquitetura

### Backend (`app.py`)

#### Classe `Relato`
```python
@dataclass
class Relato:
    id: str              # UUID único
    texto: str           # Conteúdo anonimizado
    categoria: str       # Categoria detectada
    data: str            # Timestamp ISO 8601
    respostas: List      # Respostas associadas
```

#### Classe `Resposta`
```python
@dataclass
class Resposta:
    id: str              # UUID único
    relato_id: str       # ID do relato respondido
    texto: str           # Conteúdo da resposta
    data: str            # Timestamp ISO 8601
```

#### Classe `ConfessionarioApp`
Métodos principais:
- `adicionar_relato(texto)` - Cria novo relato
- `adicionar_resposta(relato_id, texto)` - Adiciona resposta
- `buscar_semelhantes(texto, categoria)` - Encontra relatos similares
- `gerar_estatisticas()` - Calcula distribuição por categoria
- `listar_relatos(categoria)` - Lista com filtro opcional
- `obter_relato(relato_id)` - Retorna um relato específico

### Frontend (HTML/JS)

#### Endpoints da API

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| `GET` | `/api/relatos` | Lista todos os relatos |
| `GET` | `/api/relatos?categoria=Fé` | Filtra por categoria |
| `GET` | `/api/relatos/{id}` | Retorna relato específico |
| `GET` | `/api/estatisticas` | Estatísticas gerais |
| `GET` | `/api/categorias` | Lista categorias com contagem |
| `POST` | `/api/relatos` | Cria novo relato |
| `POST` | `/api/relatos/{id}/respostas` | Adiciona resposta |

#### Fluxo da Aplicação

```
1. Usuário digita um relato
   ↓
2. Frontend envia POST /api/relatos
   ↓
3. Backend:
   - Anonimiza dados pessoais
   - Classifica por categoria
   - Busca semelhantes
   - Persiste em JSON
   ↓
4. Frontend atualiza:
   - Estatísticas em tempo real
   - Mural com novo relato
   - Modal com confirmação
   ↓
5. Usuários podem clicar para ver respostas
   ↓
6. Qualquer um pode responder anonimamente
   ↓
7. Respostas são persistidas e sincronizadas
```

## 🔐 Segurança & Privacidade

### Anonimização
- Remove automaticamente padrões de email: `user@example.com`
- Remove padrões de telefone: `(11) 9999-9999`
- Substitui nomes: "Meu nome é João" → "Meu nome é [nome removido]"

### Proteções
- `X-Content-Type-Options: nosniff` - Previne MIME sniffing
- `X-Frame-Options: DENY` - Bloqueia frame embedding
- CORS habilitado apenas para localhost
- Validação de tamanho (5MB máximo por requisição)

### Limitações
Este MVP remove apenas padrões simples. Para produção, seria necessário:
- Criptografia de dados em repouso
- HTTPS mandatório
- Validação mais robusta (NLP/IA)
- Moderação e denúncias
- Conformidade com LGPD/GDPR

## 📊 Formato de Dados (dados.json)

```json
[
  {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "texto": "Tenho medo do futuro e sinto muita ansiedade.",
    "categoria": "Ansiedade",
    "data": "2026-06-10T21:52:30Z",
    "respostas": [
      {
        "id": "650e8400-e29b-41d4-a716-446655440001",
        "relato_id": "550e8400-e29b-41d4-a716-446655440000",
        "texto": "Você não está sozinho. Muitos sentem o mesmo.",
        "data": "2026-06-10T21:53:15Z"
      }
    ]
  }
]
```

## 🎯 Melhorias Futuras

- [ ] Banco de dados persistente (PostgreSQL/MongoDB)
- [ ] Autenticação opcional (modo anônimo por padrão)
- [ ] IA para agrupamento semântico avançado
- [ ] Dashboard administrativo com moderação
- [ ] API REST documentada com Swagger
- [ ] Aplicativo mobile (React Native)
- [ ] Sistema de denúncias e moderação comunitária
- [ ] Criptografia E2E para dados sensíveis
- [ ] Integração com linhas de ajuda profissional
- [ ] Suporte multilíngue
- [ ] Análise de sentimento com IA

## ⚠️ Avisos Legais

1. **Não substitui ajuda profissional** - Este é um espaço de apoio comunitário
2. **Moderação limitada** - Contato com números de emergência disponível
3. **Dados em memória** - Reiniciar o servidor limpa dados não salvos
4. **Uso responsável** - Respeite outros usuários

## 📝 Licença

Este projeto é fornecido como exemplo educacional. Sinta-se livre para modificar e distribuir.

## 💙 Contribuindo

Sugestões e melhorias são bem-vindas! Alguns pontos para contribuir:
- Melhorar algoritmos de categorização
- Adicionar novas categorias
- Aprimorar UI/UX
- Implementar testes
- Documentação

---

**Desenvolvido com ❤️ para criar um espaço seguro de partilha e apoio mútuo.**
