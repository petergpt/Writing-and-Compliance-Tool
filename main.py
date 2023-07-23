import streamlit as st
import generate_text, check_guidance, test_persona

PAGES = {
    "Generate Text": generate_text,
    "Check Guidance": check_guidance,
    "Test Persona Perception": test_persona
}

def main():
    st.sidebar.title("Navigation")
    selection = st.sidebar.radio("Go to", list(PAGES.keys()))

    page = PAGES[selection]

    with st.spinner(f"Loading {selection} ..."):
        page.app()

if __name__ == "__main__":
    main()
