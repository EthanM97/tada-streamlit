import streamlit as st
import pandas as pd
from modules.shared_functions import *
from modules.preproc_functions import *

st.set_page_config(page_title="Pre-Process Your Data", page_icon="📈", layout="wide")

st.header("Pre-Processing")

st.sidebar.header("Preprocessing")
st.sidebar.write("preprocessing is the process of preparing data for analysis. It is the first and crucial step in data analysis. It involves cleaning, transforming, and encoding data to make it ready for machine learning models.")

if 'main_df' not in st.session_state:
    df = pd.DataFrame()
    st.session_state.main_df = df
    #st.image(confused.png, caption="You haven't uploaded any data yet!")
    st.error("you havent uploaded any data yet!") 
    button = st.button("UPLOAD DATA NOW")
    if button:
        switch_page("UPLOAD") #this is not moving to upload page???

df = st.session_state["main_df"]

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Remove Duplicates", "Handle Missing Data", "Handle Outliers", "Feature Engineering", "Encoding", "Scaling", "Dimensionality Reduction"])

#removing duplicate rows

with tab1:
    num_duplicates = count_duplicate_rows(df)
    with st.form("duplicates_data_form"):
        st.subheader("Remove Duplicates")
        if num_duplicates > 0:
            st.write(f"There are {num_duplicates} duplicate rows in your data")
            st.write("*duplicates are highlighted in yellow in the table below*")
            submitted = st.form_submit_button("Remove All Duplicates")
            if submitted:
                remove_duplicate_rows(df)
                st.success("duplicate rows removed")
        else:
            st.success("Amazing! No duplicate rows found!")
            submitted = st.form_submit_button("Remove All Duplicates")
            if submitted:
                st.success("No changes to apply. Try another preprocessing step.")

#removing or filling in missing data 
#PROBLEM_2A => need to make dynamic => the total missing values and list of features with missing values should be updated after each change
                
with tab2:

    total_missing = get_total_missing_values(df)
    num_missing_by_feature = get_missing_values_by_feature(df)

    with st.form("missing_data_form"):
        st.subheader("Handle Missing Data")
        
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

            st.success("data table updated")

with tab3:
    with st.form("outliers_data_form"):
        st.subheader("Handle Outliers")
        col1, col2 = st.columns([1, 1])
        with col1:
            st.number_input("Enter the threshold for outliers", key="outlier_threshold", step=1, value=3, help="The threshold for outliers is usually 1.5 times the interquartile range (IQR)")
            st.write("These are the features in your data set that have outliers:")
            st.selectbox("Select a feature to view the outliers", df.columns, key="outlier_feature")
            st.checkbox("remove outliers", key="remove_outliers")
            submitted = st.form_submit_button("Apply Changes")
            if submitted:
                if st.session_state.remove_outliers:
                    remove_outliers(df, st.session_state.outlier_feature, st.session_state.outlier_threshold)
                st.success("data table updated")
        with col2:
            st.write("Outliers are extreme values that deviate from other observations in the data set. They may indicate a variability in a measurement, experimental errors, or a novelty. Outliers can have a disproportionate effect on statistical analysis, such as the mean, which can result in misleading interpretations. It is important to identify and remove outliers from the data set.")
            #scatterplot of selected feature
            #plot_outliers(df, st.session_state.outlier_feature)
with tab4:
    with st.form("ft_eng_data_form"):
        st.subheader("Feature Engineering")
        st.write("feature engineering logic here")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.success("data table updated")
with tab5:
    with st.form("encode_data_form"):
        st.subheader("Encoding")
        st.write("encoding logic here")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.success("data table updated")
with tab6:
    with st.form("scale_data_form"):
        st.subheader("Scaling")
        st.write("scaling logic here")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.success("data table updated")
with tab7:
    with st.form("dim_reduc_data_form"):
        st.subheader("Dimensionality Reduction")
        st.write("suggest removal of features with one to one correlation")
        st.write("suggest combining one hot encoded columns")
        st.write("Offer option of PCA")
        submitted = st.form_submit_button("Apply Changes")
        if submitted:
            st.success("data table updated")

#allow download of modified data as csv    
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




        


