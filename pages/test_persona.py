# pages/test_persona.py
import streamlit as st
from Tone_and_guidance.guidance_check import GuidanceCheck
from openai_utils import send_request_to_openai

def app():
    st.header('Test Persona')

    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    st.subheader('Persona Check')
    persona_option = st.selectbox('Select a Persona', ['Short and Simple', 'Friendly and Informal', 'Polite and Formal'], key='persona')

    # Change here: initialize persona_input from session state if it exists
    persona_input = st.text_area('What persona should be followed?', value=st.session_state.get("persona_input", ""), max_chars=None, key='persona_input')

    if st.button('Test Persona', key='button3'):
        if text_input and persona_input:
            with st.spinner('Testing persona...'):
                messages = [
                    {"role": "system", "content": f"You are reviewing a document for its adherence to the persona: {persona_input}."},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = send_request_to_openai(messages)
                st.session_state["response"] = response['choices'][0]['message']['content']
                st.session_state["persona_text"] = st.session_state["response"]

    st.text_area('Your persona result will appear here', value=st.session_state.get("persona_text", ""), max_chars=None, key=None)
