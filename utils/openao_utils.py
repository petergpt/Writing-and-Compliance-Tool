import os
import openai

api_key = os.environ["OPENAI_API_KEY"]

openai.api_key = api_key

def send_request_to_openai(messages):
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages,
      temperature=0.8,
      max_tokens=1000  
    )

    return response['choices'][0]['message']['content']