import pandas as pd
import streamlit as st

def load_data(uploaded_file):
    """Loads CSV file and returns a Pandas DataFrame."""
    try:
        df = pd.read_csv(uploaded_file)
        if len(df) > 1000:
            st.warning("Dataset is large! Loading first 1000 rows for performance.")
            df = df.head(1000)
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None
