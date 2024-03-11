import streamlit as st
from streamlit.logger import get_logger
import pandas as pd

LOGGER = get_logger(__name__)


def run():
    st.set_page_config(page_title="Tada Home", page_icon="👋", layout="wide")

    st.write("# Welcome to TADA", align="center")

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
        st.session_state.df_to_display = uploaded_df.copy()  # Initialize session state

             # Data Analysis Tools
        cols = st.columns(3)
        do_duplicates_check = cols[0].checkbox("Check for Duplicates")
        do_empty_check = cols[1].checkbox("Check for Empty Cells")
        do_encoding_check = cols[2].checkbox("Check Encoding")

        if st.button("Apply Filters"):
            df = apply_filters(st.session_state.df_to_display.copy(), do_duplicates_check, do_empty_check, do_encoding_check)
            st.session_state.df_to_display = df
            
        customize_dataframe()

def customize_dataframe():
    st.write("## Rename Features (Columns)")

    df = st.session_state.df_to_display

    # Use st.beta_columns to create two columns layout
    customize_col, data_col = st.columns(2)

    with customize_col:
        with st.form("customize_df"):
            # Display a text input for each column for renaming purposes
            st.write('### Try Renaming')
            new_column_names_dict = {col: st.text_input(f"{col}", value=col, key=f"rename_{col}") for col in df.columns}

            # Prepare a list of current (potentially new) column names for the rearrangement prompt
            # This updates as new names are entered but before the "Apply Customizations" button is clicked
            current_columns_after_rename = [new_column_names_dict[col] for col in df.columns]
            
            # Text input for user to rearrange columns, showing current (potentially new) order by default
            cols_order_str = st.text_input("Rearrange columns (comma-separated):", value=','.join(current_columns_after_rename), key="rearrange_cols")

            submitted = st.form_submit_button("Apply Customizations")
            if submitted:
                # Update column names based on user input
                df.rename(columns=new_column_names_dict, inplace=True)

                # Trim spaces from user input and split by commas to form new order list
                new_order = [col.strip() for col in cols_order_str.split(',')]

                # Validate the new column order
                invalid_columns = [col for col in new_order if col not in df.columns]
                if invalid_columns:
                    st.error(f"Error: These columns are not in the DataFrame or were mistyped: {invalid_columns}")
                else:
                    # Rearrange columns based on validated new order
                    df = df[new_order]
                    st.session_state.df_to_display = df  # Update session state to reflect changes

    with data_col:
        # Display the DataFrame with applied customizations
        st.subheader("Results Data")
        st.dataframe(st.session_state.df_to_display)


def apply_filters(df, do_duplicates_check, do_empty_check, do_encoding_check):
    if do_duplicates_check:
        df = check_and_remove_duplicates(df)
    if do_empty_check:
        df = check_and_fill_empty_cells(df)
    if do_encoding_check:
        df = apply_encoding_if_needed(df)
    return df


def apply_encoding_if_needed(df):
    df_needs_encoding = detect_encoding_needs(df.copy())
    if df_needs_encoding is not False:
        df = apply_one_hot_encoding(df_needs_encoding)
        st.info("One-hot encoding applied.")
    else:
        st.info("All columns appear to be already encoded.")
    return df
        

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
