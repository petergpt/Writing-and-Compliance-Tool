import os
import openai
import streamlit as st

OPENAI_API_KEY = os.environ['OPENAI_API_KEY']
openai.api_key = OPENAI_API_KEY

from utils import openai_utils

def app():
   
    st.title('Generate Text with OpenAI')
    text_input = st.text_area('What do you want to write?', value='', max_chars=None, key=None)
    tone_input = st.text_input('What style should be written in?', value='', max_chars=None, key=None)

    if st.button('Generate Text'):
        if text_input and tone_input:
                
            messages = [
              {"role": "system", "content": "You are a helpful assistant"},
              {"role": "user", "name": "Alice", "content": f"{tone_input}. {text_input}"},
            ]
            
            response = openai_utils.send_request_to_openai(messages)

            st.text_area('Your text will appear here', value=response,  max_chars=None, key=None)
        else:
            st.warning('Please enter both outline and tone of voice')