from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from config.settings import OPENIA_API_KEY

app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse a API

# gpt-4o-mini key
OPENIAROUTER_API_KEY = "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"
@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENIAROUTER_API_KEY}", "Content-Type": "application/json"},
        json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": user_message}]}
    )

    bot_reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"ASSISTENTE": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
