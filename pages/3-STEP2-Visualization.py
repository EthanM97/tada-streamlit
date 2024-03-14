import streamlit as st
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt 
from modules.shared_functions import *
from modules.preproc_functions import *

st.set_page_config(page_title="Visualize Your Data", page_icon="📊", layout="wide")

st.header("Visualize")

st.sidebar.header("Visualize")
st.sidebar.write("Visualizations allow the human eye to process patterns and trends with greater ease and efficiency than tabular data. This step is essential to gather key insights into your data.")

if 'main_df' not in st.session_state:
    df = pd.DataFrame()
    st.session_state.main_df = df
    #st.image(confused.png, caption="You haven't uploaded any data yet!")
    st.error("you havent uploaded any data yet!") 
    button = st.button("UPLOAD DATA NOW")
    if button:
        switch_page("UPLOAD") #this is not moving to upload page???

df = st.session_state["main_df"]

# Set theme
sns.set_style("white")
sns.color_palette("tab10")

tab1, tab2, tab3, tab4 = st.tabs(["Scatter Plot", "Histogram", "Bar Chart", "Line Chart"])

with tab1:
    st.subheader("Scatter Plot Configuration")

    # Column Selection
    col1, col2 = st.columns(2)  # Divide into two columns for selection

    with col1:
        x_col = st.selectbox("Select X-axis column:", df.columns)
    with col2:
        y_col = st.selectbox("Select Y-axis column:", df.columns)

    # Color (Hue) Selection
    hue_col = st.selectbox("Color by (optional):", df.columns.insert(0, None))

    # Plot Button
    if st.button("Create Scatter Plot"):
        # Handle potential errors before plotting
        if not x_col or not y_col:
            st.warning("Please select both X and Y columns to plot.")
        elif not df.empty and x_col in df.columns and y_col in df.columns:
            # Create the scatter plot 
            fig, ax = plt.subplots(figsize=(18, 12))  
            if hue_col:
                sns.scatterplot(x=x_col, y=y_col, hue=hue_col, data=df, ax=ax)
            else:
                sns.scatterplot(x=x_col, y=y_col, data=df, ax=ax)
            st.pyplot(fig)
        else:
            st.error("No data found or selected columns are invalid. Please check your data.")
            
            
with tab2:
    st.subheader("Histogram Configuration")
    
    hist_1, hist_2, hist_3 = st.columns(3)
    
    # We also want to select bin between 2 and 20
    bin_input = st.text_input("Enter the number of bins:", 3)
    int_bins = int(bin_input)
    
    with hist_1:
        x_col = st.selectbox("Select X-axias column:", df.columns)
        
    with hist_2:
        y_col = st.selectbox("Select Y-axias column:", df.columns)
        
    # Color (Hue) Selection
    hue_col_hist = st.selectbox("Hue:", df.columns.insert(0, None))
    
    if st.button("Plot Histogram"):
        # Handle the error
        if not x_col or not y_col:
            st.warning("Please select both X and Y columns to plot.")
        elif not df.empty and x_col in df.columns and y_col in df.columns:
            # Now create the plot
            fig, ax =  plt.subplots(figsize=(18,12))
            if hue_col_hist:
                sns.histplot(x=x_col, y=y_col, hue=hue_col_hist, data=df, ax=ax, bins=int_bins)
            else:
                sns.histplot(x=x_col, y=y_col, data=df, ax=ax, bins=int_bins)
            st.pyplot(fig)
            
        else:
            st.error("No data found or selected columns are invalid. Please check your data.")
    
    
    
    

