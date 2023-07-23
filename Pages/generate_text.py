import streamlit as st
import openai
import openai_utils
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS

def app():
    # Initialize session state if it doesn't exist
    if "response" not in st.session_state:
        st.session_state["response"] = ""
    if "generated_text" not in st.session_state:
        st.session_state["generated_text"] = ""
    if "tone_input" not in st.session_state:
        st.session_state["tone_input"] = ""

    # Section 1: Generate Text
    st.header('Generate Text')
    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    # Dropdown for Tone of Voice
    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a tone', list(TONE_OF_VOICE_OPTIONS.keys()), key='tone')
    st.session_state["tone_input"] = st.text_area('What style should be written in?', value=TONE_OF_VOICE_OPTIONS[tone_option], max_chars=None, key='tone_input')

    # Generate text button
    if st.button('Generate Text', key='button1'):  # Add a unique key for the button
        if text_input and st.session_state["tone_input"]:
            with st.spinner('Generating text...'):
                messages = [
                    {"role": "system", "content": f"There are 2 options, 1) You are given instructions to generate a certain bit of text OR 2) You are provided with a bit of text to re-write. Never list both options, only carry out one. For both, please follow this guidance: {st.session_state['tone_input']}."},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["response"] = response['choices'][0]['message']['content']
                st.session_state["generated_text"] = st.session_state["response"]  # Store the generated text in the session state

    # Display the generated text (if any)
    st.text_area('Your text will appear here', value=st.session_state["generated_text"], max_chars=None, key=None)
