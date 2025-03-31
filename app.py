from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Permite que o frontend acesse a API

# API gratuita do OpenRouter (substitui OpenAI)
OPENROUTER_API_KEY = "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"

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json"},
        json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": user_message}]}
    )

    bot_reply = response.json()["choices"][0]["message"]["content"]
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
