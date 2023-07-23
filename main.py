import streamlit as st
import app_generate_text
import app_check_guidance
import app_test_persona


def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", ['Generate Text', 'Check Guidance', 'Test Persona'])

    if selection == 'Generate Text':
        app_generate_text.app()
    elif selection == 'Check Guidance':
        app_check_guidance.app()
    elif selection == 'Test Persona':
        app_test_persona.app()


if __name__ == "__main__":
    main()
