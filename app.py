import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Debug Mode", layout="wide")

st.title("Petrol Station Dashboard")

# Show current directory
st.write("Current working directory:")
st.write(os.getcwd())

# Show files in folder
st.write("Files in this folder:")
st.write(os.listdir())

# Try loading Excel safely
try:
    df = pd.read_excel("ELSA_OIL_DATASET.xlsx")
    st.success("Excel file loaded successfully!")
    st.write("Columns in dataset:")
    st.write(df.columns)
    st.write("Preview:")
    st.dataframe(df.head())
except Exception as e:
    st.error("Error loading Excel file:")
    st.write(e)