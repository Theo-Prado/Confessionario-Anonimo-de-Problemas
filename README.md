# Confessionário Anônimo

Sistema web para publicação e resposta de relatos anônimos.

## Funcionalidades

* Relatos anônimos
* Categorias
* Respostas aos relatos
* Banco de dados SQLite
* API REST
* Interface simples e responsiva

## Estrutura

PROJETO.py
index.html
confessionario.db

## Instalação

Instale as dependências:

pip install flask flask-cors

## Executar

python PROJETO.py

Acesse:

http://localhost:5000

## Banco de Dados

O banco SQLite é criado automaticamente na primeira execução.

Tabelas:

* relatos
* respostas

## API

### Listar relatos

GET /api/relatos

### Criar relato

POST /api/relatos

Exemplo:

{
"categoria":"Fé",
"texto":"Meu relato"
}

### Criar resposta

POST /api/respostas

Exemplo:

{
"relato_id":1,
"texto":"Minha resposta"
}

## Tecnologias

* Python
* Flask
* SQLite
* HTML
* CSS
* JavaScript

## Observação

Este projeto é educacional. Em produção recomenda-se:

* autenticação
* moderação de conteúdo
* filtro anti-spam
* paginação
* PostgreSQL
* HTTPS
* rate limiting
