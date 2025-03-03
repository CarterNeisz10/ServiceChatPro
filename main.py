# ServiceChat
# Version 1.1
# fix the clear chat issue.
# connect this to git
# follow the rest of chats steps

# Imports
import sys

import pyttsx3
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import (QWidget, QGraphicsDropShadowEffect)
from deep_translator import GoogleTranslator
from langdetect import detect_langs, DetectorFactory, LangDetectException

DetectorFactory.seed = 0


# ChatBot Class
class ChatBot:
    # The Init Setup
    def __init__(self):
        # Keywords and Responses
        self.responses = {
            "hello": "Hi there!",
            "hi": "Hello there!",
            "help": "Please enter a few keywords.\n\nFor a list of keywords, Type 'Keywords'.\n\nTo toggle 'Dark Mode', press the Black Button.\nTo toggle back to 'Light Mode', press the Yellow Button.\n\nTo 'Clear Chat', press the Red Button.\n\n",
            "keywords": "The company's keywords will be here.",
            "how are you": "I'm just a chatbot, but I'm doing great! Thanks for asking.",
            "thank you": "No problem! I'm always happy to help.",
            "website": "Of course! Allow me to help with any of your Customer Service needs!"
        }

        # Stop Words to Ignore
        self.stop_words = {"the", "is", "who", "what", "when", "where", "why", "how", "a", "an", "i", "im", "i'm",
                           "looking", "for", "to", "?", ".", ",", "much", "this", "that", "get", "for", "me", "money",
                           "does", "cost", "about", "need", "today", "am", "well", "need"}

    # Response if the Bot does not Understand the User Input
    def get_response(self, user_input):
        return self.responses.get(user_input.lower(),
                                  "I'm sorry, but I don't understand that.\n\nType 'Help' if you are lost.")


# ChatApp Class
class ChatApp(QWidget):
    # imports
    pass


import random
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
                             QLineEdit, QPushButton, QScrollArea, QSizePolicy)
from PyQt5.QtCore import Qt, QTimer
from rapidfuzz import process


