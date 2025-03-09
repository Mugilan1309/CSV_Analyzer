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
    """Displays statistical summary using Pandas describe()."""
    if st.button("Show Summary Statistics"):
        st.write(df.describe())

def show_missing_values(df):
    """Displays missing value count using Pandas isnull().sum()."""
    if st.button("Show Missing Values Count"):
        st.write(df.isnull().sum())
