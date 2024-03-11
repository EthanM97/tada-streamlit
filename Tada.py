
import streamlit as st
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(
        page_title="Tada Home",
        page_icon="👋",
    )

    st.write("# Welcome to TADA")

    st.markdown(
      """
        ## Please select a excel file to upload.
      
      """
    )
    
    uploaded_df = secure_file_uploader()

    if uploaded_df is not None:
        st.subheader("Uploaded Data")
        st.dataframe(uploaded_df)
    

def secure_file_uploader():
    """
    Creates a secure file uploader for Streamlit apps.
    Allows only CSV, XLSX, and XLSM files with size under 200MB.

    Returns:
        The uploaded file as a Pandas DataFrame, or None if no valid file was uploaded.
    """

    # Set up the file uploader widget
    uploaded_file = st.file_uploader("Choose a CSV, XLSX, or XLSM file", 
                                     type=["csv", "xlsx", "xlsm"],
                                     help="Only CSV, XLSX and XLSM files are allowed")

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

            # Display success message and dataframe 
            st.success("File uploaded successfully!")

            return df

        except Exception as e:
            st.error(f"An error occurred while reading the file: {e}")
            return None



if __name__ == "__main__":
    run()
