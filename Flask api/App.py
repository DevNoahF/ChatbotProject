from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/mensagem", methods=["POST"])
def mensagem():
    dados = request.json
    mensagem = dados.get("mensagem")
    sender = dados.get("usuario", "usuario123")

    resposta = requests.post("http://localhost:5005/webhooks/rest/webhook", json={
        "sender": sender,
        "message": mensagem
    })

    return jsonify(resposta.json())

if __name__ == "__main__":
    app.run(port=5000)
