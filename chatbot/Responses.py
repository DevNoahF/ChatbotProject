# services/responses.py

import requests
from config.settings import ROUTEROPENIA_API_KEY

import json
import requests
from config.settings import ROUTEROPENIA_API_KEY

# Função para carregar o contexto do template com base no ID
def load_template_context(template_id):
    try:
        with open(f"templates_contexto/{template_id}.json", "r", encoding="utf-8") as f:
            return json.load(f)["contexto"]
    except FileNotFoundError:
        return "Você é um assistente virtual de atendimento. Seja educado, claro e objetivo."

# Função principal de resposta do bot
def get_bot_reply(user_message, template_id="loja_designs"): # Mudar o template se necessario
    contexto = load_template_context(template_id)

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {ROUTEROPENIA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "system", "content": contexto},
                {"role": "user", "content": user_message}
            ],
            "temperature": 0.3,
            "max_tokens": 100,
            "presence_penalty": -2.0,
            "top_p": 0.4
        }
    )

    return response.json()["choices"][0]["message"]["content"]

#Algum problema fez com que ele parasse de responder as perguntas
def palavras_chave(mensagem):
    palavras=["frete","produto", "valores", "plano", "Design","chatbot", "suporte", "loja virtual", "vantagens","planos" ]#Aqui fica as palavras chave que são RELEVANTES, as que não estiverem aqui não serão relevantes

    for palavras in palavras:
        if palavras.lower() in mensagem.lower():
            return True
    return False

