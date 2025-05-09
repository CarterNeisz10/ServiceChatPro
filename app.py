from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Main import ChatApp
import os

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")
    business_id = data.get("business_id", "default")

    chatbot = ChatApp(business_id)
    bot_response = chatbot.send_message(user_message, business_id)

    return jsonify({"response": bot_response})  # Send response back to frontend


@app.route("/")
def serve_chatbot():
    return send_from_directory("static", "chatbot.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
