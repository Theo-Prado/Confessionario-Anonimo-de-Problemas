from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sqlite3
from datetime import datetime

app = Flask(**name**)
CORS(app)

BANCO = "confessionario.db"

def conectar():
return sqlite3.connect(BANCO)

def criar_banco():
conn = conectar()
cursor = conn.cursor()

```
cursor.execute("""
CREATE TABLE IF NOT EXISTS relatos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    categoria TEXT NOT NULL,
    texto TEXT NOT NULL,
    data_criacao TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS respostas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relato_id INTEGER NOT NULL,
    texto TEXT NOT NULL,
    data_criacao TEXT NOT NULL,
    FOREIGN KEY(relato_id) REFERENCES relatos(id)
)
""")

conn.commit()
conn.close()
```

@app.route("/")
def home():
return send_file("index.html")

@app.route("/api/relatos", methods=["GET"])
def listar_relatos():

```
conn = conectar()
cursor = conn.cursor()

cursor.execute("""
SELECT id, categoria, texto, data_criacao
FROM relatos
ORDER BY id DESC
""")

relatos = cursor.fetchall()

resultado = []

for relato in relatos:

    relato_id = relato[0]

    cursor.execute("""
    SELECT id, texto, data_criacao
    FROM respostas
    WHERE relato_id = ?
    ORDER BY id ASC
    """, (relato_id,))

    respostas = cursor.fetchall()

    resultado.append({
        "id": relato[0],
        "categoria": relato[1],
        "texto": relato[2],
        "data": relato[3],
        "respostas": [
            {
                "id": r[0],
                "texto": r[1],
                "data": r[2]
            }
            for r in respostas
        ]
    })

conn.close()

return jsonify(resultado)
```

@app.route("/api/relatos", methods=["POST"])
def criar_relato():

```
dados = request.json

categoria = dados.get("categoria", "").strip()
texto = dados.get("texto", "").strip()

if not categoria or not texto:
    return jsonify({"erro": "Dados inválidos"}), 400

conn = conectar()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO relatos(categoria, texto, data_criacao)
VALUES (?, ?, ?)
""", (
    categoria,
    texto,
    datetime.now().strftime("%d/%m/%Y %H:%M")
))

conn.commit()
conn.close()

return jsonify({"sucesso": True})
```

@app.route("/api/respostas", methods=["POST"])
def criar_resposta():

```
dados = request.json

relato_id = dados.get("relato_id")
texto = dados.get("texto", "").strip()

if not relato_id or not texto:
    return jsonify({"erro": "Dados inválidos"}), 400

conn = conectar()
cursor = conn.cursor()

cursor.execute("""
INSERT INTO respostas(relato_id, texto, data_criacao)
VALUES (?, ?, ?)
""", (
    relato_id,
    texto,
    datetime.now().strftime("%d/%m/%Y %H:%M")
))

conn.commit()
conn.close()

return jsonify({"sucesso": True})
```

if **name** == "**main**":
criar_banco()
app.run(host="0.0.0.0", port=5000, debug=True)
