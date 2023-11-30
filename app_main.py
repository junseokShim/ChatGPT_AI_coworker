import sys

from src.download_youtube_audio import *
from src.chatbot_ui.chatbotgui import *

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ChatBotGUI()
    ex.show()
    sys.exit(app.exec_())
