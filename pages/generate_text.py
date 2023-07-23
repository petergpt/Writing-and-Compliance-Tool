# pages/generate_text.py
import streamlit as st
from Tone_and_guidance.tone_of_voice_check import ToneOfVoiceCheck
from openai_utils import send_request_to_openai

TONE_OF_VOICE_OPTIONS = {
    'Short and Simple': 'I am a short and simple persona.',
    'Friendly and Informal': 'I am a friendly and informal persona.',
    'Polite and Formal': 'I am a polite and formal persona.'
}

def app():
    st.header('Generate Text')

    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a Tone of Voice', ['Short and Simple', 'Friendly and Informal', 'Polite and Formal'], key='tone')

    if 'tone_input' not in st.session_state:
        st.session_state.tone_input = TONE_OF_VOICE_OPTIONS[tone_option]

    tone_input = st.text_area('What style should be written in?', value=st.session_state.tone_input, max_chars=None, key='tone_input')

    if st.button('Generate Text', key='button1'):
        if text_input and tone_input:
            with st.spinner('Generating text...'):
                messages = [
                    {"role": "system", "content": f"You are ChatGPT, a large language model trained by OpenAI, based on the GPT-4 architecture. You have been instructed to write in a style that is {tone_input}."},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = send_request_to_openai(messages)
                st.session_state.response = response['choices'][0]['message']['content']
                st.session_state.generated_text = st.session_state.response

    st.text_area('Your generated text will appear here', value=st.session_state.get("generated_text", ""), max_chars=None, key=None)
