import streamlit as st
import openai
import openai_utils
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS
from Tone_and_guidance.guidance import GUIDANCE_OPTIONS
from Tone_and_guidance.questions import QUESTIONS_OPTIONS
from Tone_and_guidance.personas import PERSONAS_OPTIONS

def generate_text():
    st.header('Generate Text')

    # Initialize session state if it doesn't exist
    if "generated_text" not in st.session_state:
        st.session_state["generated_text"] = ""

    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a tone', list(TONE_OF_VOICE_OPTIONS.keys()), key='tone')
    tone_input = st.text_area('What style should be written in?', value=TONE_OF_VOICE_OPTIONS[tone_option], max_chars=None, key='tone_input')

    if st.button('Generate Text', key='button1'):  
        if text_input and tone_input:
            with st.spinner('Generating text...'):
                messages = [
                    {"role": "system", "content": f"There are 2 options, 1) You are given instructions to generate a certain bit of text OR 2) You are provided with a bit of text to re-write. Never list both options, only carry out one. For both, please follow this guidance: {tone_input}."},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["generated_text"] = response['choices'][0]['message']['content']

    st.text_area('Your text will appear here', value=st.session_state["generated_text"], max_chars=None, key=None)


def check_guidance():
    if "generated_text" in st.session_state and st.session_state["generated_text"]:
        st.header('Check Guidance')

        st.subheader('Guidance')
        guidance_option = st.selectbox('Select a guidance', list(GUIDANCE_OPTIONS.keys()), key='guidance')
        st.session_state["guidance_input"] = st.text_area('What does it need to comply with (from Section 1)?', value=GUIDANCE_OPTIONS[guidance_option], max_chars=None, key='guidance_input_widget')

        if st.button('Check Compliance', key='button2'):  
            if st.session_state["guidance_input"]:
                with st.spinner('Checking for compliance...'):
                    messages = [
                        {"role": "system", "content": f"You are provided with the following guidance for what a message should comply with {st.session_state['guidance_input']}. You need to do the following: 1) Create clear assessment categories based on the criteria, 2) Analyse the text provided against it, 3) Score the text against each category on a 1-5 scale (1=poor, 5=excellent),4) Provide short commentary against each category, 5) On the very top of your assessment give an overall score and a short assessment of the message versus guidance. Format all of this in a markdown table"},
                        {"role": "user", "content": f"Analyse the following text: {st.session_state['generated_text']}"},
                    ]
                    response = openai_utils.send_request_to_openai(messages)
                    result = response['choices'][0]['message']['content']  # Extract the content of the first message
                    st.markdown(result)
            else:
                st.warning('Please enter guidance and ensure text is generated in Section 1')
    else:
        st.warning('Please generate text first')


def test_persona_perception():
    if "generated_text" in st.session_state and st.session_state["generated_text"] and "guidance_input" in st.session_state and st.session_state["guidance_input"]:
        st.header('Test Persona Perception')

        st.subheader('Questions')
        questions_option = st.selectbox('Select a set of questions', list(QUESTIONS_OPTIONS.keys()), key='questions')
        st.session_state["questions_input"] = st.text_area('The following questions will be answered by the persona', value=QUESTIONS_OPTIONS[questions_option], max_chars=None, key='questions_input_widget')

        st.subheader('Persona')
        persona_option = st.selectbox('Select a persona', list(PERSONAS_OPTIONS.keys()), key='persona')
        st.session_state["persona_input"] = st.text_area('The following persona will answer the questions', value=PERSONAS_OPTIONS[persona_option], max_chars=None, key='persona_input_widget')

        if st.button('Test Persona', key='button3'):  
            if st.session_state["questions_input"] and st.session_state["persona_input"]:
                with st.spinner('Testing persona perception...'):
                    messages = [
                        {"role": "system", "content": f"You will take on the persona of a {persona_option} and answer the following questions based on the text: {st.session_state['questions_input']}."},
                        {"role": "user", "content": f"Read the following text: {st.session_state['generated_text']}"},
                    ]
                    response = openai_utils.send_request_to_openai(messages)
                    st.markdown(response['choices'][0]['message']['content'])
            else:
                st.warning('Please enter questions and persona, and ensure text is generated and guidance is entered')
    else:
        st.warning('Please generate text and check guidance first')
