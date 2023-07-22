import streamlit as st
from streamlit.session_state import get_state
from ..utils import openai_utils

def app():
    state = get_state()  # initialize session state

    # Section 1: Generate Text
    st.header('Generate Text')
    state.text_input = st.text_area('What do you want to write?', value=state.text_input if state.text_input else '', max_chars=None, key=None)
    state.tone_input = st.text_input('What style should be written in?', value=state.tone_input if state.tone_input else '', max_chars=None, key=None)

    if st.button('Generate Text'):
        if state.text_input and state.tone_input:
            messages = [
              {"role": "system", "content": "You are a helpful assistant"},
              {"role": "user", "name": "Alice", "content": f"{state.tone_input}. {state.text_input}"},
            ]
            state.response = openai_utils.send_request_to_openai(messages)
            st.text_area('Your text will appear here', value=state.response,  max_chars=None, key=None)

    # Section 2: Check Guidance
    st.header('Check Guidance')
    if state.response:
        state.guidance_input = st.text_area('What does it need to comply with?', value=state.guidance_input if state.guidance_input else '', max_chars=None, key=None)
        if st.button('Check Compliance'):
            messages = [
                {"role": "system", "content": "You are a helpful assistant"},
                {"role": "user", "name": "Alice", "content": f"{state.guidance_input}. Check the following text: {state.response}"},
            ]
            result = openai_utils.send_request_to_openai(messages)
            markdown_table = "| Criteria | Score | Commentary |\n| --- | --- | --- |\n"
            for row in result:
                markdown_table += f"| {row['criteria']} | {row['score']} | {row['commentary']} |\n"
            st.markdown(markdown_table)