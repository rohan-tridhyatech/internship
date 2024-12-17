import streamlit as st
import pandas as pd
import plotly.express as px

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

    # Sidebar for filtering options
    st.sidebar.subheader("Filter Options")

    # Generate filters for categorical data
    filters = {}
    for col in data.select_dtypes(include=['object', 'category']).columns:
        unique_values = data[col].dropna().unique().tolist()
        selected = st.sidebar.multiselect(f"Filter by {col}", options=unique_values, default=unique_values)
        filters[col] = selected

    # Generate filters for numeric data
    numeric_filters = {}
    for col in data.select_dtypes(include=['int64', 'float64']).columns:
        min_val = float(data[col].min())
        max_val = float(data[col].max())
        range_values = st.sidebar.slider(f"Filter {col} range", min_val, max_val, (min_val, max_val))
        numeric_filters[col] = range_values

    # Apply filters to the dataset
    filtered_data = data.copy()
    for col, selected_values in filters.items():
        if selected_values:
            filtered_data = filtered_data[filtered_data[col].isin(selected_values)]
    for col, range_values in numeric_filters.items():
        filtered_data = filtered_data[(filtered_data[col] >= range_values[0]) & (filtered_data[col] <= range_values[1])]

    # Visualization
    st.subheader("Visualizations")

    numeric_cols = filtered_data.select_dtypes(include=['int64', 'float64']).columns.tolist()
    categorical_cols = filtered_data.select_dtypes(include=['object', 'category']).columns.tolist()

    # Line chart
    if numeric_cols:
        st.subheader("Line Chart")
        x_col = st.selectbox("Select X-axis for Line Chart", options=numeric_cols)
        y_col = st.selectbox("Select Y-axis for Line Chart", options=numeric_cols)
        st.line_chart(filtered_data[[x_col, y_col]].set_index(x_col))

    # Bar chart
    if numeric_cols and categorical_cols:
        st.subheader("Bar Chart")
        bar_col = st.selectbox("Select a Numeric Column for Bar Chart", options=numeric_cols)
        group_col = st.selectbox("Group Bar Chart by", options=categorical_cols)
        bar_data = filtered_data.groupby(group_col)[bar_col].sum().reset_index()
        st.bar_chart(bar_data.set_index(group_col))

    # Scatter plot
    if len(numeric_cols) >= 2:
        st.subheader("Scatter Plot")
        scatter_x = st.selectbox("Select X-axis for Scatter Plot", options=numeric_cols, key="scatter_x")
        scatter_y = st.selectbox("Select Y-axis for Scatter Plot", options=numeric_cols, key="scatter_y")
        scatter_fig = px.scatter(filtered_data, x=scatter_x, y=scatter_y, title="Scatter Plot")
        st.plotly_chart(scatter_fig)

    # Histogram
    if numeric_cols:
        st.subheader("Histogram")
        hist_col = st.selectbox("Select Column for Histogram", options=numeric_cols, key="hist_col")
        hist_bins = st.slider("Number of Bins", 5, 100, 20)
        hist_fig = px.histogram(filtered_data, x=hist_col, nbins=hist_bins, title="Histogram")
        st.plotly_chart(hist_fig)

    # Box Plot
    if numeric_cols and categorical_cols:
        st.subheader("Box Plot")
        box_col = st.selectbox("Select a Numeric Column for Box Plot", options=numeric_cols, key="box_col")
        box_group = st.selectbox("Group Box Plot by", options=categorical_cols, key="box_group")
        box_fig = px.box(filtered_data, x=box_group, y=box_col, title="Box Plot")
        st.plotly_chart(box_fig)

    # Map for geospatial data
    if {'latitude', 'longitude'}.issubset(filtered_data.columns):
        st.subheader("Map Visualization")
        st.map(filtered_data[['latitude', 'longitude']])

else:
    st.info("Please upload a CSV file to get started.")
