import streamlit as st

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):
        """Adds a new function to the application."""
        self.apps.append({"title": title, "function": func})

    def run(self):
        # dropdown to select the app to run
        app = st.sidebar.selectbox(
            'Navigate',
            self.apps,
            format_func=lambda app: app['title'])

        # run the app
        app['function']()
