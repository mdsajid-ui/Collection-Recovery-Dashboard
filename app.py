import streamlit as st
import streamlit.components.v1 as components
import os

st.set_page_config(page_title="Collection & Recovery Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Read the HTML file
html_file_path = os.path.join(os.path.dirname(__file__), "index.html")

try:
    with open(html_file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
        
    # Render the HTML using Streamlit components
    # We use a large height and enable scrolling so the dashboard fits well
    components.html(html_content, height=1200, scrolling=True)

except FileNotFoundError:
    st.error(f"Could not find {html_file_path}. Please make sure index.html is in the same folder as app.py")
