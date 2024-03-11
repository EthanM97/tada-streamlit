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
        df_to_display = check_and_remove_duplicates(df_to_display)  # Display results

      if do_empty_check:
        df_to_display = check_and_fill_empty_cells(df_to_display)  # Display results

      if do_encoding_check:
        df_needs_encoding = detect_encoding_needs(df_to_display.copy())
        if df_needs_encoding is not False:
            df_to_display = apply_one_hot_encoding(df_needs_encoding)  
            st.info("One-hot encoding applied.")
        else:
            st.info("All columns appear to be already encoded.")

      st.subheader("Analyzed Data")  
      st.dataframe(df_to_display) 
        

def check_and_remove_duplicates(df):
    """Checks for and removes duplicate rows in the DataFrame."""
    df_clean = df.copy()  # Create a copy of the DataFrame
    duplicate_rows = df_clean.duplicated().sum()
    if duplicate_rows > 0:
        df_clean.drop_duplicates(inplace=True)
        st.warning(f"Duplicate rows found and removed: {duplicate_rows}")
    else:
        st.info("No duplicate rows detected.")
    return df_clean

def check_and_fill_empty_cells(df):
    """Checks for empty cells (NaN values) and fills them in the DataFrame."""
    df_clean = df.copy()  # Create a copy of the DataFrame
    empty_cells = df_clean.isna().sum().sum()
    if empty_cells > 0:
        fill_value = st.text_input("Enter a value to fill empty cells:", "Missing")
        df_clean.fillna(fill_value, inplace=True)
        st.warning(f"Empty cells found and filled with '{fill_value}'.")
    else:
        st.info("No empty cells detected.")
    return df_clean

def detect_encoding_needs(df):
    """Checks for columns in need of one-hot/multi-hot encoding.

    Args:
        df (pandas.DataFrame): The DataFrame to analyze.

    Returns:
        pandas.DataFrame or bool: A DataFrame containing columns that require encoding, or False if all columns are already encoded.
    """

    df_to_encode = df.copy()
    for col in df_to_encode.select_dtypes(include='object'):
        unique_values = df_to_encode[col].unique()
        if len(unique_values) > 2:  # Assume already encoded if more than 2 unique values
            df_to_encode.drop(col, axis=1, inplace=True)  # Remove encoded columns

    if df_to_encode.empty:
        return False  # All columns are encoded
    else:
        return df_to_encode  # Return DataFrame with columns to encode 


def apply_one_hot_encoding(df):
    """Applies one-hot encoding to eligible columns.

    Args:
        df (pandas.DataFrame): The DataFrame containing columns to encode.

    Returns:
        pandas.DataFrame: The DataFrame with one-hot encoded columns.
    """

    return pd.get_dummies(df)  

        


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
