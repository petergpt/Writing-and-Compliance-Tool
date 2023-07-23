# pages/generate_text.py
import streamlit as st
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS
from openai_utils import send_request_to_openai

def app():
    st.header('Generate Text')
    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a tone', list(TONE_OF_VOICE_OPTIONS.keys()), key='tone')

    if st.button('Generate Text', key='button1'):
        if text_input:
            with st.spinner('Generating text...'):
                messages = [
                    {"role": "system", "content": f"You have two options: 1) You are given instructions to generate a certain bit of text OR 2) You are provided with a bit of text to re-write. Never list both options, only carry out one. For both, please follow this guidance: {TONE_OF_VOICE_OPTIONS[tone_option]}."},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = send_request_to_openai(messages)
                st.session_state["response"] = response['choices'][0]['message']['content']
                st.session_state["generated_text"] = st.session_state["response"]
                
    tone_input = st.text_area('What style should be written in?', value=st.session_state.get("tone_input", TONE_OF_VOICE_OPTIONS[tone_option]), max_chars=None, key='tone_input')

    st.text_area('Your text will appear here', value=st.session_state.get("generated_text", ""), max_chars=None, key=None)
