import sys
from src.chatbot_ui.chatbotgui import *

# openai.api_key = "sk-gDo2e82Td99sDz7pQikiT3BlbkFJ7E4 ~~~ FqyQt3UCPp03DZq4B"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatBotGUI()
    ex.show()
    sys.exit(app.exec_())
