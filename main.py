import streamlit as st
from app import home_page, generate_text, check_guidance

PAGES = {
    "Home": home_page,
    "Section 1: Generate Text": generate_text,
    "Section 2: Check Guidance": check_guidance
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()
