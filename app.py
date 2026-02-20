import streamlit as st
import pandas as pd
import plotly.express as px
import pathlib

# Page Config
st.set_page_config(page_title="Petrol Station Dashboard", layout="wide")

# Title
st.title("Petrol Station Sales Dashboard")

# Load Excel (Cloud-safe path)
file_path = pathlib.Path(__file__).parent / "ELSA_OIL_DATASET.xlsx"

@st.cache_data
def load_data():
    df = pd.read_excel(file_path)
    return df

df = load_data()

# Convert Date column if it exists
for col in df.columns:
    if "date" in col.lower():
        df[col] = pd.to_datetime(df[col], errors="coerce")

# SIDEBAR FILTERS (INTERACTIVE)
st.sidebar.header("Filter Dashboard")

# Select columns dynamically (safe for any dataset)
categorical_cols = df.select_dtypes(include="object").columns.tolist()

if len(categorical_cols) > 0:
    filter_col = st.sidebar.selectbox("Select Filter Column", categorical_cols)
    filter_values = st.sidebar.multiselect(
        f"Select {filter_col}",
        options=df[filter_col].dropna().unique(),
        default=df[filter_col].dropna().unique()
    )
    filtered_df = df[df[filter_col].isin(filter_values)]
else:
    filtered_df = df.copy()

# KPI SECTION
st.subheader("Key Performance Indicators")

numeric_cols = filtered_df.select_dtypes(include="number").columns

col1, col2, col3 = st.columns(3)

if len(numeric_cols) >= 1:
    col1.metric("Total Records", len(filtered_df))
    col2.metric("Total Value", f"{filtered_df[numeric_cols[0]].sum():,.2f}")
    col3.metric("Average Value", f"{filtered_df[numeric_cols[0]].mean():,.2f}")

# CHART SECTION
st.subheader("📈 Interactive Visualizations")

if len(numeric_cols) >= 1 and len(categorical_cols) >= 1:
    chart_data = filtered_df.groupby(categorical_cols[0])[numeric_cols[0]].sum().reset_index()

    fig_bar = px.bar(
        chart_data,
        x=categorical_cols[0],
        y=numeric_cols[0],
        title=f"{numeric_cols[0]} by {categorical_cols[0]}",
        text_auto=True
    )

    st.plotly_chart(fig_bar, use_container_width=True)

# DATA TABLE (for client inspection)
st.subheader("Data Preview")
st.dataframe(filtered_df, use_container_width=True)

# DOWNLOAD BUTTON (Professional Feature)
csv = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="⬇ Download Filtered Data as CSV",
    data=csv,
    file_name="filtered_petrol_data.csv",
    mime="text/csv",
)
