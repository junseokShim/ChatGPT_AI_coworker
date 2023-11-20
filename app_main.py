import sys
from src.chatbot_ui.chatbotgui import *

openai.api_key = "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"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatBotGUI()
    ex.show()
    sys.exit(app.exec_())
