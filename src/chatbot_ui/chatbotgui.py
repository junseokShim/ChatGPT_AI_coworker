from src.chatbot_ui.worker import *
from src.utils import * # save_to_csv, extract_csv_to_dataframe
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QProgressDialog


class ChatBotGUI(QWidget):
    def __init__(self):
        """클래스 생성자: 사용자 인터페이스 초기화 및 메시지 로그 설정."""
        super().__init__()
        self.init_ui()
        self.message_log = [{
            "role": "system",
            "content":
                '''
                You are a DJ assistant who creates playlists. Your user will be Korean, so communicate in Korean, but you must not translate artists' names and song titles into Korean.
                    - When you show a playlist, it must contains the title, artist, and release year of each song in a list format. You must ask the user if they want to save the playlist like this: "이 플레이리스트를 CSV로 저장하시겠습니까?"
                    - If they want to save the playlist into CSV, show the playlist with a header in CSV format, separated by ';' and the release year format should be 'YYYY'. The CSV format must start with a new line. The header of the CSV file must be in English and it should be formatted as follows: 'Title;Artist;Released'.
                '''
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
        self.send_button.clicked.connect(self.on_send)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle('GPT Powered DJ')


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

    def on_send(self):
        user_input = self.user_entry.text()
        self.user_entry.clear()

        if user_input.lower() == "quit":
            self.close()
            return

        # 여기서 생각 중... 팝업과 같은 처리를 하고, 메시지 로그 처리 및 응답 처리를 수행해야 함
        # 예: response = send_message(user_input)
        # ...

        # 예시 응답을 채팅 창에 표시
        self.send_message()


    def update_gui(self, response):
        """GUI 업데이트: 챗봇 응답을 텍스트 영역에 추가."""

        df = extract_csv_to_dataframe(response)
        self.progress_dialog.close()

        if df is not None:
            file_save_result = save_to_csv(df)
            print(file_save_result)
            if file_save_result == '저장을 취소했습니다.':
                response = file_save_result
            else:
                response = file_save_result + '\n' + response

        self.message_log.append({
            "role" : "assistant",
            "content" : response
        })

        self.append_message("Assistant", response, "white")  # 빨간색으로 챗봇 메시지 추가


    def append_message(self, sender, message, color):
        """메시지를 텍스트 영역에 색상을 적용하여 추가."""
        # HTML <pre> 태그를 사용하여 공백과 줄바꿈을 유지
        colored_message = f"<span style='color:{color};'><pre>{sender}: {message}</pre></span>"
        self.text_area.append(colored_message)
