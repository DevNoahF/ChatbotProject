from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from chatbot.Responses import palavras_chave, idnt_question
from config.settings import ROUTEROPENIA_API_KEY, change_tokens

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "").strip()

    # Verifica palavras-chave primeiro
    tem_palavra_chave = palavras_chave(user_message)

    # Tenta identificar pergunta parecida
    tipo_resposta = idnt_question(user_message)

    bot_reply = ""

    if tem_palavra_chave or tipo_resposta == 0:
        # Se encontrou palavra-chave ou pergunta com alta confiança, chama a API
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ROUTEROPENIA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": (
                        "Você é um bot de atendimento ao cliente, seja educado, claro e objetivo, "
                        "evite usar palavras grandes e explicações desnecessárias. "
                        "Nós somos um site que criamos Designs para lojas virtuais, vendemos planos diferentes que oferecem diferentes vantagens. "
                        "Plano Básico: Design Completo, ChatBot IA, Suporte 24h. "
                        "Plano Completo: Design Completo, ChatBot IA, Suporte 24h, Relatório. "
                        "Plano Premium: Design Completo, ChatBot IA, Suporte 24h, Relatório e Taxa em 0.75%. "
                        "Sempre que você receber uma mensagem referente aos planos, gere uma resposta levando em conta essas informações."
                    )},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.3,
                "max_tokens": min(80, change_tokens(user_message)),
                "presence_penalty": 0.3,
                "top_p": 0.8
            }
        )
        bot_reply = response.json()["choices"][0]["message"]["content"]

    elif tipo_resposta == 1:
        bot_reply = "Não posso responder essa pergunta, pois não existe no meu banco de perguntas."

    else:
        # Aqui tipo_resposta é uma tupla com pergunta próxima e similaridade
        pergunta_sugerida, sim = tipo_resposta
        bot_reply = f"Você quis dizer: '{pergunta_sugerida}'? Pode explicar melhor?"

    # Se não tem palavra-chave e não reconheceu pergunta, resposta padrão
    if not tem_palavra_chave and tipo_resposta == 1:
        bot_reply = "Desculpe, não posso responder a essa pergunta."

    print(f"Mensagem: {user_message}")
    print(f"Palavras-chave: {tem_palavra_chave}")
    print(f"Tipo resposta: {tipo_resposta}")
    print(f"Resposta do bot: {bot_reply}")

    return jsonify({"ASSISTENTE": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
