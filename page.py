import streamlit as st
import openai_utils
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS
from Tone_and_guidance.guidance import GUIDANCE_OPTIONS
from Tone_and_guidance.questions import QUESTIONS_OPTIONS
from Tone_and_guidance.personas import PERSONAS_OPTIONS
from Tone_and_guidance.content_type_prompts import CONTENT_TYPE_PROMPTS

# Importing our database utilities
from database_utils import store_in_database

def main():
    generate_text()
    check_guidance()
    test_persona_perception()


    # Hidden feature to display database content
if st.button("Display Database Contents"):
    from database_utils import fetch_all_records
    records = fetch_all_records()
    st.write("Trying to fetch records...")  # Debug line
    if records:
        for record in records:
            st.write(record)
    else:
        st.write("No records found in the database.")

def generate_text():
    st.header('✏ Generate Text')

    # Choose content type
    content_type = st.selectbox('Select a content type', list(CONTENT_TYPE_PROMPTS.keys()), key='content_type')
    default_dynamic_part = CONTENT_TYPE_PROMPTS[content_type]

    # Editable dynamic part of the system prompt
    if st.checkbox('Click to edit the system prompt', key='checkbox_prompt_gen'):
        default_dynamic_part = st.text_area('Edit the system prompt if you want', value=default_dynamic_part, key='system_prompt')

    text_input = st.text_area('What do you want to write about?', value='', max_chars=10000)

    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a tone', list(TONE_OF_VOICE_OPTIONS.keys()), key='tone')
    tone_input = st.text_area('What style should be written in?', value=TONE_OF_VOICE_OPTIONS[tone_option], max_chars=None, key='tone_input')

    if st.button('✏ Generate Text', key='button1'):  
        if text_input and tone_input:
            with st.spinner('Generating text...'):
                static_part = "Write the text using the following guidance: " + tone_input
                full_prompt = static_part + " " + default_dynamic_part
                messages = [
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["generated_text"] = response['choices'][0]['message']['content']

                # Store data in the database
                data = {
                    'content_type': content_type,
                    'text_input': text_input,
                    'tone_option': tone_option,
                    'tone_input': tone_input,
                    'generated_text': st.session_state["generated_text"],
                }
                store_in_database(data)

    # Initialize session state if it doesn't exist
    if "generated_text" not in st.session_state:
        st.session_state["generated_text"] = ""
        
    st.text_area('Your text will appear here', value=st.session_state["generated_text"], max_chars=None, key=None)

def check_guidance():
    st.header('✅ Check Guidance')

    st.subheader('Guidance')
    guidance_option = st.selectbox('Select a guidance', list(GUIDANCE_OPTIONS.keys()), key='guidance')
    st.session_state["guidance_input"] = st.text_area(
        'What does it need to comply with?',
        value=GUIDANCE_OPTIONS[guidance_option],
        max_chars=None,
        key='guidance_input_widget')

    # Editable dynamic part of the system prompt
    default_dynamic_part = "You need to do the following: 1) ONLY using the guidance provided, create clear assessment categories based on the guidance provided (never create your own criteria), 2) Analyse the text provided against it, 3) Score the text against each category on a 1-5 scale (1=poor, 5=excellent),4) Provide short commentary against each category, 5) On the very top of your assessment give an overall score and a short assessment of the message versus guidance. Format all of this in a markdown table"
    if st.checkbox('Click to edit the system prompt', key='checkbox_prompt_check'):
        default_dynamic_part = st.text_area('Edit the system prompt if you want',
                                            value=default_dynamic_part,
                                            key='system_prompt_check_guidance')

    if st.button('✅ Check Compliance', key='button2'):
        if st.session_state["guidance_input"]:
            with st.spinner('Checking for compliance...'):
                static_part = "Here is the guidance: " + st.session_state["guidance_input"]
                full_prompt = static_part + " " + default_dynamic_part
                messages = [
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": f"Analyse the following text: {st.session_state['generated_text']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["compliance_result"] = response['choices'][0]['message']['content']

                # Store data in the database
                data = {
                    'guidance_option': guidance_option,
                    'guidance_input': st.session_state["guidance_input"],
                    'compliance_result': st.session_state["compliance_result"],
                }
                store_in_database(data)
        else:
            st.warning('Please enter guidance and ensure text is generated in Section 1')

    if "compliance_result" in st.session_state:
        st.markdown(st.session_state["compliance_result"])

def test_persona_perception():
    st.header('🙋‍♀️ Test Persona Perception')

    st.subheader('Questions')
    questions_option = st.selectbox('Select a set of questions', list(QUESTIONS_OPTIONS.keys()), key='questions')
    st.session_state["questions_input"] = st.text_area(
        'The following questions will be answered by the persona',
        value=QUESTIONS_OPTIONS[questions_option],
        max_chars=None,
        key='questions_input_widget')

    st.subheader('Persona')
    persona_option = st.selectbox('Select a persona', list(PERSONAS_OPTIONS.keys()), key='persona')
    st.session_state["persona_input"] = st.text_area(
        'The following persona will answer the questions',
        value=PERSONAS_OPTIONS[persona_option],
        max_chars=None,
        key='persona_input_widget')

    default_dynamic_part = "You must answer questions provided in line with what the persona would have answered after reading the text that will be provided to you. Format your answers in a markdown table, columns: #, Question, Answer, Commentary. At the end provide an Overall Assessment giving a score of 1-5 (1=poor, 5=excellent) and providing commentary."
    if st.checkbox('Click to edit the system prompt', key='checkbox_prompt_persona'):
        default_dynamic_part = st.text_area('Edit the system prompt if you want', value=default_dynamic_part, key='system_prompt_test_persona')

    if st.button('🙋‍♀️ Test Persona', key='button3'):
        if st.session_state["questions_input"] and st.session_state["persona_input"]:
            with st.spinner('Testing persona perception...'):
                static_part = "You will fully embody a persona " + persona_option
                full_prompt = static_part + " " + default_dynamic_part
                messages = [
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": f"Read the following text: {st.session_state['generated_text']} and answer the following questions: {st.session_state['questions_input']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["persona_result"] = response['choices'][0]['message']['content']

                # Store data in the database
                data = {
                    'questions_option': questions_option,
                    'persona_option': persona_option,
                    'persona_result': st.session_state["persona_result"],
                }
                store_in_database(data)
        else:
            st.warning('Please enter questions and persona, and ensure text is generated and guidance is entered')

    if "persona_result" in st.session_state:
        st.markdown(st.session_state["persona_result"])
    
if __name__ == "__main__":
    main()

