import streamlit as st
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(page_title="Tada Home", page_icon="👋")

    st.write("# Welcome to TADA")

    st.markdown(
        """
          #### Tada: Your Data Transformation Sidekick

          Tada was created to revolutionize the way you work with data. Say goodbye to tedious cleaning and manipulation tasks – Tada does the heavy lifting so you can focus on the insights that matter. With lightning-fast processing and automatic insight generation, unlock the true power of your data with ease.

          ---

          ## Please select an Excel file to upload: 
        
        """
    )

    uploaded_df = secure_file_uploader()
    if uploaded_df is not None:
      # Data Analysis Tools
      cols = st.columns(3)  # Create columns for checkboxes
      do_duplicates_check = cols[0].checkbox("Check for Duplicates")
      do_empty_check = cols[1].checkbox("Check for Empty Cells")
      do_encoding_check = cols[2].checkbox("Check Encoding")

      # Updated DataFrame (Initially displayed as-is)
      df_to_display = uploaded_df.copy() 

      # Apply analysis if selected
      if do_duplicates_check:
          df_to_display = modify_df_for_duplicates(df_to_display)  # You'll need to implement this
          check_duplicates(df_to_display)  # Display results

      if do_empty_check:
          df_to_display = modify_df_for_empty_cells(df_to_display)  # You'll need to implement this
          check_empty_cells(df_to_display)  # Display results

      if do_encoding_check:
          check_encoding(df_to_display)  # Display results

      st.subheader("Analyzed Data")  
      st.dataframe(df_to_display) 
        

def check_duplicates(df):
    """Checks for duplicate rows in the DataFrame."""
    if df.duplicated().sum() > 0:
        st.warning("Duplicate rows found!")
    else:
        st.info("No duplicate rows detected.")

def check_empty_cells(df):
    """Checks for empty cells (NaN values) in the DataFrame."""
    if df.isna().sum().sum() > 0:
        st.warning("Empty cells found!")
    else:
        st.info("No empty cells detected.")

def check_encoding(df):
    """Checks if any columns contain one-hot or multi-hot encoding."""
    for col in df.select_dtypes(include='object'):
        if len(df[col].unique()) <= 2:
            st.info(f"Column '{col}' appears to be one-hot encoded.")
        elif len(df[col].unique()) > 2:
            st.info(f"Column '{col}' may be multi-hot encoded.")

def modify_df_for_duplicates(df):
    """Removes duplicate rows from the DataFrame."""
    df_clean = df.drop_duplicates()
    st.info("Duplicate rows removed.")  # Indicate that changes were made
    return df_clean


def modify_df_for_empty_cells(df):
    """Fills empty cells (NaN values) in the DataFrame."""  
    fill_value = st.text_input("Enter a value to fill empty cells:", "Missing")
    df_clean = df.fillna(fill_value)
    st.info("Empty cells filled.") 
    return df_clean


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


if __name__ == "__main__":
    run()
