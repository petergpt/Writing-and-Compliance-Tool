import streamlit as st
import openai
import openai_utils
from Tone_and_guidance.guidance import GUIDANCE_OPTIONS

def app():
    # Check if needed session state exists
    if "response" not in st.session_state or "tone_input" not in st.session_state:
        st.error("Please generate some text first.")
        return

    if "guidance_input" not in st.session_state:
        st.session_state["guidance_input"] = ""

    # Section 2: Check Guidance
    st.header('Check Guidance')
    # Dropdown for Guidance
    st.subheader('Guidance')
    guidance_option = st.selectbox('Select a guidance', list(GUIDANCE_OPTIONS.keys()), key='guidance')
    st.session_state["guidance_input"] = st.text_area('What does it need to comply with (from Section 1)?', value=GUIDANCE_OPTIONS[guidance_option], max_chars=None, key='guidance_input_widget')

    if st.button('Check Compliance', key='button2'):  # Add a unique key for the button
        if st.session_state["guidance_input"]:
            with st.spinner('Checking for compliance...'):
                messages = [
                    {"role": "system", "content": f"You are provided with the following guidance for what a message should comply with {st.session_state['guidance_input']}. You need to do the following: 1) Create clear assessment categories based on the criteria, 2) Analyse the text provided against it, 3) Score the text against each category on 1-5 scale (1=poor, 5=excellent),4) Provide short commentary against each category, 5) On the very top of your assessment give an overall score and a short assessment of the message versus guidance. Format all of this in a markdown table"},
                    {"role": "user", "content": f"Analyse the following text: {st.session_state['response']}"},
                ]
                response = openai_utils.send_request_to_openai(messages)
                result = response['choices'][0]['message']['content']  # Extract the content of the first message
                st.markdown(result)
        else:
            st.warning('Please enter guidance and ensure text is generated in Section 1')
