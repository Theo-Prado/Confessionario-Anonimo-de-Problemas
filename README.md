# Confessionário Anônimo de Problemas

## Visão Geral

O **Confessionário Anônimo de Problemas** é um MVP de plataforma web onde qualquer pessoa pode compartilhar dificuldades, medos, dúvidas, fracassos, inseguranças, problemas familiares, problemas de relacionamento, dúvidas de fé e outros dilemas cotidianos de forma totalmente anônima e segura.

O projeto não oferece terapia nem aconselhamento profissional. Seu objetivo é criar uma experiência acolhedora para mostrar que outras pessoas vivem situações parecidas e que ninguém precisa enfrentar seus desafios sozinho.

Quando alguém envia um relato, o sistema:

- remove padrões simples de dados pessoais;
- classifica o conteúdo por categoria;
- busca relatos semelhantes;
- retorna uma mensagem de apoio;
- mostra estatísticas emocionais da comunidade;
- atualiza o mural anônimo da interface.

## Funcionalidades

- Envio de relatos anônimos por uma interface moderna.
- Backend local em Python puro, sem frameworks pesados.
- Programação Orientada a Objetos com as classes `Relato` e `Confessionario`.
- Armazenamento em memória para facilitar execução e demonstração.
- Anonimização básica de e-mails, telefones e apresentações com nome.
- Classificação automática em categorias como Ansiedade, Família, Estudos, Amizades, Fé e Outros.
- Busca simples de relatos semelhantes por categoria e termos em comum.
- Estatísticas percentuais por categoria.
- Mural com relatos fictícios e relatos enviados durante a sessão.
- Design responsivo com tema escuro, glassmorphism, blur, bordas arredondadas e animações leves.
- Aviso explícito de privacidade e de não substituição de ajuda profissional.

## Tecnologias

- **Backend:** Python 3
- **Servidor local:** `http.server` e `ThreadingHTTPServer` da biblioteca padrão
- **Frontend:** HTML, CSS e JavaScript puro
- **Dados:** armazenamento em memória
- **Estilo visual:** tema escuro, glassmorphism, gradientes, sombras suaves e responsividade

## Estrutura do Projeto

```text
/
├── PROJETO.py
├── index.html
└── README.md
```

## Como Executar

1. Verifique se você possui Python 3 instalado:

   ```bash
   python --version
   ```

2. Execute o servidor local na raiz do projeto:

   ```bash
   python PROJETO.py
   ```

3. Acesse a aplicação no navegador:

   ```text
   http://localhost:8000
   ```

4. Alternativa: também é possível abrir o `index.html` diretamente no navegador, mas a API só funcionará se o servidor Python estiver rodando em `http://localhost:8000`.

## Exemplos de Uso

### Exemplo 1

Relato enviado:

```text
Tenho dificuldade de manter uma rotina de oração.
```

Resposta esperada:

```text
Você não está sozinho.
Categoria detectada: Fé
Pessoas com relatos semelhantes: número calculado a partir da sessão atual
```

### Exemplo 2

Relato enviado:

```text
Tenho medo do futuro e fico ansioso antes de dormir.
```

Resposta esperada:

```text
Você não está sozinho.
Categoria detectada: Ansiedade
Pessoas com relatos semelhantes: número calculado a partir da sessão atual
```

### Exemplo 3

Relato enviado:

```text
Briguei com minha família e não sei como conversar de novo.
```

Resposta esperada:

```text
Você não está sozinho.
Categoria detectada: Família
Pessoas com relatos semelhantes: número calculado a partir da sessão atual
```

## Arquitetura

### Classe `Relato`

A classe `Relato` representa uma confissão anônima dentro do sistema. Ela possui os atributos obrigatórios:

- `id`: identificador único gerado com UUID;
- `texto`: conteúdo anonimizado do relato;
- `categoria`: categoria detectada pelo classificador;
- `data`: data de criação em formato ISO.

### Classe `Confessionario`

A classe `Confessionario` concentra as regras principais do MVP:

- `adicionar_relato()`: recebe um texto, remove dados pessoais simples, classifica o relato, salva em memória e retorna a análise;
- `buscar_semelhantes()`: encontra relatos parecidos por categoria ou por palavras em comum;
- `gerar_estatisticas()`: calcula totais e percentuais de relatos por categoria;
- `listar_relatos()`: retorna os relatos em ordem recente para a interface ou futuras integrações.

### Fluxo da aplicação

1. O usuário digita um problema na interface.
2. O JavaScript exibe o estado `Analisando...`.
3. O frontend envia o relato para `POST /api/relatos`.
4. O backend anonimiza padrões sensíveis simples.
5. O backend classifica o relato com palavras-chave auditáveis.
6. O backend busca relatos semelhantes já armazenados em memória.
7. O backend retorna categoria, quantidade de semelhantes, mensagem de apoio e estatísticas.
8. A interface atualiza o cartão de resultado, os gráficos e o mural anônimo.

## Melhorias Futuras

- Banco de dados persistente.
- Login opcional com modo totalmente anônimo por padrão.
- IA para agrupamento semântico de relatos semelhantes.
- Dashboard administrativo com moderação e métricas agregadas.
- API REST documentada com autenticação para integrações.
- Aplicativo mobile.
- Sistema de denúncias e moderação comunitária.
- Criptografia adicional para dados sensíveis.
- Detecção mais robusta de informações pessoais.
- Integração com recursos de ajuda profissional e contatos de emergência.

## Observação de Privacidade

Este MVP remove apenas padrões simples de dados pessoais, como e-mails e telefones. Em produção, seria necessário usar técnicas mais robustas de privacidade, revisão de segurança, moderação de conteúdo e conformidade com regulamentações como LGPD e GDPR. Os dados são armazenados apenas em memória durante a sessão e não persistem após o servidor ser interrompido.

## Licença

Este projeto é fornecido como exemplo educacional e pode ser livremente modificado e distribuído.
