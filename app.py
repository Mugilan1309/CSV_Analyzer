import streamlit as st
import pandas as pd
from modules.data_loader import load_data
from modules.data_analysis import show_basic_info, show_summary, show_missing_values
from modules.preprocessing import handle_missing_values, scale_data
from modules.visualization import plot_data

# Configure page layout
st.set_page_config(page_title="CSV Data Analyzer", layout="wide")

# Custom Styled Header
st.markdown(
    """
    <h1 style='text-align: center; color: #4CAF50;'>CSV Data Analyzer & Preprocessor</h1>
    <p style='text-align: center; font-size:18px;'>Easily analyze, preprocess, and visualize your CSV data with just a few clicks! 📊</p>
    """, unsafe_allow_html=True
)

# Sidebar Navigation
st.sidebar.title("📊 CSV Data Analyzer & Preprocessor")
option = st.sidebar.radio("Choose Operation", 
                          ["📂 View Data", "📈 Basic Analysis", "🛠️ Preprocessing", "📊 Visualization", "📥 Download"])

# File Upload Section (Centered)
st.markdown("<h2 style='text-align: center;'>📂 Upload Your CSV File</h2>", unsafe_allow_html=True)
uploaded_file = st.file_uploader("", type=["csv"], help="Upload a CSV file to start processing.")

if uploaded_file:
    with st.spinner("📊 Loading data..."):
        df = load_data(uploaded_file)
        st.success("✅ File uploaded successfully!")

    # View Data Section
    if option == "📂 View Data":
        st.subheader("Dataset Preview")
        rows = st.slider("Number of rows to display:", 5, len(df), 10)  # Let users choose rows
        st.dataframe(df.head(rows))

    # Basic Analysis Section
    elif option == "📈 Basic Analysis":
        st.subheader("🔎 Dataset Information")
        show_basic_info(df)
        show_summary(df)
        show_missing_values(df)

    # Preprocessing Section
    elif option == "🛠️ Preprocessing":
        st.title("🛠️ Data Preprocessing")

        # Apply Missing Value Handling
        df = handle_missing_values(df)

        # Apply Scaling
        df = scale_data(df)

        # Display updated dataset
        st.write("### Processed Data Preview")
        st.dataframe(df)

    # Visualization Section
    elif option == "📊 Visualization":
        st.subheader("📊 Data Visualization")
        plot_data(df)

    # Download Section
    elif option == "📥 Download":
        st.subheader("📥 Download Processed Data")

        # Let users select preprocessing steps before downloading
        st.write("### Select Preprocessing Steps to Apply:")
        
        col1, col2 = st.columns(2)
        with col1:
            apply_missing_values = st.checkbox("Handle Missing Values")
        with col2:
            apply_scaling = st.checkbox("Scale Numeric Data")

        df_processed = df.copy()  # Create a copy to apply transformations

        # Apply selected preprocessing steps
        if apply_missing_values:
            df_processed = handle_missing_values(df_processed)
        if apply_scaling:
            df_processed = scale_data(df_processed)

        # Show a full preview of processed rows (only changed ones)
        st.write("### Processed Data Preview")
        st.dataframe(df_processed[df_processed.ne(df).any(axis=1)])  # Show only modified rows

        # Convert processed data to CSV
        csv = df_processed.to_csv(index=False).encode("utf-8")

        # Center the download button
        col1, col2, col3 = st.columns([1, 3, 1])
        with col2:
            st.download_button(
                label="📥 Download Processed CSV",
                data=csv,
                file_name="processed_data.csv",
                mime="text/csv",
            )

        st.success("✅ Your processed CSV is ready for download!")

else:
    st.info("Please upload a CSV file.")
