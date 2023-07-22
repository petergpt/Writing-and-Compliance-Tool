
import streamlit as st
import openai
from utils import openai_utils

def app():
    # Initialize session state if it doesn't exist
    if "response" not in st.session_state:
        st.session_state["response"] = ""
    
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
            st.session_state["response"] = openai_utils.send_request_to_openai(messages)
            st.text_area('Your text will appear here', value=st.session_state["response"], max_chars=None, key=None)

    # Section 2: Check Guidance
    if st.session_state["response"]:
        st.header('Check Guidance')
        guidance_input = st.text_area('What does it need to comply with (from Section 1)?', value='', max_chars=None, key=None)
       
        if st.button('Check Compliance'):
            if guidance_input:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant"},
                    {"role": "user", "name": "Alice", "content": f"{guidance_input}. Check the following text: {st.session_state['response']}"},
                ]
                result = openai_utils.send_request_to_openai(messages)
              
                # Assuming markdown results are coming from OpenAI API
                markdown_table = "| Criteria | Score | Commentary |\n| --- | --- | --- |\n"
                for row in result:
                    markdown_table += f"| {row['criteria']} | {row['score']} | {row['commentary']} |\n"
                
                # Render the markdown table
                st.markdown(markdown_table)
            else:
                st.warning('Please enter guidance and ensure text is generated in Section 1')