import openai
from PyQt5.QtCore import pyqtSignal, QThread

openai.api_key = "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"

class Worker(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, message_log):
        super().__init__()
        self.message_log = message_log

    def run(self):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.message_log,
                temperature=0.5,
            )
            message = response.choices[0].message['content']
            self.response_signal.emit(message)
        except Exception as e:
            self.response_signal.emit(f"An error occurred: {e}")
