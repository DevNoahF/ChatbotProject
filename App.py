# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

from services.responses import get_bot_reply

app = Flask(__name__)
CORS(app)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")
    bot_reply = get_bot_reply(user_message)
    return jsonify({"ASSISTENTE": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)
