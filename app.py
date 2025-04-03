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
