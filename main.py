import streamlit as st
import page
from database_utils import setup_database

def main():
    setup_database()  # Initialize the database
    st.title("Quentin 🤖 - AI-based Text Generator & Checker")
    page.main()

if __name__ == "__main__":
    main()
