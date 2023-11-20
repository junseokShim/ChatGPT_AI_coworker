import openai

openai.api_key = "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"

# OpenAI 챗봇 모델에 메시지를 보내고 응답하는 하수
def send_message(message_log):
    # OpenAI ChatCompletion API를 사용해 챗봇 응답 얻기
    response = openai.ChatCompletion.create(
        model = "gpt-4",
        messages = message_log,
        temperature = 0.5,
    )

    # 텍스트가 포함된 챗봇의 첫번째 응답 찾기
    # 일부 응답에는 텍스트가 없을 수 있음
    for choice in response.choices:
        if "text" in choice:
            return choice.text

    # 텍스트가 포함된 응답이 없을 경우, 첫번째 응답의 내용 반환
    return response.choices[0].message.content


def main():
    
    # 챗봇에서 받은 메시지로 대화 기록 초기화
    message_log = [
        {
            "role" : "system",
            "content" : "You are a helpful assistant"
        }
    ]

    # 'quit'를 입력할 때까지 실행되는 루프 시작하기
    while True:
        # 터미널에서 사용자 입력받기
        user_input = input("You : ")

        # 사용자가 'quit'를 입력하면 루프를 종료하고 작별 메시지 출력
        if user_input.lower() == "quit":
            print("Goodbye ! ")
            break

        # 사용자의 입력을 대화 기록(message_log)에 추가하기
        message_log.append(
            {
                "role" : "user",
                "content" : user_input
            }
        )

        # 챗봇에게 대화 기록을 보내 응답하기
        response = send_message(message_log=message_log)

        # 대화 기록에 챗봇의 응답을 추가하고 콘솔에 출력하기
        message_log.append(
            {
                "role" : "user",
                "content" : response
            }
        )
        print(f"assistant : {response}")


if __name__=="__main__":
    main()

