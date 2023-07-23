import streamlit as st
import openai
import openai_utils
from Tone_and_guidance.questions import QUESTIONS_OPTIONS
from Tone_and_guidance.personas import PERSONAS_OPTIONS

def app():
    # Check if needed session state exists
    if "response" not in st.session_state or "tone_input" not in st.session_state or "guidance_input" not in st.session_state:
        st.error("Please generate some text and check guidance first.")
        return

    if "questions_input" not in st.session_state:
        st.session_state["questions_input"] = ""
    if "persona_input" not in st.session_state:
        st.session_state["persona_input"] = ""

    # Section 3: Test Persona Perception
    st.header('Test Persona Perception')

    # Dropdown for Questions
    st.subheader('Questions')
    questions_option = st.selectbox('Select a set of questions', list(QUESTIONS_OPTIONS.keys()), key='questions')
    st.session_state["questions_input"] = st.text_area('The following questions will be answered by the persona', value=QUESTIONS_OPTIONS[questions_option], max_chars=None, key='questions_input_widget')

    # Dropdown for Persona
    st.subheader('Persona')
    persona_option = st.selectbox('Select a persona', list(PERSONAS_OPTIONS.keys()), key='persona')
    st.session_state["persona_input"] = st.text_area('The following persona will answer the questions', value=PERSONAS_OPTIONS[persona_option], max_chars=None, key='persona_input_widget')

    if st.button('Test Persona', key='button3'):  # Add a unique key for the button
        if st.session_state["questions_input"] and st.session_state["persona_input"]:
            with st.spinner('Testing persona perception...'):
                messages = [
                    {"role": "system", "content": f"You will take on the persona of a {persona_option} and answer the following questions based on the text: {st.session_state['questions_input']}."},
                    {"role": "user", "content": f"Here is the text to analyze: {st.session_state['response']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                result = response['choices'][0]['message']['content']  # Extract the content of the first message
                st.markdown(result)
        else:
            st.warning('Please select a set of questions and a persona, and ensure text is generated in Section 1')
