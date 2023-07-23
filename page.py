import streamlit as st
import openai
import openai_utils
from Tone_and_guidance.tone_of_voice import TONE_OF_VOICE_OPTIONS
from Tone_and_guidance.guidance import GUIDANCE_OPTIONS

def app():
    # Initialize session state if it doesn't exist
    if "response" not in st.session_state:
        st.session_state["response"] = ""
    if "generated_text" not in st.session_state:
        st.session_state["generated_text"] = ""
    if "guidance_input" not in st.session_state:
        st.session_state["guidance_input"] = ""

    # Section 1: Generate Text
    st.header('Generate Text')
    text_input = st.text_area('What do you want to write?', value='', max_chars=1000)

    # Dropdown for Tone of Voice
    st.subheader('Tone of Voice')
    tone_option = st.selectbox('Select a tone', list(TONE_OF_VOICE_OPTIONS.keys()), key='tone')
    tone_input = st.text_area('What style should be written in?', value=TONE_OF_VOICE_OPTIONS[tone_option], max_chars=None, key='tone_input')

    # Generate text button
    if st.button('Generate Text', key='button1'):  # Add a unique key for the button
        if text_input and tone_input:
            messages = [
                {"role": "system", "content": f"There are 2 options, 1) You are given instructions to generate a certain bit of text OR 2) You are provided with a bit of text to re-write. For both, please follow this guidance: {tone_input}."},
                {"role": "user", "content": f"{text_input}"},
            ]
            response = openai_utils.send_request_to_openai(messages)
            st.session_state["response"] = response['choices'][0]['message']['content']
            st.session_state["generated_text"] = st.session_state["response"]  # Store the generated text in the session state

    # Display the generated text (if any)
    st.text_area('Your text will appear here', value=st.session_state["generated_text"], max_chars=None, key=None)

    # Section 2: Check Guidance
    if st.session_state["response"]:
      st.header('Check Guidance')
    # Dropdown for Guidance
      st.subheader('Guidance')
    guidance_option = st.selectbox('Select a guidance', list(GUIDANCE_OPTIONS.keys()), key='guidance')
    st.session_state["guidance_input"] = st.text_area('What does it need to comply with (from Section 1)?', value=GUIDANCE_OPTIONS[guidance_option], max_chars=None, key='guidance_input_widget')


        if st.button('Check Compliance', key='button2'):  # Add a unique key for the button
            if st.session_state["guidance_input"]:
                messages = [
                    {"role": "system", "content": f"You are provided with the following guidance for what a message should comply with {st.session_state['guidance_input']}. You need to do the following: 1) Create clear assessment categories based on the criteria, 2) Analyse the text provided against it, 3) Score the text against each category on 1-5 scale (1=poor, 5=excellent),4) Provide short commentary against each category, 5) On the very top of your assessment give an overall score and a short assessment of the message versus guidance. Format all of this in a markdown table"},
                    {"role": "user", "content": f"Analyse the following text: {st.session_state['response']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                result = response['choices'][0]['message']['content']  # Extract the content of the first message
                st.markdown(result)
            else:
                st.warning('Please enter guidance and ensure text is generated in Section 1')
