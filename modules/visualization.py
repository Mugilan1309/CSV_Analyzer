import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def plot_data(df):
    """Generates different visualizations using Pandas and Matplotlib."""
    st.write("### Visualization")
    plot_type = st.selectbox("Select Plot Type", ["None", "Histogram", "Box Plot", "Scatter Plot"])

    if plot_type != "None":
        col1, col2 = st.columns(2)
        with col1:
            x_col = st.selectbox("X-axis", df.columns)
        with col2:
            y_col = st.selectbox("Y-axis", df.columns) if plot_type == "Scatter Plot" else None

        fig, ax = plt.subplots()

        if plot_type == "Histogram":
            df[x_col].hist(ax=ax, bins=20)
        elif plot_type == "Box Plot":
            df.boxplot(column=[x_col], ax=ax)
        elif plot_type == "Scatter Plot" and y_col:
            ax.scatter(df[x_col], df[y_col])

        st.pyplot(fig)
