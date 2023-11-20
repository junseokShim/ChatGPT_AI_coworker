import sys
from src.chatbot_ui.chatbotgui import *

openai.api_key = "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"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatBotGUI()
    ex.show()
    sys.exit(app.exec_())
