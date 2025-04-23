from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from Main import ChatApp

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

chatbot = ChatApp()


@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "")

    if not user_input:
        return jsonify({"error": "No input provided"}), 400

    response = chatbot.send_message(user_input)  # Get chatbot's response
    return jsonify({"response": chatbot.bot_response})  # Return translated response


import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



