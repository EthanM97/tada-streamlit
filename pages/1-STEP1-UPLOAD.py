import streamlit as st
import pandas as pd
from modules.shared_functions import *

# Setup the page
st.set_page_config(page_title="Upload Your Data", page_icon="📈", layout="wide")
st.header("Upload Your Data")
st.write("Upload your data to get started. You can re-upload to replace the current data at any time. When you are done, click Next to move to the next step.")

# Sidebar setup
st.sidebar.header("Rules for Data Upload")
st.sidebar.write("1. Only CSV, XLSX, and XLSM files are allowed.")
st.sidebar.write("The maximum file size allowed is 200MB.")
st.sidebar.write("*Disclaimer - Tada does not store your data. Once you close the app, your data is deleted. Tada is also not responsible for the security of your data*")
st.sidebar.divider()

# File uploader with callback
def handle_file_upload():
    uploaded_file = st.session_state['uploaded_file']
    if uploaded_file is not None:
        if uploaded_file.size > 200 * 1024 * 1024:  # 200 MB limit
            st.error("File size exceeds the 200MB limit")
            return

        try:
            if uploaded_file.type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" or uploaded_file.type == "application/vnd.ms-excel.sheet.macroEnabled.12":
                df = pd.read_excel(uploaded_file)
            else:
                df = pd.read_csv(uploaded_file)
            st.session_state['main_df'] = df
            st.success("File uploaded successfully!")
        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")

st.file_uploader("Choose a CSV, XLSX, or XLSM file", type=["csv", "xlsx", "xlsm"],
                 on_change=handle_file_upload, key="uploaded_file")

# Display the current data if it exists
if 'main_df' in st.session_state and not st.session_state['main_df'].empty:
    st.write("Current data loaded:")
    st.dataframe(st.session_state['main_df'])

# Navigation button
col1, col2 = st.columns([18, 1])
with col2:
    if st.button("Next", key="next_button", help="Move to next step"):
        if 'main_df' in st.session_state and not st.session_state['main_df'].empty:
            switch_page("STEP1-Preprocessing")  # Function to navigate to the next step