# ChatApp Class
class ChatApp(QWidget):
    # The Init Setup
    def __init__(self):
        super().__init__()

        # Initializing Typing Label, Timers, Default Language, UI colour
        self.latest_edit_button = None
        self.bot_message_index = None
        self.current_bot_message = None
        self.latest_bot_buttons = None
        self.bot_label = None
        self.bot_response = None
        self.user_input = None
        self.detected_language = None
        self.typing_help_timer = None
        self.typing_welcome_timer = None
        self.help_index = None
        self.current_help_message = None
        self.welcome_index = None
        self.current_welcome_message = None
        self.help_label = None
        self.welcome_label = None
        self.typing_label = None
        self.typing_animation_timer = QTimer(self)
        self.typing_animation_timer.timeout.connect(self.update_typing_indicator)
        self.typing_timer = QTimer(self)
        self.typing_timer.timeout.connect(self.bot_reply)
        self.typing_effect_timer = QTimer(self)
        self.typing_effect_timer.timeout.connect(self.type_next_character)
        self.typing_state = 0
        self.dark_mode = False
        self.user_messages = []
        self.send_button_color = "black"
        self.selected_language_name = "English"
        self.selected_language = "en"
        self.bot_messages = []

        # Initializing the Main Window
        self.setWindowTitle("ServiceChat")
        self.setGeometry(100, 100, 500, 600)
        self.setStyleSheet("background-color: #FFFFFF; color: black;")
        self.chatbot = ChatBot()

        # Main Layout
        main_layout = QVBoxLayout(self)

        # Initializing the Scrollable Chat Area
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setStyleSheet("background-color: #FFFFFF; border: none;")
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.chat_layout = QVBoxLayout(self.scroll_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.scroll_area.setWidget(self.scroll_widget)
        main_layout.addWidget(self.scroll_area)

        # Initializing the Input Container (Holds the Input Field and Buttons)
        self.input_container = QWidget()
        self.input_container.setStyleSheet("""
        background-color: #FFFFFF;
        border-radius: 20px;
        border: 1px solid light-gray;
        """)
        input_layout = QVBoxLayout(self.input_container)
        input_layout.setContentsMargins(10, 10, 10, 10)

        # Initializing the Input Field
        self.input_field = QLineEdit(self)
        self.input_field.setPlaceholderText("Type a message...")
        self.input_field.setStyleSheet(
            "background-color: transparent; color: black; padding-top: 5px; font-size: 14px; border: none;")
        self.input_field.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.input_field.returnPressed.connect(self.send_message)

        # Initializing Buttons
        # Creating a horizontal layout for buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.setSpacing(10)
        buttons_layout.setAlignment(Qt.AlignLeft)

        # Bottom Buttons Container (Dark Mode, Clear Chat, Settings)
        bottom_buttons_container = QWidget()
        bottom_buttons_layout = QHBoxLayout(bottom_buttons_container)
        bottom_buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Send Button (Black, Circular, Hover Effect)
        self.send_button = QPushButton("↑")
        self.send_button.setFixedSize(40, 40)
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: black; 
                color: white; 
                border-radius: 20px; 
                font-size: 20px; 
                border: 1px grey;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050; /* Dark grey on hover */
            }
        """)
        self.send_button.clicked.connect(self.send_message)

        # Dark Mode Button (Black, Circular, Hover Effect)
        self.dark_mode_button = QPushButton("🌙")
        self.dark_mode_button.setFixedSize(30, 30)
        self.dark_mode_button.setStyleSheet("""
            QPushButton {
                background-color: black; 
                color: white; 
                border-radius: 15px; 
                border: 1px solid grey;
            }
            QPushButton:hover {
                background-color: #505050; /* Dark grey on hover */
            }
        """)
        self.dark_mode_button.clicked.connect(self.toggle_theme)
        buttons_layout.addWidget(self.dark_mode_button)

        '''
        # Clear Chat Button (Red, Circular, Hover Effect)
        self.clear_chat_button = QPushButton("🗑️")
        self.clear_chat_button.setFixedSize(30, 30)
        self.clear_chat_button.setStyleSheet("""
            QPushButton {
                background-color: red; 
                color: white; 
                border-radius: 15px; 
                border: 1px solid grey;
            }
            QPushButton:hover {
                background-color: #FF8888; /* Dark grey on hover */
            }
        """)
        if self.clear_chat_button.clicked:
            for i in range(2):
                self.clear_chat_button.clicked.connect(self.clear_chat)
        buttons_layout.addWidget(self.clear_chat_button)
        '''

        # Scroll to Bottom Button (White, Circular, Hidden by Default)
        self.scroll_to_bottom_btn = QPushButton("↓")
        self.scroll_to_bottom_btn.setFixedSize(40, 40)
        self.scroll_to_bottom_btn.setStyleSheet("""
            background-color: white; 
            color: black; 
            border-radius: 20px; 
            font-size: 20px;
            border: 1px solid black;
        """)
        self.scroll_to_bottom_btn.setVisible(False)  # Initially hidden
        self.scroll_to_bottom_btn.clicked.connect(self.scroll_to_bottom)

        # Layout for the Input and Send Button
        input_row_layout = QHBoxLayout()
        input_row_layout.addWidget(self.input_field)
        input_row_layout.addWidget(self.send_button)
        input_layout.addLayout(input_row_layout)

        # Adding Buttons to Input Layout
        input_layout.addLayout(buttons_layout)

        # Adding Input Container to the Main Layout
        main_layout.addWidget(self.input_container)
        self.apply_shadow(self.input_container)

        # Adding Scroll Down Button to Chat Area
        chat_area_layout = QVBoxLayout(self.scroll_area)
        chat_area_layout.addWidget(self.scroll_to_bottom_btn, alignment=Qt.AlignCenter | Qt.AlignBottom)
        self.scroll_area.verticalScrollBar().valueChanged.connect(self.check_scroll_position)
        self.chatbot.app_instance = self

        # Calling the Welcome Message Function As Soon As Application is Opened
        self.add_welcome_message()

    '''Welcome Messages, Typing Animations, UI Quality of Life'''  # -------------------------------------------------------------------------------------------------------------------------------------------------

    # Adding a shadow effect to the bottom box
    @staticmethod
    def apply_shadow(widget):
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(Qt.gray)
        widget.setGraphicsEffect(shadow)

    # Dynamically Adjusting the Input Field Height
    def adjust_input_field_height(self):
        document = self.input_field.document()
        document.setTextWidth(self.input_field.width())
        new_height = document.size().height() + 10
        max_height = 100
        min_height = 40
        self.input_field.setFixedHeight(min(max_height, max(new_height, min_height)))

    # Checking the Vertical Position that the User is At
    def check_scroll_position(self):
        scroll_bar = self.scroll_area.verticalScrollBar()
        if scroll_bar.value() < scroll_bar.maximum() - 50:
            self.scroll_to_bottom_btn.setVisible(True)
        else:
            self.scroll_to_bottom_btn.setVisible(False)

    # The Initial Welcome Message When the Program is Opened or Clear Chat is Called
    def add_welcome_message(self):
        # Creating a QLabel for the Welcome Message
        self.welcome_label = QLabel("")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        self.welcome_label.setWordWrap(True)
        # Setting the Font Size and Making it Bold
        font = QFont()
        font.setPointSize(22)
        font.setBold(True)
        self.welcome_label.setFont(font)
        # Creating QLabel for the Smaller "How can I help?" Message
        self.help_label = QLabel("")
        self.help_label.setAlignment(Qt.AlignCenter)
        self.help_label.setWordWrap(True)
        # Setting it to be a Smaller Font Size
        help_font = QFont()
        help_font.setPointSize(14)
        self.help_label.setFont(help_font)
        self.help_label.setStyleSheet("color: gray;")
        # Formatting the Big Message On Top and Small On Bottom
        self.chat_layout.addWidget(self.welcome_label, alignment=Qt.AlignCenter)
        self.chat_layout.addWidget(self.help_label, alignment=Qt.AlignCenter)
        # Initializing the Typing Animation Effect for Both Messages
        self.current_welcome_message = "Welcome to ServiceChat!"
        self.welcome_index = 0
        self.current_help_message = "How can I help?\n\n"
        self.help_index = 0
        self.typing_welcome_timer = QTimer(self)
        self.typing_welcome_timer.timeout.connect(self.type_next_welcome_character)
        self.typing_welcome_timer.start(50)

        # Animation of Typing Effect for the Beginning Message

    def type_next_welcome_character(self):
        if self.welcome_index < len(self.current_welcome_message):
            text = self.current_welcome_message[:self.welcome_index + 1]
            self.welcome_label.setText(text + " ●")
            self.welcome_index += 1
            self.typing_welcome_timer.start(random.randint(25, 70))
        else:
            self.typing_welcome_timer.stop()
            self.welcome_label.setText(self.current_welcome_message)
            QTimer.singleShot(500, self.start_help_typing)

    # Animation of Typing Effect for the Second Beginning Message
    def start_help_typing(self):
        self.typing_help_timer = QTimer(self)
        self.typing_help_timer.timeout.connect(self.type_next_help_character)
        self.typing_help_timer.start(50)

        # Animation of Typing the Second Message

    def type_next_help_character(self):
        if self.help_label is None:
            return
        if self.help_index < len(self.current_help_message):
            text = self.current_help_message[:self.help_index + 1]
            self.help_label.setText(text + " ●")
            self.help_index += 1
            self.typing_help_timer.start(random.randint(25, 70))
        else:
            self.typing_help_timer.stop()
            self.help_label.setText(self.current_help_message)

            # Setting the Typing Indicator Animation

    def update_typing_indicator(self):
        if self.typing_label:
            dot_color = "white" if self.dark_mode else "black"
            dots = ["", f'<span style="color:{dot_color}">●</span>',
                    f'<span style="color:{dot_color}">● ●</span>',
                    f'<span style="color:{dot_color}">● ● ●</span>']
            self.typing_state = (self.typing_state + 1) % len(dots)
            self.typing_label.setText(dots[self.typing_state])

    '''Language Detection and Translation'''  # -------------------------------------------------------------------------------------------------------------------------------------------------

    # Detecting Language of User Message in English French or Spanish
    @staticmethod
    def detect_language(text):
        try:
            if len(text) < 5:
                text = (text + " ") * 3
            detected_langs = detect_langs(text)
            print(f"Raw Language Detection Results: {detected_langs}")
            # Filter for allowed languages English, French, Spanish
            for lang in detected_langs:
                if lang.lang in {"en", "fr", "es"}:
                    return lang.lang
            return "en"
        except LangDetectException:
            return "en"

            # Translating Text from Dictionary Value to Detected Language

    @staticmethod
    def translate_text(text, target_language):
        if target_language == "en":
            return text
        try:
            translated_text = GoogleTranslator(source="auto", target=target_language).translate(text)
            return translated_text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    '''Sending User and Bot Messages'''  # -------------------------------------------------------------------------------------------------------------------------------------------------

    # User Sending Message
    def send_message(self):
        user_input_text = self.input_field.text().strip()
        if not user_input_text:
            return
            # Detecting Language
        self.detected_language = self.detect_language(user_input_text)
        self.add_user_message(user_input_text)
        translated_input = user_input_text
        if self.detected_language != "en":
            try:
                translated_input = GoogleTranslator(source=self.detected_language, target="en").translate(
                    user_input_text)
            except Exception as e:
                print(f"Translation Error: {e}")
        # Splitting and Joining Words
        user_input = translated_input.lower()
        words = user_input.split()
        filtered_words = [word for word in words if word not in self.chatbot.stop_words]
        user_input = " ".join(filtered_words)
        # Typo Handling
        match = process.extractOne(user_input, self.chatbot.responses.keys(), score_cutoff=80)
        if match:
            user_input = str(match[0])
        # Change send button to a square when bot starts typing
        self.send_button.setText("■")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050; /* Dark grey on hover */
            }
        """)
        self.send_button.clicked.disconnect()
        self.send_button.clicked.connect(self.stop_typing)
        # Add typing indicator
        self.add_typing_indicator()
        self.typing_animation_timer.start(500)
        bot_response = self.chatbot.get_response(user_input)
        word_count = len(bot_response.split())
        if word_count <= 5:
            delay = random.uniform(0.5, 1.5) * 1000
        elif word_count <= 15:
            delay = random.uniform(1.5, 3.0) * 1000
        else:
            delay = random.uniform(3.0, 6.0) * 1000
        self.typing_timer.start(int(delay))
        self.user_input = user_input
        self.bot_response = bot_response
        self.input_field.clear()
        self.scroll_to_bottom()

    # Displaying the User Message
    def add_user_message(self, message):
        msg_layout = QHBoxLayout()
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        self.user_messages.append(msg_label)
        self.update_user_message_color(msg_label)
        msg_layout.addStretch()
        msg_layout.addWidget(msg_label)
        msg_label.installEventFilter(self)
        self.chat_layout.addLayout(msg_layout)
        self.scroll_to_bottom()

    # Creating the Bot Message
    def add_bot_message(self):
        if hasattr(self, "latest_bot_buttons") and self.latest_bot_buttons:
            self.latest_bot_buttons.setParent(None)
        self.latest_bot_buttons = None
        bot_container = QWidget()
        bot_container.setStyleSheet("background: transparent;")
        bot_container.setObjectName("bot_container")
        bot_layout = QVBoxLayout()
        # Bot Message Label
        self.bot_label = QLabel("")
        font = QFont()
        font.setPointSize(17)
        self.bot_label.setFont(font)
        self.bot_label.setWordWrap(True)
        # Buttons Layout
        button_layout = QHBoxLayout()
        button_layout.setSpacing(5)
        button_layout.setContentsMargins(0, 0, 0, 0)
        # Text-to-Speech Button
        tts_button = QPushButton("🔊")
        tts_button.setFixedSize(30, 30)
        tts_button.setStyleSheet(self.get_default_button_style())
        tts_button.clicked.connect(lambda: self.speak_message(self.bot_label.text()))
        # Thumbs Up Button
        thumbs_up_button = QPushButton("👍")
        thumbs_up_button.setFixedSize(30, 30)
        thumbs_up_button.setStyleSheet(self.get_default_button_style())
        thumbs_up_button.clicked.connect(lambda: self.rate_message(self.bot_label, "up"))
        # Thumbs Down Button
        thumbs_down_button = QPushButton("👎")
        thumbs_down_button.setFixedSize(30, 30)
        thumbs_down_button.setStyleSheet(self.get_default_button_style())
        thumbs_down_button.clicked.connect(lambda: self.rate_message(self.bot_label, "down"))
        # Copy Button
        copy_button = QPushButton("📋")
        copy_button.setFixedSize(30, 30)
        copy_button.setStyleSheet(self.get_default_button_style())
        copy_button.clicked.connect(lambda: self.copy_to_clipboard(self.bot_label.text()))
        # Other Stuff
        button_layout.addWidget(tts_button)
        button_layout.addWidget(thumbs_up_button)
        button_layout.addWidget(thumbs_down_button)
        button_layout.addWidget(copy_button)
        button_layout.addStretch()
        button_container = QWidget()
        button_container.setLayout(button_layout)
        button_container.setVisible(True)
        self.latest_bot_buttons = button_container
        bot_layout.addWidget(self.bot_label)
        bot_layout.addWidget(button_container)
        self.chat_layout.addLayout(bot_layout)
        self.bot_messages.append((button_container, button_container))
        bot_container.installEventFilter(self)
        button_container.enterEvent = lambda event: self.fade_in_buttons(button_container)
        button_container.leaveEvent = lambda event: self.fade_out_buttons(button_container)
        QTimer.singleShot(50, self.scroll_to_bottom)

    # The Bot Sending a Message
    def bot_reply(self):
        self.typing_timer.stop()
        self.typing_animation_timer.stop()
        if self.typing_label:
            self.typing_label.deleteLater()
            self.typing_label = None
        # Change send button to a stop square
        self.send_button.setText("■")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                font-size: 15px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050; /* Dark grey on hover */
            }
        """)
        # Clicking the square will now stop typing
        self.send_button.clicked.disconnect()
        self.send_button.clicked.connect(self.stop_typing)
        # Translate bot response to the detected language
        translated_response = self.translate_text(self.bot_response, self.detected_language)
        self.current_bot_message = translated_response
        self.bot_message_index = 0
        self.add_bot_message()
        self.typing_effect_timer.start(50)

    '''Typing Animation Stuff'''  # ------------------------------------------------------------------------------------------------------------------------------------------

    # Animates the Bot Typing Effect
    def type_next_character(self):
        if self.bot_message_index < len(self.current_bot_message):
            text = self.current_bot_message[:self.bot_message_index + 1]
            self.bot_label.setText(text + " ●")
            self.bot_message_index += 1
            self.scroll_to_bottom()
            # Occasionally Introduces a Hesitation and Typing Speed
            if random.random() < 0.05:
                self.typing_effect_timer.start(random.randint(200, 700))
            else:
                self.typing_effect_timer.start(random.randint(5, 25))
        else:
            self.typing_effect_timer.stop()
            self.bot_label.setText(self.current_bot_message)
            self.send_button.setText("↑")
            self.send_button.setStyleSheet("""
                QPushButton {
                    background-color: black;
                    color: white;
                    border-radius: 20px;
                    font-size: 20px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #505050; /* Dark grey on hover */
                }
            """)
            self.send_button.clicked.disconnect()
            self.send_button.clicked.connect(self.send_message)

            # Adding the Bot is Thinking Message at the Bottom of the Chat

    def add_typing_indicator(self):
        if self.typing_label is None:  # Prevent multiple labels
            self.typing_label = QLabel("")
            self.typing_label.setAlignment(Qt.AlignLeft)
            self.typing_label.setStyleSheet("color: black; padding-left: 10px;")
            self.chat_layout.addWidget(self.typing_label)
            self.scroll_to_bottom()

    '''Buttons Fading in and Out'''  # -----------------------------------------------------------------------------------------------------------------------------------

    @staticmethod
    def fade_in_buttons(button_container):
        """Smoothly fades in buttons when hovering over a bot message."""
        button_container.setVisible(True)
        animation = QPropertyAnimation(button_container, b"windowOpacity")
        animation.setDuration(200)
        animation.setStartValue(0.0)
        animation.setEndValue(1.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        button_container.setGraphicsEffect(None)  # Ensure it starts fresh
        animation.start()

    @staticmethod
    def fade_out_buttons(button_container):
        """Smoothly fades out buttons when leaving a bot message."""
        animation = QPropertyAnimation(button_container, b"windowOpacity")
        animation.setDuration(200)
        animation.setStartValue(1.0)
        animation.setEndValue(0.0)
        animation.setEasingCurve(QEasingCurve.InOutQuad)
        animation.finished.connect(lambda: button_container.setVisible(False))
        animation.start()

    def eventFilter(self, obj, event):
        """Handles hover effects for bot messages and buttons."""

        for bot_avatar, bot_label in self.bot_messages:
            if obj == bot_label and event.type() == event.Enter:
                if hasattr(bot_label, "button_container"):
                    self.fade_in_buttons(bot_label.button_container)
            elif obj == bot_label and event.type() == event.Leave:
                if hasattr(bot_label, "button_container") and bot_label.button_container != self.latest_bot_buttons:
                    self.fade_out_buttons(bot_label.button_container)

        return super().eventFilter(obj, event)

        """Handles hover effects for buttons (adds grey background when hovered)."""
        if isinstance(obj, QPushButton):
            if event.type() == event.Enter:
                obj.setStyleSheet(self.get_hover_button_style())  # Show hover effect
            elif event.type() == event.Leave:
                obj.setStyleSheet(self.get_default_button_style())  # Remove hover effect
        return super().eventFilter(obj, event)

    @staticmethod
    def hide_buttons_if_not_hovered(button_container):
        """Hides buttons only if the cursor is not over them."""
        if not button_container.underMouse():
            button_container.setVisible(False)

    @staticmethod
    def get_default_button_style():
        """Returns default style for bot buttons with hover effect built-in."""
        return """
            QPushButton {
                background: transparent;
                border: none;
                font-size: 16px;
                border-radius: 15px;
                padding: 5px;
            }
            QPushButton:hover {
                background: rgba(211, 211, 211, 0.5);  /* Light grey (semi-transparent) */
                border-radius: 15px; /* Circular effect */
            }
        """

    @staticmethod
    def get_hover_button_style():
        """Returns hover effect style for bot buttons (faint grey circle)."""
        return """
            QPushButton {
                background: rgba(211, 211, 211, 0.5);  /* Light grey (semi-transparent) */
                border-radius: 15px; /* Circular effect */
                font-size: 16px;
                padding: 5px;
            }
        """

    '''Functions that are Called with Buttons'''  # ------------------------------------------------------------------------------------------------------------------------

    # Copying the Message
    def copy_to_clipboard(self, text):
        clipboard = QApplication.clipboard()
        clipboard.setText(text)
        self.show_tooltip("Copied!", duration=1000)

    # Displaying the Copied Message
    def show_tooltip(self, message, duration=1000):
        tooltip = QLabel(message, self)
        tooltip.setStyleSheet("""
            background-color: black;
            color: white;
            padding: 6px;
            border-radius: 5px;
        """)
        tooltip.setAlignment(Qt.AlignCenter)
        tooltip.setGeometry(self.width() - 120, self.height() - 80, 100, 30)
        tooltip.show()
        QTimer.singleShot(duration, tooltip.hide)

    # Reads the Latest Bot Message Out Loud Via the Speak Button
    @staticmethod
    def speak_message(message):
        engine = pyttsx3.init()
        engine.setProperty("rate", 150)
        engine.setProperty("volume", 1.0)
        engine.say(message)
        engine.runAndWait()

    # Lets User Rate the Last Bot Message Via the Thumbs Up/Down Buttons
    @staticmethod
    def rate_message(bot_label, rating):
        if rating == "up":
            bot_label.setStyleSheet("color: green;")
        elif rating == "down":
            bot_label.setStyleSheet("color: red;")

            # Scrolls Down to the Latest Message Via the Scroll Down Button

    def scroll_to_bottom(self):
        self.scroll_area.verticalScrollBar().setValue(self.scroll_area.verticalScrollBar().maximum())

    # Clearing the Chat Area Via the Clear Chat Button
    '''
    def clear_chat(self):
        try:
            for timer in ["typing_help_timer", "typing_welcome_timer", "typing_timer", "typing_effect_timer",
                          "typing_animation_timer"]:
                if hasattr(self, timer) and getattr(self, timer).isActive():
                    getattr(self, timer).stop()
            if hasattr(self, "scroll_to_bottom_btn"):
                self.scroll_to_bottom_btn.setVisible(False)
            while self.chat_layout.count():
                item = self.chat_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()
            self.user_messages.clear()
            self.bot_messages.clear()
            if hasattr(self, "typing_label") and self.typing_label:
                self.typing_label.deleteLater()
                self.typing_label = None
            if hasattr(self, "latest_edit_button") and self.latest_edit_button:
                self.latest_edit_button.setParent(None)
                self.latest_edit_button = None
            if hasattr(self, "scroll_widget"):
                self.scroll_widget.deleteLater()
                self.scroll_widget = QWidget()
                self.chat_layout = QVBoxLayout(self.scroll_widget)
                self.chat_layout.setAlignment(Qt.AlignTop)
                self.scroll_area.setWidget(self.scroll_widget)
            if hasattr(self, "input_field"):
                self.input_field.clear()
            QTimer.singleShot(100, self.add_welcome_message)

        except Exception as e:
            print(f"⚠ Error in clear_chat: {e}")

            # Updates all User Message Bubbles When Dark/Light Mode is Toggled
    '''

    def update_all_user_message_colors(self):
        for msg_label in self.user_messages:
            self.update_user_message_color(msg_label)

    # Updates the Colour of a User Message Bubble to Match the Current Theme
    def update_user_message_color(self, msg_label):
        user_color = "#555555" if self.dark_mode else "#E3E3E3"
        text_color = "#D1D5DB" if self.dark_mode else "black"
        msg_label.setStyleSheet(f"""
            background-color: {user_color};
            color: {text_color};
            padding: 12px;
            border-top-left-radius: 12px;
            border-top-right-radius: 12px;
            border-bottom-left-radius: 12px;
            border-bottom-right-radius: 2px;  /* Only bottom-right corner is slightly rounded */
        """)

    # Updating Bot Message Color Based on Theme
    def update_bot_message_color(self):
        bot_text_color = "white" if getattr(self, "dark_mode", False) else "black"
        dot_color = "white" if self.dark_mode else "black"  # Ensure correct color update
        font = QFont()
        font.setPointSize(17)
        for bot_avatar, bot_label in self.bot_messages:
            if bot_avatar:
                bot_avatar.setStyleSheet(f"background-color: {dot_color}; border-radius: 8px;")
            if bot_label:
                bot_label.setStyleSheet(f"font-size: 16px; color: {bot_text_color}; padding: 8px;")

    # Switching Between Dark Mode and Light Mode
    def toggle_theme(self):
        # Light Mode
        if getattr(self, "dark_mode", False):
            background_color = "#FFFFFF"
            input_box_color = "#FFFFFF"
            border_color = "light-gray"
            text_color = "black"
            self.dark_mode_button.setStyleSheet("""
            QPushButton {
                background-color: black; 
                color: white; 
                border-radius: 15px;
                border: 1px solid black;
            }
            QPushButton:hover {
                background-color: #505050;
            }
        """)
            self.dark_mode_button.setText("🌙")
            self.dark_mode = False
            # Dark Mode
        else:
            background_color = "#202123"
            input_box_color = "#555555"
            border_color = "#555"
            text_color = "white"
            self.dark_mode_button.setStyleSheet("""
            QPushButton {
                background-color: yellow; 
                color: black; 
                border-radius: 15px;
                border: 1px solid grey;
            }
            QPushButton:hover {
                background-color: #FFFF99;
            }
        """)
            self.dark_mode_button.setText("💡")
            self.dark_mode = True
            # Update UI
        self.setStyleSheet(f"background-color: {background_color}; color: {text_color};")
        self.scroll_area.setStyleSheet(f"background-color: {background_color}; border: none;")
        self.scroll_widget.setStyleSheet(f"background-color: {background_color};")
        self.input_container.setStyleSheet(f"""
            background-color: {input_box_color};  
            border-radius: 20px;
            border: 1px solid {border_color};
        """)
        self.input_field.setStyleSheet(f"""
            background-color: {input_box_color};  
            color: {text_color};
            font-size: 14px;
            border: none;
        """)
        # Update All User Messages
        self.update_all_user_message_colors()
        if self.typing_label:
            self.update_typing_indicator()

    # Stops the Bot from Typing and Leaves the Message As Is
    def stop_typing(self):
        if self.typing_effect_timer.isActive():
            self.typing_effect_timer.stop()
        self.send_button.setText("↑")
        self.send_button.setStyleSheet("""
            QPushButton {
                background-color: black;
                color: white;
                border-radius: 20px;
                font-size: 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #505050; /* Dark grey on hover */
            }
        """)
        self.send_button.clicked.disconnect()
        self.send_button.clicked.connect(self.send_message)

    # Running the App


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ChatApp()
    window.show()
    sys.exit(app.exec_())