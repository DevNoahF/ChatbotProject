# services/responses.py

import requests
from config.settings import ROUTEROPENIA_API_KEY

def get_bot_reply(user_message):
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {ROUTEROPENIA_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": "openai/gpt-3.5-turbo",
            "messages": [
                {"role": "user", "content": user_message},
                {"role": "user", "content": "Você é um bot de atendimento ao cliente, seja educado, claro e objetivo"}
            ],
            "temperature": 0.3,
            "max_tokens": 50,
            "presence_penalty": 1.0
        }
    )

    return response.json()["choices"][0]["message"]["content"]
