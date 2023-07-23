import streamlit as st
from multiapp import MultiApp
from pages import generate_text, check_guidance, test_persona

app = MultiApp()

st.sidebar.title('Navigation')

# Add all your application here
app.add_app("Generate Text", generate_text.app)
app.add_app("Check Guidance", check_guidance.app)
app.add_app("Test Persona", test_persona.app)

# The main app
app.run()
