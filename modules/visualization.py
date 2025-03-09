import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

def plot_data(df):
    """Allows users to visualize numerical and categorical data separately."""
    
    # Identify column types
    numeric_cols = df.select_dtypes(include=['number']).columns
    categorical_cols = df.select_dtypes(exclude=['number']).columns

    plot_type = st.selectbox("Choose a Plot Type", ["None", "Scatter Plot", "Line Chart", "Histogram", "Bar Plot", "Count Plot"])

    if plot_type == "None":
        st.info("📌 Select a plot type to visualize data.")
        return

    # Scatter Plot & Line Chart (Only for Numeric Data)
    if plot_type in ["Scatter Plot", "Line Chart"]:
        if len(numeric_cols) < 2:
            st.warning("⚠️ Not enough numerical columns for scatter/line plot.")
            return

        x_col = st.selectbox("Select X-axis", numeric_cols)
        y_col = st.selectbox("Select Y-axis", numeric_cols)

        fig, ax = plt.subplots()
        if plot_type == "Scatter Plot":
            sns.scatterplot(x=df[x_col], y=df[y_col], ax=ax)
        else:
            sns.lineplot(x=df[x_col], y=df[y_col], ax=ax)

    # Histogram (Only for Numerical Columns)
    elif plot_type == "Histogram":
        if not numeric_cols.any():
            st.warning("⚠️ No numerical columns available for histogram.")
            return

        hist_col = st.selectbox("Select Column", numeric_cols)
        fig, ax = plt.subplots()
        sns.histplot(df[hist_col], bins=30, kde=True, ax=ax)

    # Bar Plot (Categorical X, Numerical Y)
    elif plot_type == "Bar Plot":
        if not categorical_cols.any() or not numeric_cols.any():
            st.warning("⚠️ Bar plots require at least one categorical and one numerical column.")
            return

        cat_col = st.selectbox("Select Categorical Column (X-axis)", categorical_cols)
        num_col = st.selectbox("Select Numerical Column (Y-axis)", numeric_cols)

        fig, ax = plt.subplots()
        sns.barplot(x=df[cat_col], y=df[num_col], ax=ax)

    # Count Plot (Only for Categorical Columns)
    elif plot_type == "Count Plot":
        if not categorical_cols.any():
            st.warning("⚠️ No categorical columns available for count plot.")
            return

        count_col = st.selectbox("Select Categorical Column", categorical_cols)
        fig, ax = plt.subplots()
        sns.countplot(x=df[count_col], ax=ax)

    st.pyplot(fig)