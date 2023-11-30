from src.chatbot_ui.worker import *
from src.utils import * # save_to_csv, extract_csv_to_dataframe
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QMessageBox, QInputDialog, QApplication, QWidget, QVBoxLayout, QTextEdit, QLineEdit, QPushButton, QProgressDialog


class ChatBotGUI(QWidget):
    def __init__(self):
        """클래스 생성자: 사용자 인터페이스 초기화 및 메시지 로그 설정."""
        super().__init__()
        self.api_key = None
        self.init_ui()
        self.request_api_key()
        self.message_log = [{
            "role" : "system",
            "content" : 
            '''
            You are a powerful SW development assistant who makes source code. your user will be Korean, so communicate in Korean, and You must perform the roles described below.
            - Debugging Assistance: "ChatGPT-4, please assist me in debugging this Python script. It's supposed to sort a list of numbers but keeps returning an error."
            - Code Review: "Can you review this JavaScript function I wrote for any potential inefficiencies or errors? I'm particularly concerned about the loop structure."
            - Algorithm Explanation: "Explain how the QuickSort algorithm works and suggest scenarios where it's more efficient compared to MergeSort."
            - Best Practices Advice: "Provide some best practices for database design in SQL, focusing on normalization and data integrity."
            - Technology Recommendation: "I need to choose a backend framework for a new web project. Can you compare Django and Flask in terms of scalability and ease of use?"
            - API Integration Guide: "Guide me through integrating the Google Maps API into my existing React application."
            - Troubleshooting Support: "My C++ program is not compiling. It's giving a 'segmentation fault'. What are the common causes for this and how can I fix it?"
            - Learning Path Suggestions: "I'm new to software development. Can you suggest a learning path for mastering full-stack development, starting from the basics?"
            - Code Optimization: "Review this block of C# code for a file-handling operation and suggest optimizations for performance improvement."
            - Project Management Tips: "Provide tips on managing a software development project effectively using Agile methodologies."
            '''
        }]
        self.temperature = 0.1
        # self.function_call = "auto"
        #self.file_path = None


    def request_api_key(self):
        """OpenAI API 키를 요청하는 팝업 생성."""
        key, ok = QInputDialog.getText(self, 'API Key', 'Enter your OpenAI API key:')
        if ok:
            self.api_key = key
            openai.api_key = self.api_key
        else:
            QMessageBox.warning(self, "Warning", "You need to enter an API key to use this application.")
            sys.exit()


    def init_ui(self):
        """GUI 요소 초기화 및 레이아웃 설정."""
        self.setGeometry(100, 100, 1200, 800)
        layout = QVBoxLayout()

        # 좌우 분할을 위한 QHBoxLayout 추가
        h_layout = QHBoxLayout()

         # text_area 영역
        text_area_layout = QVBoxLayout()
        text_area_label = QLabel("Chat Area")
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        text_area_layout.addWidget(text_area_label)
        text_area_layout.addWidget(self.text_area)
        h_layout.addLayout(text_area_layout)

        # code_area 영역
        code_area_layout = QVBoxLayout()
        code_area_label = QLabel("Code Area")
        self.code_area = QTextEdit()
        self.code_area.setReadOnly(True)
        code_area_layout.addWidget(code_area_label)
        code_area_layout.addWidget(self.code_area)
        h_layout.addLayout(code_area_layout)

        layout.addLayout(h_layout)

        self.input_line = QLineEdit()
        self.input_line.returnPressed.connect(self.send_message)
        layout.addWidget(self.input_line)

        self.copy_button = QPushButton('Copy')
        self.copy_button.clicked.connect(self.copy_to_clipboard)
        layout.addWidget(self.copy_button)

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.on_send)
        layout.addWidget(self.send_button)

        self.setLayout(layout)
        self.setWindowTitle('GPT Powered SW Dev assistant')

        self.append_message("Assistant", "Powerful SW Dev Assistant 입니다. 질문해주세요", "white")


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
        self.progress_dialog.close()
        self.message_log.append({"role": "assistant", "content": response})

        # 응답에서 코드 스니펫 추출 및 처리
        if '```' in response:
            start = response.find('```') + 3
            end = response.rfind('```')
            code_snippet = response[start:end].strip()
            self.code_area.setPlainText(code_snippet)  # 코드 영역에 표시
            # 코드를 제외한 나머지 텍스트를 일반 텍스트 영역에 표시
            rest_of_response = response[:start-3] + response[end+3:]
            if rest_of_response.strip():
                self.append_message("Assistant", rest_of_response, "white")  
        else:
            self.append_message("Assistant", response, "white")  # 일반 응답을 텍스트 영역에 표시


    def append_message(self, sender, message, color, is_code=False):
        """메시지를 텍스트 영역에 색상을 적용하여 추가."""
        if is_code:
            self.code_area.setPlainText(message)  # 코드 응답을 코드 영역에 표시
        else:
            colored_message = f"<span style='color:{color};'><pre>{sender}: {message}</pre></span>"
            self.text_area.append(colored_message)  # 일반 응답을 텍스트 영역에 표시
            
            
    def copy_to_clipboard(self):
        """'Copy' 버튼 클릭 시 호출: 코드 영역의 텍스트를 클립보드로 복사."""
        clipboard = QApplication.clipboard()
        clipboard.setText(self.code_area.toPlainText())
