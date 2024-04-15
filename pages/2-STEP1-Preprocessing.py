import streamlit as st
import pandas as pd
from datetime import datetime
from modules.shared_functions import *
from modules.preproc_functions import *

st.set_page_config(page_title="Pre-Process Your Data", page_icon="📈", layout="wide")

st.header("Pre-Processing")

st.sidebar.header("Preprocessing")
st.sidebar.write("preprocessing is the process of preparing data for analysis. It is the first and crucial step in data analysis. It involves cleaning, transforming, and encoding data to make it ready for machine learning models.")

# Check if the main dataframe is in the session state
if 'main_df' not in st.session_state:
    st.session_state.main_df = pd.DataFrame()

# If no data is uploaded yet, prompt the user
if st.session_state.main_df.empty:
    st.error("You haven't uploaded any data yet!")
    button = st.button("UPLOAD DATA NOW")
    if button:
        # Assuming switch_page function exists to handle page switching
        switch_page("UPLOAD")
else:
    df = st.session_state.main_df


tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Remove Duplicates", "Handle Missing Data", "Handle Outliers", "Feature Engineering", "Encoding", "Scaling", "Dimensionality Reduction"])

def update_dataframe(new_df):
    st.session_state['main_df'] = new_df
    st.session_state['last_updated'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def handle_duplicates():
    df = st.session_state['main_df']
    df = remove_duplicate_rows(df)
    update_dataframe(df)

with tab1:
    st.subheader("Remove Duplicates")
    num_duplicates = count_duplicate_rows(df)
    if num_duplicates > 0:
        st.write(f"There are {num_duplicates} duplicate rows in your data.")
        st.button("Remove All Duplicates", on_click=handle_duplicates)
    else:
        st.write("No duplicate rows found!")


#removing or filling in missing data 
#PROBLEM_2A => need to make dynamic => the total missing values and list of features with missing values should be updated after each change
                
with tab2:

    df = st.session_state.main_df

    total_missing = get_total_missing_values(df)
    num_missing_by_feature = get_missing_values_by_feature(df)

    with st.form("missing_data_form"):
        st.subheader("Handle Missing Data")
        df = st.session_state.main_df
        
        if total_missing > 0:
            st.write(f"There are {total_missing} missing values in your dataset")
        else:
            st.success("Congratulations! There are no more missing values in your dataset!")
        
        st.selectbox("Select a feature to fill in missing values", num_missing_by_feature.index, key="fill_feature")
        st.selectbox("Select a method to fill in missing values", ["Fill with mean", "Fill with median", "Fill with mode", "Fill with custom value"], key="fill_method")
        st.text_input("Fill in missing values with:", key="fill_value")

        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            fill_method = st.session_state.fill_method
            fill_feature = st.session_state.fill_feature
            fill_value = st.session_state.fill_value
            fill_missing_values(df, fill_method, fill_feature, fill_value)
            st.session_state.main_df = df 
            st.success("data table updated")
            
with tab3:
    
    df = st.session_state.main_df
    
    with st.form("outliers_data_form"):
        st.subheader("Handle Outliers")
        col1, col2 = st.columns([1, 1])
        with col1:
            threshold = st.number_input("Enter the threshold for outliers", key="outlier_threshold", step=1, value=3, help="The threshold for outliers is usually 1.5 times the interquartile range (IQR)")
            st.write("These are the features in your data set that have outliers:")
            feature = st.selectbox("Select a feature to view the outliers", df.columns, key="outlier_feature")
            remove = st.checkbox("Remove outliers", key="remove_outliers")
            submitted = st.form_submit_button("Apply Changes")
            if submitted:
                if remove:
                    df = remove_outliers(df, feature, threshold)
                    st.session_state.main_df = df  # Update session state
                    #st.rerun()
                st.success("Data table updated")
        with col2:
            st.write("Outliers are extreme values that deviate from other observations in the data set...")
            
with tab4:
    df = st.session_state.main_df
    
    with st.form("ft_eng_data_form"):
        st.subheader("Feature Engineering")
        st.write("feature engineering logic here")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.session_state.main_df = df  # Update session state
            st.success("data table updated")
            
            
with tab5:
    df = st.session_state.main_df

    with st.form("encode_data_form"):
        st.subheader("Encoding")
        st.write("encoding logic here")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.session_state.main_df = df  # Update session state
            st.success("data table updated")
            
            
with tab6:
    df = st.session_state.main_df
    
    with st.form("scale_data_form"):
        st.subheader("Scaling")
        st.write("scaling logic here")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.session_state.main_df = df  # Update session state
            st.success("data table updated")
            
            
with tab7:
    df = st.session_state.main_df
    
    with st.form("dim_reduc_data_form"):
        st.subheader("Dimensionality Reduction")
        st.write("suggest removal of features with one to one correlation")
        st.write("suggest combining one hot encoded columns")
        st.write("Offer option of PCA")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.session_state.main_df = df  # Update session state
            st.success("data table updated")

df = st.session_state.main_df


# allow download of modified data as csv  
csv = convert_df(df)
st.dataframe(df)

col1, col2 = st.columns([20, 4])

with col1:
    st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='processed_data.csv',
    mime='text/csv',
)
with col2:    
    finish_button = st.button("NEXT VISUALIZATION", key="finish_button", help="Move to Visualization")
    if finish_button: 
        if 'main_df' not in st.session_state:
            st.session_state.main_df = uploaded_df.copy()  # Initialize session state
            st.dataframe(st.session_state.main_df)
        switch_page("STEP2-Visualization")




        


