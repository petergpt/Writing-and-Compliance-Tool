import streamlit as st
import openai
import openai_utils
from emoji import emojize
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS
from Tone_and_guidance.guidance import GUIDANCE_OPTIONS
from Tone_and_guidance.questions import QUESTIONS_OPTIONS
from Tone_and_guidance.personas import PERSONAS_OPTIONS
from Tone_and_guidance.content_type_prompts import CONTENT_TYPE_PROMPTS

def main():
    generate_text()
    check_guidance()
    test_persona_perception()

def generate_text():
    st.header('✏ Generate Text')

    # Choose content type
    content_type = st.selectbox('Select a content type', list(CONTENT_TYPE_PROMPTS.keys()), key='content_type')
    default_dynamic_part = CONTENT_TYPE_PROMPTS[content_type]  # This is the dynamic part of the prompt now

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
                # Include the tone_input into the static part
                static_part = "Write the text using the following guidance: " + tone_input
                # Combine the static part and the dynamic part into the full prompt
                full_prompt = static_part + " " + default_dynamic_part
                messages = [
                    {"role": "system", "content": full_prompt},
                    {"role": "user", "content": f"{text_input}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["generated_text"] = response['choices'][0]['message']['content']

    # Display either the generated text or the edited version
    edited_or_generated_text = st.text_area('Your text will appear here', value=st.session_state.get("generated_text", ""), max_chars=None, key=None)
    st.session_state["generated_text"] = edited_or_generated_text

def check_guidance():
    st.header('✅ Check Guidance')

    st.subheader('Guidance')
    guidance_option = st.selectbox('Select a guidance', list(GUIDANCE_OPTIONS.keys()), key='guidance')
    st.session_state["guidance_input"] = st.text_area(
        'What does it need to comply with?',
        value=GUIDANCE_OPTIONS[guidance_option],
        max_chars=None,
        key='guidance_input_widget')

    if st.button('✅ Check Compliance', key='button2'):
        # Step 1: Create the framework
        static_part_framework = "You need to do the following: ONLY using the guidance provided, create clear assessment categories based on the guidance provided (never create your own criteria)."
        messages = [
            {"role": "system", "content": static_part_framework},
            {"role": "user", "content": f"Here is the guidance: {st.session_state['guidance_input']}"},
        ]
        response = openai_utils.send_request_to_openai(messages)
        framework = response['choices'][0]['message']['content']

        # Step 2: Analyze the text using the generated framework
        if st.session_state["guidance_input"] and "generated_text" in st.session_state:
            static_part_analysis = f"""1) Take the framework provided ({framework}), 2) Analyse the text provided against it, 3) Score the text against each category on a 1-5 scale (1=poor, 5=excellent),4) Provide short commentary against each category, 5) On the very top of your assessment give an overall score and a short assessment of the message versus guidance. Format all of this in a markdown table."""
            messages = [
                {"role": "system", "content": static_part_analysis},
                {"role": "user", "content": f"Analyse the following text using the framework provided: {st.session_state['generated_text']}"},
            ]
            with st.spinner('Checking for compliance...'):
                response = openai_utils.send_request_to_openai(messages)
                st.session_state["compliance_result"] = response['choices'][0]['message']['content']  # Store the content in the session state
        else:
            st.warning('Please enter guidance and ensure text is generated in Section 1')

    if "compliance_result" in st.session_state:
        st.markdown(st.session_state["compliance_result"])  # Display the stored result

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
                st.session_state["persona_result"] = response['choices'][0]['message']['content']  # Store the content in the session state
        else:
            st.warning('Please enter questions and persona, and ensure text is generated and guidance is entered')

    if "persona_result" in st.session_state:
        st.markdown(st.session_state["persona_result"])  # Display the stored result

if __name__ == "__main__":
  main()
