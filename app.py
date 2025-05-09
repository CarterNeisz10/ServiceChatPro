from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from Main import ChatApp
import os

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins

@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message")
        business_id = data.get("business_id", "default")  # Extract business_id

        print(f"Received message: {user_message}")
        print(f"Business ID: {business_id}")  # Debugging line

        if not user_message:
            return jsonify({"error": "No message provided"}), 400  # If no message, return an error

        chatbot = ChatApp(business_id)
        bot_response = chatbot.send_message(user_message)

        # Return a response to the frontend
        return jsonify({"response": bot_response})  # Send response back to frontend

    except Exception as e:
        print(f"Error processing request: {e}")
        return jsonify({"error": str(e)}), 500  # Return a helpful error message


@app.route("/")
def serve_chatbot():
    return send_from_directory("static", "chatbot.html")


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
