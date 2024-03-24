import streamlit as st
import pandas as pd
from modules.shared_functions import *

#-------------------------function for file upload------------------------------#
        
def secure_file_uploader():
    """
    Creates a secure file uploader for Streamlit apps.
    Allows only CSV, XLSX, and XLSM files with a size under 200MB.

    Returns:
        The uploaded file as a Pandas DataFrame, or None if no valid file was uploaded.
    """

    uploaded_file = st.file_uploader(
        "Choose a CSV, XLSX, or XLSM file",
        type=["csv", "xlsx", "xlsm"],
        help="Only CSV, XLSX and XLSM files are allowed"
    )

    if uploaded_file is not None:
        # Check file size
        if uploaded_file.size > 200 * 1024 * 1024:  # 200 MB limit
            st.error("File size exceeds the 200MB limit")
            return None

        # Try reading the file as a DataFrame
        try:
            df = pd.read_csv(uploaded_file)  # Assuming it's a CSV for now
            if uploaded_file.type == "xlsx" or uploaded_file.type == "xlsm":
                df = pd.read_excel(uploaded_file)  # Use read_excel for Excel files

            st.success("File uploaded successfully!")
            return df

        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            return None

#--------------------------------PAGE SET UP--------------------------------

st.set_page_config(page_title="Upload Your Data", page_icon="📈", layout="wide")

st.header("Upload Your Data")
st.write("Upload your data to get started. When you are done. Click Next to move to the next step.")

#--Sidebar setup--------------------------------

st.sidebar.header("Rules for Data Upload")
st.sidebar.divider()
st.sidebar.write("1. Only CSV, XLSX, and XLSM files are allowed.")
st.sidebar.write("The maximum file size allowed is 200MB.")
st.sidebar.divider()
st.sidebar.write("*Disclaimer - Tada does not store your data. Once you close the app, your data is deleted. Tada is also not responsible for the security of your data*")
st.sidebar.divider()


#-----------------------------File Upload Section--------------------------------

uploaded_df = secure_file_uploader()

if uploaded_df is not None:
    st.session_state.main_df = uploaded_df.copy()  # Initialize session state

if 'main_df' in st.session_state:
    st.write("Preview of the uploaded data:")
    st.dataframe(st.session_state.main_df)
            
else:
    st.warning("Please upload a file to continue")

#--------------------------------Next Button--------------------------------
        
col1, col2 = st.columns([10, 1])

with col1:
    st.write("")
with col2:    
    next_button = st.button("Next", key="next_button", help="Move to next step")
    if next_button: 
        if 'main_df' not in st.session_state:
            st.session_state.main_df = uploaded_df.copy()  # Initialize session state
        switch_page("STEP 2 - Preprocessing")


