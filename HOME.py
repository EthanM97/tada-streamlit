import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
from modules.shared_functions import *
from st_pages import Page, add_page_title, show_pages

LOGGER = get_logger(__name__)

show_pages(
[
    Page("HOME.py", "HOME", "🏠"),
    # Can use :<icon-name>: or the actual icon
    Page("pages/1-upload.py", "STEP 1 - Upload", "📁"),
    # The pages appear in the order you pass them
    Page("pages/2-Preprocessing.py", "STEP 2 - Preprocessing", "💻"),
    Page("pages/3-Visualization.py", "STEP 3 - Visualization", "📊"),
    # Will use the default icon and name based on the filename if you don't
    # pass them
    Page("pages/4-Machine_Learning.py", "STEP 4 - Machine Learning","🤖")

]
)   

def run():
    st.set_page_config(page_title="Tada Home", page_icon="🎉", layout="wide")
    st.write("# Welcome to TADA 🎉")
    
    st.markdown(
        """
          #### A Data Scientists Best Friend 🐕

          Tada was created to streamline the way you work with data. Say goodbye to tedious cleaning and manipulation tasks – Tada does the heavy lifting so you can focus on the insights that matter. With lightning-fast processing and automatic insight generation, unlock the true power of your data with ease.

          ---
        
        """
    )

    col1, col2 = st.columns([10, 2])

    with col1:
        st.write("")
    with col2:    
        next_button = st.button("Next", key="next_button", help="Move to next step")
        if next_button: 
            switch_page("STEP 1 - Upload")



if __name__ == "__main__":
    run()