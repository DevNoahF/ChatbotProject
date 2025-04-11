from flask import Flask, request, jsonify
from flask_cors import CORS
import requests


from chatbot.Responses import palavras_chave

from config.settings import ROUTEROPENIA_API_KEY

app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse a API

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {ROUTEROPENIA_API_KEY}", "Content-Type": "application/json"},
        json={"model": "openai/gpt-3.5-turbo", "messages": [
            {"role": "user", "content": user_message},
            {"role": "user", "content": "Você é um bot de atendimento ao cliente, seja educado, claro e objetivo"},
            #Contexto para ele, mais tarde a gente adiciona as coisas
        ],
            "temperature":0.3,#Define se ele é determinístico ou criativo
            "max_tokens":50, #Define quantidade de caracteres
            "presence_penalty":-2.0, #Define penalidade por sair do assunto
            "top_p":0.4 #Deixa mais favorável a usar palavras mais comuns
        }
    )
    palavras_chave(user_message)

    bot_reply = response.json()["choices"][0]["message"]["content"]
    if not palavras_chave(bot_reply):
        bot_reply= "Desculpe, não posso responder a essa pergunta"


    return jsonify({"ASSISTENTE": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
