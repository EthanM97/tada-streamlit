import streamlit as st
from streamlit.logger import get_logger
import pandas as pd
from modules.shared_functions import *

LOGGER = get_logger(__name__)

def run():
    st.set_page_config(page_title="Tada Home", page_icon="👋", layout="wide")

    st.write("# Welcome to TADA")

    st.markdown(
        """
          #### Tada: Your Data Transformation Sidekick

          Tada was created to revolutionize the way you work with data. Say goodbye to tedious cleaning and manipulation tasks – Tada does the heavy lifting so you can focus on the insights that matter. With lightning-fast processing and automatic insight generation, unlock the true power of your data with ease.

          ---
        
        """
    )

    col1, col2 = st.columns([10, 2])

    with col1:
        st.write("")
    with col2:    
        next_button = st.button("Next", key="next_button", help="Move to next step")
        if next_button: 
            switch_page("STEP1-UPLOAD")


#allows addition of logo to top of sidebar menu

def add_logo(logo_url: str, height: int = 120):
    """Add a logo (from logo_url) on the top of the navigation page of a multipage app.
    Taken from [the Streamlit forum](https://discuss.streamlit.io/t/put-logo-and-title-above-on-top-of-page-navigation-in-sidebar-of-multipage-app/28213/6)
    The url can either be a url to the image, or a local path to the image.

    Args:
        logo_url (str): URL/local path of the logo
    """

    if validators.url(logo_url) is True:
        logo = f"url({logo_url})"
    else:
        logo = f"url(data:image/png;base64,{base64.b64encode(Path(logo_url).read_bytes()).decode()})"

    st.markdown(
        f"""
        <style>
            [data-testid="stSidebarNav"] {{
                background-image: {logo};
                background-repeat: no-repeat;
                padding-top: {height - 40}px;
                background-position: 20px 20px;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

if __name__ == "__main__":
    run()