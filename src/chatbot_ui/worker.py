import json
import openai
from src.download_youtube_audio import *
from PyQt5.QtCore import pyqtSignal, QThread

# openai.api_key = "sk-gDo2e82Td99sDz7pQikiT3BlbkFJ7E4 ~~~ FqyQt3UCPp03DZq4B"

class Worker(QThread):
    response_signal = pyqtSignal(str)

    def __init__(self, message_log, file_path=None):
        super().__init__()
        self.message_log = message_log
        self.file_path = file_path
        # self.functions = [
        #     {
        #         "name": "download_youtube_audio",
        #         "description": "Download mp3 of songs in the recent CSV file",
        #         "parameters": {
        #             "type": "object",
        #             "properties": {
        #                 "csv_file_path": {
        #                     "type": "string",
        #                     "description": "The recent csv file path",
        #                 },
        #             },
        #             "required": ["csv_file_path"],
        #         },
        #     }
        # ]

    def run(self):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.message_log,
                temperature=0.1,
                # function_call='auto'
            )
            # message = response['choices'][0].message['content']
            message = response.choices[0].message.content
            # if message.get("function_call"):
            #     available_functions = {
            #         "download_youtube_audio": download_youtube_audio,
            #     }
            #     print('Function call detected')

            #     function_name = message["function_call"]["name"]
                
            #     if function_name in available_functions:
            #         function_to_call = available_functions[function_name]

            #         function_args = {"csv_file_path": self.file_path} if self.file_path else json.loads(message["function_call"]["arguments"])
            #         function_response = function_to_call(**function_args)

            #         # 함수 실행 결과를 GPT에게 보내 답을 받아오기 위한 부분
            #         self.message_log.append({
            #             "role": "function",
            #             "name": function_name,
            #             "content": f'{function_response}',
            #         })
            #         response = openai.ChatCompletion.create(
            #             model="gpt-4",
            #             messages=self.message_log,
            #             temperature=0.1
            #         )
            #         message = response.choices[0].message
                
                # Function call, but not in available functions
            
            # Function call is not included at openai response
            #message = message['content']
            self.response_signal.emit(message)
        except Exception as e:
            self.response_signal.emit(f"An error occurred : {e}")
