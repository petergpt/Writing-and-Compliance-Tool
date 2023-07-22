import streamlit as st
import openai
from utils import openai_utils

def app():
    st.title('Text Generation and Compliance Checking')

    # Section 1: Generate Text
    st.header('Generate Text')
    text_input = st.text_area('What do you want to write?', value='', max_chars=None, key=None)
    tone_input = st.text_input('What style should be written in?', value='', max_chars=None, key=None)
    
    if st.button('Generate Text'):
        if text_input and tone_input:
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "name": "Alice", "content": f"{tone_input}. {text_input}"},
            ]
            response = openai_utils.send_request_to_openai(messages)
            st.text_area('Your text will appear here', value=response, max_chars=None, key=None)
            
            # "Check Guidance" button
            if st.button('Check Guidance'):
                guidance_input = st.text_area('What does it need to comply with?', value='', max_chars=None, key=None)
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "name": "Alice", "content": f"{guidance_input}. Check the following text: {response}"},
                ]
                result = openai_utils.send_request_to_openai(messages)
                
                # Assuming markdown results are coming from OpenAI API
                markdown_table = "| Criteria | Score | Commentary |\n| --- | --- | --- |\n"
                for row in result:
                    markdown_table += f"| {row['criteria']} | {row['score']} | {row['commentary']} |\n"
                
                # Render the markdown table
                st.markdown(markdown_table)
    
        else:
            st.warning('Please enter both outline and tone of voice')