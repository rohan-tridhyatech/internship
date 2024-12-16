import streamlit as st
import pandas as pd
import numpy as np

# Title and description
st.title("Interactive Data Visualization Dashboard")
st.write("This dashboard allows you to upload a CSV file, filter data, and visualize it with interactive charts.")

# File uploader
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    # Read the uploaded CSV file
    data = pd.read_csv(uploaded_file)

    # Display the data
    st.subheader("Dataset Preview")
    st.dataframe(data.head())

    # Select columns for filtering and visualization
    st.sidebar.subheader("Filter Options")

    # Generate filters dynamically based on data
    filters = {}
    for col in data.select_dtypes(include=['object', 'category']).columns:
        unique_values = data[col].dropna().unique().tolist()
        selected = st.sidebar.multiselect(f"Filter by {col}", options=unique_values, default=unique_values)
        filters[col] = selected

    # Apply filters
    filtered_data = data.copy()
    for col, selected_values in filters.items():
        if selected_values:
            filtered_data = filtered_data[filtered_data[col].isin(selected_values)]

    # Visualization
    st.subheader("Visualizations")

    # Line chart for numeric data
    numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    if numeric_cols:
        x_col = st.selectbox("Select X-axis for Line Chart", options=numeric_cols)
        y_col = st.selectbox("Select Y-axis for Line Chart", options=numeric_cols)
        st.line_chart(filtered_data[[x_col, y_col]].set_index(x_col))

    # Bar chart for categorical data
    if numeric_cols and len(filters) > 0:
        bar_col = st.selectbox("Select a Numeric Column for Bar Chart", options=numeric_cols)
        group_col = st.selectbox("Group Bar Chart by", options=filters.keys())
        bar_data = filtered_data.groupby(group_col)[bar_col].sum().reset_index()
        st.bar_chart(bar_data.set_index(group_col))

    # Map for geospatial data (latitude and longitude)
    if {'latitude', 'longitude'}.issubset(filtered_data.columns):
        st.subheader("Map Visualization")
        st.map(filtered_data[['latitude', 'longitude']])

else:
    st.info("Please upload a CSV file to get started.")
