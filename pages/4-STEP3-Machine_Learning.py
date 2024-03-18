import streamlit as st
import pandas as pd
from modules.shared_functions import switch_page

st.set_page_config(page_title="Use Your Data For ML", page_icon="📈", layout="wide")

st.image("images/UNDER CONSTRUCTION.png", caption=None, width=None, use_column_width=None, clamp=False, channels="RGB", output_format="auto")
st.sidebar.header("Machine Learning")
st.sidebar.write("On this page, you can use your data to train a machine learning model. You can also use the model to make predictions on new data.")