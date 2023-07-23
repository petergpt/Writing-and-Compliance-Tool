# pages/check_guidance.py
import streamlit as st
from Tone_and_guidance.guidance_check import GuidanceCheck
from openai_utils import send_request_to_openai

def app():
    st.header('Check Guidance')

    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    st.subheader('Guidance Check')
    guidance_option = st.selectbox('Select a Guidance', ['Short and Simple', 'Friendly and Informal', 'Polite and Formal'], key='guidance')

    # Change here: initialize guidance_input from session state if it exists
    guidance_input = st.text_area('What guidance should be followed?', value=st.session_state.get("guidance_input", ""), max_chars=None, key='guidance_input')

    if st.button('Check Guidance', key='button2'):
        if text_input and guidance_input:
            with st.spinner('Checking guidance...'):
                messages = [
                    {"role": "system", "content": f"You are reviewing a document for its adherence to the guidance: {guidance_input}."},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = send_request_to_openai(messages)
                st.session_state["response"] = response['choices'][0]['message']['content']
                st.session_state["guidance_text"] = st.session_state["response"]

    st.text_area('Your guidance result will appear here', value=st.session_state.get("guidance_text", ""), max_chars=None, key=None)
