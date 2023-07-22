import streamlit as st
import openai
from utils import openai_utils

def app():
    st.title('OpenAI Text Generation and Compliance Checking')

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
        else:
            st.warning('Please enter both outline and tone of voice')

    # Section 2: Check Compliance
    st.header('Check Guidance')
    guidance_input = st.text_area('What does it need to comply with (from Section 1)?', value='', max_chars=None, key=None)
    
    if st.button('Check Compliance'):
        if response and guidance_input:
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "name": "Alice", "content": f"{guidance_input}. Check the following text: {response}"},
            ]
            result = openai_utils.send_request_to_openai(messages)
            
            # Assuming markdown results are coming from OpenAI API as list of dicts
            # result_data = [{'criteria': 'Criteria 1', 'score': '4/5', 'commentary': 'Good'}]

            # Convert to markdown table format
            markdown_table = "| Criteria | Score | Commentary |\n| --- | --- | --- |\n"
            for row in result:
                markdown_table += f"| {row['criteria']} | {row['score']} | {row['commentary']} |\n"
            
            # Render the markdown table
            st.markdown(markdown_table)
            
        else:
            st.warning('Please enter guidance and ensure text is generated in Section 1')