import streamlit as st
import openai
from utils import openai_utils

def app():
    # Initialize session state if it doesn't exist
    if "response" not in st.session_state:
        st.session_state["response"] = ""
    if "generated_text" not in st.session_state:
        st.session_state["generated_text"] = ""

    # Section 1: Generate Text
    st.header('Generate Text')
    text_input = st.text_area('What do you want to write?', value='', max_chars=None, key=None)
    tone_input = st.text_input('What style should be written in?', value='', max_chars=None, key=None)

    if st.button('Generate Text', key='button1'):  # Add a unique key for the button
        if text_input and tone_input:
            messages = [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "name": "Alice", "content": f"{tone_input}. {text_input}"},
            ]
            response = openai_utils.send_request_to_openai(messages)
            st.session_state["response"] = response['choices'][0]['message']['content']
            st.session_state["generated_text"] = st.session_state["response"]  # Store the generated text in the session state

    # Display the generated text (if any)
    st.text_area('Your text will appear here', value=st.session_state["generated_text"], max_chars=None, key=None)

    # Section 2: Check Guidance
    if st.session_state["response"]:
        st.header('Check Guidance')
        guidance_input = st.text_area('What does it need to comply with (from Section 1)?', value='', max_chars=None, key=None)

        if st.button('Check Compliance', key='button2'):  # Add a unique key for the button
            if guidance_input:
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "name": "Alice", "content": f"{guidance_input}. Check the following text: {st.session_state['response']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                result = response['choices'][0]['message']['content']  # Extract the content of the first message
                st.text(result)  # Use st.text() instead of st.markdown()
            else:
                st.warning('Please enter guidance and ensure text is generated in Section 1')
