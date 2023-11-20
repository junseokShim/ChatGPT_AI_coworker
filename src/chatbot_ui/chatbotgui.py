from src.chatbot_ui.worker import *
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QProgressDialog


class ChatBotGUI(QWidget):
    def __init__(self):
        """클래스 생성자: 사용자 인터페이스 초기화 및 메시지 로그 설정."""
        super().__init__()
        self.init_ui()
        self.message_log = [{
            "role": "system",
            "content": "You are a helpful assistant"
        }]


    def init_ui(self):
        """GUI 요소 초기화 및 레이아웃 설정."""
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()

        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_line)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle('ChatBot')


    def send_message(self):
        """'Send' 버튼 클릭 시 호출: 사용자 입력 처리 및 챗봇 응답 요청."""
        user_input = self.input_line.text()
        self.append_message("You", user_input, "yellow")  # 파란색으로 사용자 메시지 추가
        self.input_line.clear()

        self.message_log.append({
            "role": "user",
            "content": user_input
        })

        self.progress_dialog = QProgressDialog("Getting response...", "Cancel", 0, 0, self)
        self.progress_dialog.setModal(True)
        self.progress_dialog.show()

        self.worker = Worker(self.message_log)
        self.worker.response_signal.connect(self.update_gui)
        self.worker.start()


    def update_gui(self, response):
        """GUI 업데이트: 챗봇 응답을 텍스트 영역에 추가."""
        self.append_message("Assistant", response, "white")  # 빨간색으로 챗봇 메시지 추가
        self.progress_dialog.close()
        

    def append_message(self, sender, message, color):
        """메시지를 텍스트 영역에 색상을 적용하여 추가."""
        colored_message = f"<span style='color:{color};'>{sender}: {message}</span>"
        self.text_area.append(colored_message)
