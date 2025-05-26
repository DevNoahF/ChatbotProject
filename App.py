from flask import Flask, request, jsonify
from flask_cors import CORS
import requests



from chatbot.Responses import palavras_chave, idnt_question


from config.settings import ROUTEROPENIA_API_KEY, change_tokens

app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse a API

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    bot_reply=""

    tipo_resposta = idnt_question(user_message)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {ROUTEROPENIA_API_KEY}", "Content-Type": "application/json"},
        json={"model": "openai/gpt-3.5-turbo", "messages": [
            {"role": "user", "content": user_message},
            {"role": "user", "content": "Você é um bot de atendimento ao cliente, seja educado, claro e objetivo"
            "Nós somos um site que criamos Designs para lojas virtuais, vendemos planos diferentes que oferecem diferentes vantagens,"
            "Plano Básico-Design Completo, ChatBot IA, Suporte 24h,"
            "Plano Completo-Design Completo, ChatBot IA, Suporte 24h, Relatório"
            "Plano Premium-Design Completo, ChatBot IA, Suporte 24h, Relatório e Taxa em 0.75%"
            "Sempre que você receber uma mensagem a qualquer coisa referente aos planos, você deve gerar uma resposta levando em conta o quê eu acabei de dizer a você"
            "Seja criativo ao gerar a resposta para chamar a atenção do cliente"
            },
            #Contexto para ele, mais tarde a gente adiciona as coisas
        ],
            "temperature":0.7,#Define se ele é determinístico ou criativo
            "max_tokens":change_tokens(user_message), #Define quantidade de caracteres
            "presence_penalty":0.3, #Define penalidade por sair do assunto
            "top_p":0.8 #Deixa mais favorável a usar palavras mais comuns
        }
    )
    if tipo_resposta==0:
        bot_reply = response.json()["choices"][0]["message"]["content"]


    if tipo_resposta==1:
        bot_reply="Não posso responder essa pergunta, pois não existe no meu banco de perguntas"


    if tipo_resposta !=0 and tipo_resposta !=1:
        bot_reply=f"Você quis dizer {tipo_resposta}"


    if not palavras_chave(user_message):
        bot_reply= "Desculpe, não posso responder a essa pergunta"

    print(f"tipo_resposta: {tipo_resposta}")
    print(f"palavras_chave: {palavras_chave(user_message)}")
    return jsonify({"ASSISTENTE": bot_reply})



if __name__ == "__main__":
    app.run(debug=True)
