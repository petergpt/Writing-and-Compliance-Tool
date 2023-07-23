import os
import openai

openai.organization = "org-RgaR5omwSOHKfgH8FjtxRDis"

#OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
#openai.api_key = "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"

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
