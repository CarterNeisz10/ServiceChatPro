# ServiceChat
# Imports
from rapidfuzz import process
import json
import os
import random

# ChatBot Class
class ChatBot:
    def __init__(self, business_id):  # Accept business_id
        self.bot_messages = []
        self.responses = self.load_responses(business_id)
        self.stop_words = {"the", "is", "who", "what", "when", "where", "why", "how", "a", "an", "i", "im", "i'm",
                           "looking", "for", "to", "?", ".", ",", "much", "this", "that", "get", "for", "me", "money",
                           "does", "about", "need", "today", "am", "well", "need", "people", "person", "slaves",
                           "slavery"}

    def get_response(self, user_input):
        possible_responses = self.responses.get(user_input.lower())
        if not possible_responses:
            return "I'm sorry, but I don't understand that.\n\nType 'Help' if you are lost."

        if isinstance(possible_responses, list):
            return random.choice(possible_responses)
        return possible_responses  # fallback if it's a string

    def load_responses(self, business_id):
        path = f"configs/{business_id}.json"
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
                return data.get("responses", {})
        else:
            print(f"[ERROR] No config found for {business_id}")
            return {}

# Chat App Class
class ChatApp:
    def __init__(self, business_id="default"):
        self.chatbot = ChatBot(business_id)
        self.user_input = ""
        self.bot_response = ""

    def send_message(self, user_input_text, business_id="default"):
        original_input = user_input_text.strip()
        self.user_input = original_input

        if not self.user_input:
            return "I'm sorry, I didn't catch that."

        try:
            with open(f"configs/{business_id}.json", "r") as f:
                response_data = json.load(f)
                self.chatbot.responses = response_data.get("responses", {})
        except FileNotFoundError:
            print(f"Response file for business ID '{business_id}' not found. Using default responses.")
            try:
                with open("configs/servicechat.json", "r") as f:
                    response_data = json.load(f)
                    self.chatbot.responses = response_data.get("responses", {})
            except Exception as e:
                print(f"Could not load default responses: {e}")
                self.chatbot.responses = {}

        original_lower = original_input.lower()

        # 🔑 Context-aware logic (BEFORE filtering or fuzzymatching)
        if original_lower in {"yes", "yeah", "yep"}:
            if "anything" in self.last_bot_message.lower() and "help" in self.last_bot_message.lower():
                self.bot_response = "What do you need help with?"
            else:
                self.bot_response = self.chatbot.get_response(original_lower)
        elif original_lower in {"no", "nah"}:
            if "anything" in self.last_bot_message.lower() and "help" in self.last_bot_message.lower():
                self.bot_response = "Okay! Have a great day."
            else:
                self.bot_response = self.chatbot.get_response(original_lower)
        else:
            # 💬 Continue with normal logic
            words = original_lower.split()
            filtered_words = [word for word in words if word not in self.chatbot.stop_words]
            filtered_input = " ".join(filtered_words)

            match = process.extractOne(filtered_input, self.chatbot.responses.keys(), score_cutoff=80)
            if match:
                matched_key = str(match[0])
            else:
                matched_key = filtered_input

            self.bot_response = self.chatbot.get_response(matched_key)

        self.last_bot_message = self.bot_response
        return self.bot_response

    def bot_reply(self):
        print(self.bot_response)
        print("")

if __name__ == "__main__":
    chatbot = ChatApp(business_id="servicechat")
    while True:
        user_input = input("You: ")
        response = chatbot.send_message(user_input)
        print(f"Bot: {response}")
