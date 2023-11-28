import openai
import json

def get_current_weather(location, unit="fahrenheit"):
    '''
	location으로 받은 지역의 날씨를 알려주는 기능
	'''

    weather_info = {
		"location" : location,
		"temperature" : "72",
		"unit" : unit,
		"forecast" : ["sunny", "windy"]
	}

    return json.dumps(weather_info)



def run_conversation():
    # Step 1 : message 뿐만 아닌, 사용할 수 있는 함수에 대한 설명 추가
	
    messages = [{
		"role" : "user",
		"content" : "What's the weather like in Boston ?"
    }]

    functions = [
	    {
			"name" : "get_current_weather",
			"description" : "Get the current weather in a given location",
			"parameters" : {
				"type" : "object",
				"properties" : {
					"location":{
						"type" : "string",
						"description" : "The city and state, e.g. San Francisco, CA",
					},
					"unit" : {
						"type" : "string",
						"enum" : ["celsius", "fahrenheit"]
                        },
					},
					"required" : ["location"],
            },
	    }
    ]

    # functions에는 리스트로 만든 함수 정보를 담아보냄
    # function_call: {"name": "<사용할 함수명>"}과 같은 방식으로 functions에 정의된 함수 중 일부만 지정할 수 있음
	
    response = openai.ChatCompletion.create(
		model = "gpt-4",
		messages = messages,
		functions = functions,
		function_call = "auto", # auto가 기본 설정
    )
    response_message = response["choices"][0]["message"]
    '''
    response_message [OUTPUT]
	{
		"role" : "assistant", 
		"content" : null,
		"function_call" : {
			"name" : "get_current_weather",
			"arguments " "{\n\"location\" : \"Boston\"\n}"
		}
	}
		=> function_call 을 통해 호출하고자 하는 함수(get_current_weather)과
		호출하고자 하는 함수의 인자값(location = "Boston")을 입력
    '''
	
	# Step 2 : GPT의 응답이 function을 실행해야 한다고 판단했는지 확인하기
    if response_message.get("function_call"):
		# Step 3 : 해당 함수 실행하기
        available_functions = {
			"get_current_weather" : get_current_weather,
        } 
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(
	    	location = function_args.get("location"),
			unit = function_args.get("unit"),
		)

	# Step 4 : 함수를 실행한 결과를 GPT에게 보내 답을 받아옴
	# role을 function으로 해둔다면, 
	# name에서 사용한 함수명을, content에는 함수 실행 결과를 넣은 후,
	# GPT에게 이 정보를 담아 API로 넘기면 GPT는 함수의 결과를 예쁜 문장으로 다듬어 다시 우리에게 넘겨줌
    # 
    messages.append(response_message)
    messages.append(
		{
			"role" : "function",
			"name" : function_name,
			"content" : function_response,
		}
	) # 함수 실행결과도 GPT messages에 추가
    second_response = openai.ChatCompletion.create(
    	model = "gpt-4",
		messages = messages,
    ) # 함수 실행 결과를 GPT에 보내 새로운 답변 받아오기

    return second_response



if __name__ == '__main__':
    #openai.api_key = "sk -gDo2e82  Td99sDz7pQikiT3BlbkFJ7E4FqyQt3UCPp03DZq4B"
    print(run_conversation())