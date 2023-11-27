import json
import openai

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
            - At first, suggest songs to make a playlist based on user's request. The playlist must contain the title, artist, and release year of each song in a list format. You must ask the user if they want to save the playlist like this: "이 플레이리스트를 CSV로 저장하시겠습니까?
            '''
        }]
        self.functions = [
            {
                "name": "save_playlist_as_csv",
                "description": "Saves the given playlist data into a CSV file when the user confirms the playlist.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "playlist_csv": {
                            "type": "string",
                            "description": "A playlist in CSV format separated by ';'. It must contains a header and the release year should follow the 'YYYY' format. The CSV content must starts with a new line. The header of the CSV file must be in English and it should be formatted as follows: 'Title;Artist;Released'.",
                        },
                    },
                    "required": ["playlist_csv"],
                },
            }
        ]
        self.temperature = 0.1
        self.function_call = "auto"

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

        self.update_gui()

    def on_send(self):
        user_input = self.user_entry.text()
        self.user_entry.clear()

        if user_input.lower() == "quit":
            self.close()
            return

        self.send_message()


    def update_gui(self):
        """GUI 업데이트: 챗봇 응답을 텍스트 영역에 추가."""
        # print(f" Debug : {response}")
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=self.message_log,
            temperature=self.temperature,
            functions=self.functions,
            function_call=self.function_call
        )

        response_message = response["choices"][0]["message"]
        if response_message.get("function_call"):
            available_functions = {
                "save_playlist_as_csv": save_playlist_as_csv,
            }
            function_name = response_message["function_call"]["name"]
            function_to_call = available_functions[function_name]
            function_args = json.loads(response_message["function_call"]["arguments"])

            function_response = function_to_call(**function_args)

            # 함수 실행 결과를 GPT에게 보내 답을 받아오기 위한 부분
            self.message_log.append({
                "role": "function",
                "name": function_name,
                "content": function_response,
            })
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.message_log,
                temperature=0.1
            )

        response = response["choices"][0]["message"]["content"]


        self.progress_dialog.close()
        self.append_message("Assistant", response, "white")  # 빨간색으로 챗봇 메시지 추가


    def append_message(self, sender, message, color):
        """메시지를 텍스트 영역에 색상을 적용하여 추가."""
        # HTML <pre> 태그를 사용하여 공백과 줄바꿈을 유지
        colored_message = f"<span style='color:{color};'><pre>{sender}: {message}</pre></span>"
        self.text_area.append(colored_message)
