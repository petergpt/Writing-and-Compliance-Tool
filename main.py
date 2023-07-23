import streamlit as st
from multiapp import MultiApp
from generate_text import app as generate_text_app
from check_guidance import app as check_guidance_app
from test_persona import app as test_persona_app

app = MultiApp()

app.add_app("Generate Text", generate_text_app)
app.add_app("Check Guidance", check_guidance_app)
app.add_app("Test Persona", test_persona_app)

app.run()
