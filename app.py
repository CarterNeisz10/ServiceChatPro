from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
from Main import ChatApp

app = Flask(__name__)

# Enable CORS for all routes
CORS(app, origins=["*"])  # Allow all origins (can specify your frontend domain instead of "*")


chatbot = ChatApp()


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get('message')
    business_id = request.json.get('business_id', 'default')

    chatbot = ChatApp(business_id)
    chatbot.send_message(user_input)
    bot_response = chatbot.bot_reply()  # Get the response

    return jsonify({"response": bot_response})  # Send the response back to the frontend





from flask import send_from_directory

@app.route("/")
def serve_chatbot():
    return send_from_directory("static", "chatbot.html")

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



