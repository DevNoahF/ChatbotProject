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

    # Verifica palavras-chave fitness/suplementos
    tem_palavra_chave = palavras_chave(user_message)

    # Verifica similaridade com perguntas frequentes
    tipo_resposta = idnt_question(user_message)

    bot_reply = ""

    if tem_palavra_chave or tipo_resposta == 0:
        # Gera resposta baseada em contexto de loja de suplementos
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {ROUTEROPENIA_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "system",
                        "content": (
                            "Você é um especialista em nutrição esportiva e atendimento ao cliente. "
                            "Atende em uma loja virtual de suplementos para academia. "
                            "Seja educado, claro e objetivo. Ajude o cliente a escolher os melhores produtos com base no objetivo dele, como ganho de massa, definição, energia ou recuperação. "
                            "Esclareça dúvidas sobre uso, combinações, efeitos, horários e resultados. "
                            "Evite termos técnicos desnecessários e foque em ser útil e direto."
                        )
                    },
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.3,
                "max_tokens": min(100, change_tokens(user_message)),
                "presence_penalty": 0.3,
                "top_p": 0.8
            }
        )
        bot_reply = response.json()["choices"][0]["message"]["content"]

    elif tipo_resposta == 1:
        bot_reply = "Desculpe, ainda não tenho informações suficientes para responder a isso com precisão."

    else:
        # tipo_resposta é uma tupla com sugestão de pergunta semelhante
        pergunta_sugerida, sim = tipo_resposta
        bot_reply = f"Você quis dizer: '{pergunta_sugerida}'? Pode explicar melhor para que eu possa te ajudar com o suplemento ideal?"

    # Resposta padrão se nada for identificado
    if not tem_palavra_chave and tipo_resposta == 1:
        bot_reply = "Desculpe, não consegui entender sua dúvida sobre suplementos. Pode reformular?"

    print(f"Mensagem do usuário: {user_message}")
    print(f"Palavras-chave detectadas: {tem_palavra_chave}")
    print(f"Tipo de resposta: {tipo_resposta}")
    print(f"Resposta do bot: {bot_reply}")

    return jsonify({"ASSISTENTE": bot_reply})


if __name__ == "__main__":
    app.run(debug=True)
