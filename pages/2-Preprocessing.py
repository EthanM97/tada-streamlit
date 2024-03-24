import streamlit as st
import pandas as pd
from modules.shared_functions import *
from modules.preproc_functions import *

st.set_page_config(page_title="Pre-Process Your Data", page_icon="📈", layout="wide")

# Function to revert to original DataFrame
def undo():
    st.session_state.main_df = st.session_state.original_df
    st.session_state.changes_undone = True

def show_only_duplicates():   
    if st.session_state.show_duplicates:
        st.session_state.main_df = get_duplicate_rows(st.session_state.main_df)

def remove_duplicates():
    st.session_state.modified_df = remove_duplicate_rows(st.session_state.main_df)
    st.session_state.main_df = st.session_state.modified_df
    st.session_state.num_duplicates = count_duplicate_rows(st.session_state.main_df)

def remove_selected_duplicates():
    st.session_state.main_df.drop(st.session_state.remove_specific_duplicates, inplace=True)
    st.session_state.modified_df = st.session_state.main_df.copy()
    st.session_state.num_duplicates = count_duplicate_rows(st.session_state.main_df)

def show_visualization_button():
    finish_button = st.button("TRY VISUALIZATION", key="finish_button", help="Move to Visualization")
    if finish_button: 
        if 'main_df' not in st.session_state:
            st.dataframe(st.session_state.main_df)
        switch_page("2-Visualization")

def get_indices_of_duplicates(df):
    '''return the indices of duplicate rows in the data set'''
    return df[df.duplicated(keep=False)].index

def show_csv_download_button():
    csv = convert_df(st.session_state.main_df)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='processed_data.csv',
        mime='text/csv',
    )

def show_undo_button():
    st.button("Undo Changes", on_click=undo)
    if st.session_state.changes_undone:
        st.success("undo successful!")

#--Sidebar setup--------------------------------

st.header("Pre-Processing")
st.sidebar.header("Preprocessing")
st.sidebar.write("preprocessing is the process of preparing data for analysis. It is the first and crucial step in data analysis. It involves cleaning, transforming, and encoding data to make it ready for machine learning models.")


#-----direct user back to upload page if no data has been uploaded yet

if 'main_df' not in st.session_state:

    st.image("images/confused.png", caption="You haven't uploaded any data yet!")
    st.error("you havent uploaded any data yet!") 
    button = st.button("UPLOAD DATA NOW")
    if button:
        switch_page("1-upload") #this is not moving to upload page???

else: 
    
    #initialize other session state variables
    
    st.session_state.original_df = st.session_state.main_df.copy()
    st.session_state.modified_df = st.session_state.main_df.copy()
    st.session_state.num_duplicates = count_duplicate_rows(st.session_state.main_df)
    st.session_state.duplicates_removed = False
    st.session_state.changes_undone = False

    #add logic for each preprocessing tab

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(["Remove Duplicates", "Handle Missing Data", "Handle Outliers", "Feature Engineering", "Encoding", "Scaling", "Dimensionality Reduction"])

    with tab1:

        with st.container():

            st.subheader("Remove Duplicates")
            
            if st.session_state.num_duplicates > 0: 

                col1, col2, col3 = st.columns([2,2,1])
                
                with col1:
                    st.write(f"We found {st.session_state.num_duplicates} duplicate rows in your data!")
                
                with col2:
                    # Checkbox to show only duplicate rows
                    duplicates_only = st.checkbox("Show only duplicate rows", value=False, key="show_duplicates", on_change=show_only_duplicates)
                
                dropdown = st.selectbox("Select the duplicated row you wish to remove", get_indices_of_duplicates(st.session_state.main_df), key="remove_specific_duplicates")

                col1, col2, col3 = st.columns([3, 3, 5])
                with col1: 
                    st.session_state.remove_selected = st.button("Remove Selected Duplicates" , on_click=remove_selected_duplicates, key="row")
                with col2:   
                    # Button to remove all duplicates
                    st.session_state.remove_all = st.button("Remove All Duplicates" , on_click=remove_duplicates)
                     
                #whenever a row is removed print row x removed successfully
                if st.session_state.remove_selected:
                    st.success(f"Selected row removed successfully!")
                elif st.session_state.remove_all:
                    st.success(f"All duplicate rows have been removed!")
                    
            elif st.session_state.num_duplicates <= 0 and 'remove_selected' in st.session_state or 'remove_all' in st.session_state: 
                st.success(f"No duplicate rows remaining! Select another preprocessing function from the tabs above, or move on to Visualization (STEP 2)")
                col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])
                
                with col1:
                    show_undo_button()
            else:
                st.success(f"No duplicate rows found in your data! Select another preprocessing function from the tabs above, or move on to Visualization (STEP 2)")    
                col1, col2, col3, col4, col5 = st.columns([3,1,1,1,1])
                
                with col1:
                    show_undo_button()

            # Display the DataFrame with applied customizations
            st.dataframe(st.session_state.main_df)
            col1, col2, col3, col4, col5 = st.columns([2,1,1,1,1])

            with col4:
                    show_csv_download_button()
            with col5:    
                show_visualization_button()

    #removing or filling in missing data 
    #PROBLEM_2A => need to make dynamic => the total missing values and list of features with missing values should be updated after each change
                    
    with tab2:
        
        st.session_state.total_missing = get_total_missing_values(st.session_state.main_df)
        st.session_state.num_missing_by_feature = get_missing_values_by_feature(st.session_state.main_df)

        with st.form("missing_data_form"):
            st.subheader("Handle Missing Data")
            
            if st.session_state.total_missing > 0:
                st.write(f"There are {st.session_state.total_missing} missing values in your dataset")
            else:
                st.success("Congratulations! There are no more missing values in your dataset!")
            
            st.selectbox("Select a feature to fill in missing values", st.session_state.num_missing_by_feature.index, key="fill_feature")
            st.selectbox("Select a method to fill in missing values", ["Fill with mean", "Fill with median", "Fill with mode", "Fill with custom value"], key="fill_method")
            st.text_input("Fill in missing values with:", key="fill_value")

            submitted = st.form_submit_button("Apply Changes")
            if submitted:
                fill_method = st.session_state.fill_method
                fill_feature = st.session_state.fill_feature
                fill_value = st.session_state.fill_value
                fill_missing_values(st.session_state.main_df, fill_method, fill_feature, fill_value)

                st.success("data table updated")

    with tab3:
        '''with st.form("outliers_data_form"):
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
                #plot_outliers(df, st.session_state.outlier_feature)'''
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


   
       




            


