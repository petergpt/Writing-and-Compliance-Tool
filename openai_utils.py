import os
import openai

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

def send_request_to_openai(messages):
    
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages,
      temperature=0.8,
      max_tokens=2000  
    )

    return response
