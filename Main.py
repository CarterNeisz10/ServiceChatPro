# ServiceChat
# Imports
from rapidfuzz import process
from deep_translator import GoogleTranslator
from langdetect import detect_langs, DetectorFactory, LangDetectException
import json
import os

DetectorFactory.seed = 0


# ChatBot Class
class ChatBot:
    def __init__(self, business_id):  # Accept business_id
        self.selected_language_name = "English"
        self.selected_language = "en"
        self.bot_messages = []
        self.responses = self.load_responses(business_id)  # Load business-specific responses
        self.stop_words = {"the", "is", "who", "what", "when", "where", "why", "how", "a", "an", "i", "im", "i'm",
                           "looking", "for", "to", "?", ".", ",", "much", "this", "that", "get", "for", "me", "money",
                           "does", "cost", "about", "need", "today", "am", "well", "need"}

    def get_response(self, user_input):
        return self.responses.get(user_input.lower(),
                                  "I'm sorry, but I don't understand that.\n\nType 'Help' if you are lost.")

    def load_responses(self, business_id):
        # Changed from 'configs/{business_id}_config.json' to 'configs/{business_id}.json'
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
        self.detected_language = "en"

    def detect_language(self, user_input):
        try:
            detected_langs = detect_langs(user_input)
            for lang in detected_langs:
                if lang.lang in {"en", "fr", "es"}:
                    return lang.lang
            return "en"
        except LangDetectException:
            return "en"

    def translate_text(self, user_input, target_language):
        if target_language == "en":
            return user_input
        try:
            translated_text = GoogleTranslator(source="auto", target=target_language).translate(user_input)
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            return user_input

    def send_message(self, user_input_text, business_id="default"):
        self.user_input = user_input_text.strip()
        if not self.user_input:
            return "I'm sorry, I didn't catch that."

        try:
            # Changed file path from 'responses/{business_id}.json' to 'configs/{business_id}.json'
            with open(f"configs/{business_id}.json", "r") as f:
                response_data = json.load(f)
                # Assumes the JSON has a "responses" key containing your dictionary of responses.
                self.chatbot.responses = response_data.get("responses", {})
        except FileNotFoundError:
            print(f"Response file for business ID '{business_id}' not found. Using default responses.")
            try:
                with open("configs/servicechat.json", "r") as f:  # Ensure you have a default file if needed
                    response_data = json.load(f)
                    self.chatbot.responses = response_data.get("responses", {})
            except Exception as e:
                print(f"Could not load default responses: {e}")
                self.chatbot.responses = {}

        self.detected_language = self.detect_language(self.user_input)
        translated_input = self.user_input
        if self.detected_language != "en":
            try:
                translated_input = GoogleTranslator(source=self.detected_language, target="en").translate(
                    self.user_input)
            except Exception as e:
                print(f"Translation Error: {e}")

        user_input = translated_input.lower()
        words = user_input.split()
        filtered_words = [word for word in words if word not in self.chatbot.stop_words]
        user_input = " ".join(filtered_words)

        match = process.extractOne(user_input, self.chatbot.responses.keys(), score_cutoff=80)
        if match:
            user_input = str(match[0])

        self.bot_response = self.chatbot.get_response(user_input)
        translated_response = self.translate_text(self.bot_response, self.detected_language)
        return translated_response

    def bot_reply(self):
        translated_response = self.translate_text(self.bot_response, self.detected_language)
        print(translated_response)
        print("")


if __name__ == "__main__":
    chatbot = ChatApp(business_id="servicechat")
    while True:
        user_input = input("You: ")
        response = chatbot.send_message(user_input)  # Added assignment to capture the response
        print(f"Bot: {response}")
