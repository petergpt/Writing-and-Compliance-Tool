import streamlit as st
import openai
import openai_utils
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS
from Tone_and_guidance.guidance import GUIDANCE_OPTIONS
from Tone_and_guidance.questions import QUESTIONS_OPTIONS
from Tone_and_guidance.personas import PERSONAS_OPTIONS
from Tone_and_guidance.content_type_prompts import CONTENT_TYPE_PROMPTS

def main():
    st.sidebar.title('Navigation')
    selection = st.sidebar.radio("Go to", ['Generate Text', 'Check Guidance', 'Test Persona Perception'])

    if selection == 'Generate Text':
        generate_text()
    elif selection == 'Check Guidance':
        check_guidance()
    elif selection == 'Test Persona Perception':
        test_persona_perception()

def generate_text():
    st.header('Generate Text')

    # Choose content type
    content_type = st.selectbox('Select a content type', list(CONTENT_TYPE_PROMPTS.keys()), key='content_type')
    prompt = CONTENT_TYPE_PROMPTS[content_type]

    # Editable system prompt
    if st.checkbox('Click to edit the system prompt'):
        prompt = st.text_area('Edit the system prompt if you want', value=prompt, key='system_prompt')

    text_input = st.text_area('What do you want to write?', value='', max_chars=10000)

    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a tone', list(TONE_OF_VOICE_OPTIONS.keys()), key='tone')
    tone_input = st.text_area('What style should be written in?', value=TONE_OF_VOICE_OPTIONS[tone_option], max_chars=None, key='tone_input')

    if st.button('Generate Text', key='button1'):  
        if text_input and tone_input:
            with st.spinner('Generating text...'):
                messages = [
                    {"role": "system", "content": f"{prompt}"},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["generated_text"] = response['choices'][0]['message']['content']

    # Initialize session state if it doesn't exist
    if "generated_text" not in st.session_state:
        st.session_state["generated_text"] = ""
        
    st.text_area('Your text will appear here', value=st.session_state["generated_text"], max_chars=None, key=None)

def check_guidance():
    st.header('Check Guidance')

    # Editable system prompt
    default_prompt = "You are provided with the following guidance for what a message should comply..."
    if st.checkbox('Click to edit the system prompt'):
        default_prompt = st.text_area('Edit the system prompt if you want', value=default_prompt, key='system_prompt_check_guidance')

    st.subheader('Guidance')
    guidance_option = st.selectbox('Select a guidance', list(GUIDANCE_OPTIONS.keys()), key='guidance')
    st.session_state["guidance_input"] = st.text_area('What does it need to comply with (from Section 1)?', value=GUIDANCE_OPTIONS[guidance_option], max_chars=None, key='guidance_input_widget')

    if st.button('Check Compliance', key='button2'):  
        if st.session_state["guidance_input"]:
            with st.spinner('Checking for compliance...'):
                messages = [
                    {"role": "system", "content": f"{default_prompt}"},
                    {"role": "user", "content": f"Analyse the following text: {st.session_state['generated_text']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["result"] = response['choices'][0]['message']['content']  # Store the content in the session state

        else:
            st.warning('Please enter guidance and ensure text is generated in Section 1')

        if "result" in st.session_state:
            st.markdown(st.session_state["result"])  # Display the stored result

def test_persona_perception():
    st.header('Test Persona Perception')

    # Editable system prompt
    default_prompt = "You will fully embody a persona of a {persona_option} and answer the following questions based on the text..."
    if st.checkbox('Click to edit the system prompt'):
        default_prompt = st.text_area('Edit the system prompt if you want', value=default_prompt, key='system_prompt_test_persona')

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
                    {"role": "system", "content": f"{default_prompt}"},
                    {"role": "user", "content": f"Read the following text: {st.session_state['generated_text']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.markdown(response['choices'][0]['message']['content'])
        else:
            st.warning('Please enter questions and persona, and ensure text is generated and guidance is entered')

if __name__ == "__main__":
    main()
