import streamlit as st
import page

# Page dictionary only includes single page.py
PAGES = {
    "Text Generation & Compliance Check": page,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page.app()