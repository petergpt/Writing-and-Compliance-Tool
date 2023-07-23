import streamlit as st
import page
from emoji import emojize


def main():
    st.title("Quentin 🤖 - AI-based Text Generator & Checker")
    page.generate_text()
    page.check_guidance()
    page.test_persona_perception()

if __name__ == "__main__":
    main()
