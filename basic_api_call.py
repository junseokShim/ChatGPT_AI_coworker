import openai

openai.api_key = "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"

def ask_to_gpt_35_turbo(user_input):  
    response = openai.ChatCompletion.create(
        model="gpt-4",
        top_p=0.1,
        temperature=0.1,
        messages=[
            {"role": "system", "content":"You are the mirror of Snow White. You must pretend like the mirror of the story."},  
            {"role":"user", "content": user_input}
        ]  
    )  
    
    return response.choices[0].message.content 

users_request = '''
거울아! 거울아! 세상에서 누가 제일 예쁘니?
'''
r = ask_to_gpt_35_turbo(users_request)
print(r)