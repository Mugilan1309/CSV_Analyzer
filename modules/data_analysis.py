import streamlit as st
import pandas as pd
import io

def show_basic_info(df):
    """Displays dataset information."""
    if st.button("Show Dataset Info"):
        buffer = io.StringIO()
        df.info(buf=buffer)  # Redirects df.info() output to buffer
        info_str = buffer.getvalue()
        st.text(info_str)  # Displays properly in Streamlit


def show_summary(df):
    """Displays summary statistics for both numerical and categorical columns."""
    st.write("### 📊 Data Summary")
    if st.button("Show Summary"):
        numeric_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object']).columns

        if not numeric_cols.empty:
            st.write("#### 🔢 Numerical Columns Summary")
            st.dataframe(df[numeric_cols].describe())  # Standard numeric summary

        if not categorical_cols.empty:
            st.write("#### 🔠 Categorical Columns Summary")
            cat_summary = df[categorical_cols].agg(['nunique', lambda x: x.mode().iloc[0] if not x.mode().empty else None])
            cat_summary.rename(index={'nunique': 'Unique Values', '<lambda_0>': 'Most Frequent (Mode)'}, inplace=True)
            st.dataframe(cat_summary)

def show_missing_values(df):
    """Displays missing value count using Pandas isnull().sum()."""
    st.write("### ❓Missing Values")
    if st.button("Show Missing Values Count"):
        st.write(df.isnull().sum())
