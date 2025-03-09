import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler

def handle_missing_values(df):
    """Handles missing values separately for numerical and categorical columns without errors."""
    st.write("### 🛠️ Handle Missing Values")
    
    method = st.selectbox("Choose Method", ["None", "Fill with Mean (Numeric)", "Fill with Median (Numeric)", "Fill with Mode (Categorical)", "Drop Rows"])

    if method != "None":
        df_copy = df.copy()

        # Identify numeric and categorical columns
        numeric_cols = df_copy.select_dtypes(include=['number']).columns
        categorical_cols = df_copy.select_dtypes(exclude=['number']).columns

        missing_before = df_copy.isnull().sum().sum()  # Count total missing before

        if method in ["Fill with Mean (Numeric)", "Fill with Median (Numeric)"] and numeric_cols.empty:
            st.warning("⚠️ No numeric columns available to apply mean/median. Please select another method.")
            return df
        
        if method == "Fill with Mode (Categorical)" and categorical_cols.empty:
            st.warning("⚠️ No categorical columns available to apply mode. Please select another method.")
            return df
        
        if method == "Fill with Mean (Numeric)":
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].mean())
        
        elif method == "Fill with Median (Numeric)":
            df_copy[numeric_cols] = df_copy[numeric_cols].fillna(df_copy[numeric_cols].median())

        elif method == "Fill with Mode (Categorical)":
            for col in categorical_cols:
                if not df_copy[col].mode().empty:
                    df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
                else:
                    st.warning(f"⚠️ Column `{col}` has no mode, filling with 'Unknown'.")
                    df_copy[col] = df_copy[col].fillna("Unknown")

        elif method == "Drop Rows":
            df_copy.dropna(inplace=True)

        missing_after = df_copy.isnull().sum().sum()  # Count total missing after

        # Show affected rows
        changed_rows = df_copy[df.isnull().any(axis=1)]
        if not changed_rows.empty:
            st.write("### 🔄 Affected Rows After Preprocessing:")
            st.dataframe(changed_rows)
        else:
            st.success("✅ No missing values detected!")

        st.write(f"🔍 Missing values before: `{missing_before}`, After: `{missing_after}`")
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
