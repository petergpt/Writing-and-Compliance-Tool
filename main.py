import streamlit as st
import page

def main():
    st.title("OpenAI GPT-4 Text Generation Interface")
    page.generate_text()
    page.check_guidance()
    page.test_persona_perception()

if __name__ == "__main__":
    main()
