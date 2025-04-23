# ServiceChat
# Imports
from rapidfuzz import process
from deep_translator import GoogleTranslator
from langdetect import detect_langs, DetectorFactory, LangDetectException

DetectorFactory.seed = 0


# ChatBot Class
class ChatBot:
    def __init__(self):
        self.selected_language_name = "English"
        self.selected_language = "en"
        self.bot_messages = []
        # The Bots Dictionary of Keywords to Look for, and Responses
        self.responses = {
            "hello": "Hi there!",
            "hi": "Hello there!",
            "help": "Please enter a few keywords.\n\nFor a list of keywords, Type 'Keywords'.",
            "keywords": "ServiceChat, Products, Services, Price, About, Contact",
            "how are you": "I'm just a chatbot, but I'm doing great! Thanks for asking.",
            "thank you": "No problem! I'm always happy to help.",
            "servicechat" : "ServiceChat is a customer service chatbot that is here to help you with all of your customer service related needs! It will be integrated into your website for users to gain quick access to.",
            "products" : "ServiceChat - Our brilliant customer service chatbot made to help your customers with their needs. It can answer a very wide range of questions, understand typos, think quickly, and more.",
            "services" : "Basic Maintenance - Make some tweaks to ServiceChat. \nHeavy Maintenance - Make significant changes to ServiceChat. \nTotal Maintenance Overhaul - Reimagine your whole ServiceChat experience.",
            "price" : "Our model is on sale for $250.00 CAD.",
            "about" : "ServiceChat was created by a computer science student in university. Our goal is to help small business owners with their overwhelming amount of customers that need attention.",
            "contact" : "Please feel free to contact me via my information below.",
            "basic maintenance" : "Make some tweaks to ServiceChat, for $50.",
            "heavy maintenance" : "Make significant changes to ServiceChat, for $100.",
            "total maintenanec overhaul" : "Reimagine your whole ServiceChat experience, for $150.",
        }
        # Words to Ignore when Iterating Through User Input
        self.stop_words = {"the", "is", "who", "what", "when", "where", "why", "how", "a", "an", "i", "im", "i'm",
                           "looking", "for", "to", "?", ".", ",", "much", "this", "that", "get", "for", "me", "money",
                           "does", "cost", "about", "need", "today", "am", "well", "need"}

    # The Default Response if the (Translated) User Input is not a Key Here
    def get_response(self, user_input):
        return self.responses.get(user_input.lower(),
                                  "I'm sorry, but I don't understand that.\n\nType 'Help' if you are lost.")


# Chat App Class
class ChatApp:
    def __init__(self):
        self.chatbot = ChatBot()
        self.user_input = ""
        self.detected_language = "en"

    # Detecting the Language of the User Input
    def detect_language(self, user_input):
        try:
            detected_langs = detect_langs(user_input)
            for lang in detected_langs:
                if lang.lang in {"en", "fr", "es"}:  # Understands, and Responds in English, French, and Spanish
                    return lang.lang
            return "en"
        except LangDetectException:
            return "en"

    # Used if the Bot Needs to Translate its Response
    def translate_text(self, user_input, target_language):
        if target_language == "en":
            return user_input
        try:
            translated_text = GoogleTranslator(source="auto", target=target_language).translate(user_input)
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            return user_input

    # When the User Sends a Message
    def send_message(self, user_input_text):
        # Stripping the User Input
        self.user_input = user_input_text.strip()
        if not self.user_input:
            return
        # Detecting the Language of the User Input
        self.detected_language = self.detect_language(self.user_input)
        translated_input = self.user_input
        # If the Language is not English, Try Translating it to English
        if self.detected_language != "en":
            try:
                translated_input = GoogleTranslator(source=self.detected_language, target="en").translate(
                    self.user_input)
            except Exception as e:
                print(f"Translation Error: {e}")
        # Making the Translated Input Lowercase, Splitting it Up
        user_input = translated_input.lower()
        words = user_input.split()
        filtered_words = [word for word in words if word not in self.chatbot.stop_words]
        user_input = " ".join(filtered_words)
        # Understanding Typos
        match = process.extractOne(user_input, self.chatbot.responses.keys(),
                                   score_cutoff=80)  # Understands Spelling 80% Accuracy or Above
        if match:
            user_input = str(match[0])
        self.bot_response = self.chatbot.get_response(user_input)
        self.bot_reply()

    # The Bot Translating its Response to the User Detected Language
    def bot_reply(self):
        translated_response = self.translate_text(self.bot_response, self.detected_language)
        print(translated_response)
        print("")


if __name__ == "__main__":
    chatbot = ChatApp()
    while True:
        user_input = input("You: ")
        chatbot.send_message(user_input)

