import openai
import streamlit as st
from utils import openai_utils



def app():

    st.title('Check Text Compliance with OpenAI')

    text_input = st.text_area('Generated Text', value='', max_chars=None, key=None)
    guidance_input = st.text_area('What does it need to comply with?', value='', max_chars=None, key=None)

    if st.button('Check Compliance'):

        if text_input and guidance_input:

            messages = [
              {"role": "system", "content": "You are a helpful assistant"},
              {"role": "user", "name": "Alice", "content": f"{guidance_input}. Check the following text: {text_input}"},
            ]

            response = openai_utils.send_request_to_openai(messages)

            st.text_area('Assessment Dashboard', value=response,  max_chars=None, key=None)

        else:
            st.warning('Please enter both guidance and text to check')