import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def handle_missing_values(df):
    """Handles missing values in the dataset."""
    st.write("### Handle Missing Values")
    method = st.selectbox("Choose Method", ["None", "Fill with Mean", "Fill with Median", "Drop Rows"])

    if method != "None":
        df_copy = df.copy()
        missing_before = df_copy.isnull().sum().sum()  # Count missing values before

        if method == "Fill with Mean":
            df_copy.fillna(df_copy.mean(), inplace=True)
        elif method == "Fill with Median":
            df_copy.fillna(df_copy.median(), inplace=True)
        elif method == "Drop Rows":
            df_copy.dropna(inplace=True)

        missing_after = df_copy.isnull().sum().sum()  # Count missing values after

        # Show only affected rows
        changed_rows = df_copy[df.isnull().any(axis=1)]  
        if not changed_rows.empty:
            st.write("### Affected Rows After Preprocessing:")
            st.dataframe(changed_rows)
        else:
            st.success("No missing values detected!")

        st.write(f"Missing values before: {missing_before}, After: {missing_after}")
        return df_copy
    
    return df

def scale_data(df):
    """Scales numeric data using Standardization or Normalization."""
    st.write("### Scale Data")
    method = st.selectbox("Choose Scaling Method", ["None", "Standardization", "Normalization"])

    if method != "None":
        df_copy = df.copy()
        numeric_cols = df_copy.select_dtypes(include=['number']).columns

        if method == "Standardization":
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()

        df_copy[numeric_cols] = scaler.fit_transform(df_copy[numeric_cols])

        st.write("Scaled Dataset:")
        st.dataframe(df_copy.head())
        return df_copy
    
    return df
