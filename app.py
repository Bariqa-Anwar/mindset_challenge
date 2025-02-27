import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up the app
st.set_page_config(page_title="Data Cleaner & Transformer", layout='wide')

# Custom CSS for contrast UI
st.markdown(
    """
    <style>
        .stApp {
            background-color: #fffbea;
            padding: 20px;
        }
        .main-title {
            font-size: 32px;
            font-weight: bold;
            text-align: center;
            color: #ffcc00;
        }
        .stSidebar {
            background-color: #fff5cc;
            padding: 20px;
            border-radius: 10px;
        }
        .custom-box {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='main-title'>Data Cleaner & Transformer</div>", unsafe_allow_html=True)
st.write("### Clean, Analyze, and Transform Your Data")

# Sidebar sections
st.sidebar.subheader("Share Your Feedback")
feedback = st.sidebar.text_area("Your Feedback:")
if st.sidebar.button("Submit Feedback"):
    st.sidebar.success("Thank you for your feedback!")

st.sidebar.subheader("How to Use This App")
if st.sidebar.checkbox("Show Help"):
    st.sidebar.info(
        """
        **Steps to Use:**
        1. Upload CSV, Excel, or JSON files.
        2. Preview the file and clean the data.
        3. Select the columns you need.
        4. Explore the data with visualizations.
        5. Export the cleaned file in CSV or Excel format.
        """
    )

# File uploader
uploaded_files = st.file_uploader(
    "Upload Your Data Files (CSV, Excel, or JSON):", 
    type=["csv", "xlsx", "json"], 
    accept_multiple_files=True
)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        df = None

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        elif file_ext == ".json":
            df = pd.read_json(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        with st.container():
            st.markdown("<div class='custom-box'>", unsafe_allow_html=True)
            st.write(f"**File Name:** {file.name}  |  **Size:** {file.size / 1024:.2f} KB")
            st.dataframe(df.head())
            st.markdown("</div>", unsafe_allow_html=True)

        st.subheader("Data Cleaning & Preparation")
        col1, col2 = st.columns(2)
        with col1:
            if st.button(f"Remove Duplicates from {file.name}"):
                df.drop_duplicates(inplace=True)
                st.success("Duplicates Removed!")
        with col2:
            if st.button(f"Fill Missing Values for {file.name}"):
                numeric_cols = df.select_dtypes(include=['number']).columns
                df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                st.success("Missing Values Filled!")

        st.subheader("Select Columns to Keep or Transform")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        st.subheader("Explore Your Data with Visualizations")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        st.subheader("Export Your Data")
        export_type = st.radio(f"Export {file.name} as:", ["CSV", "Excel"], key=file.name)
        if st.button(f"Export {file.name}"):
            buffer = BytesIO()
            try:
                if export_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                else:
                    df.to_excel(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                st.download_button(
                    label=f"Download {file.name} as {export_type}",
                    data=buffer,
                    file_name=file_name,
                    mime=mime_type
                )
                st.success("File exported successfully!")
            except ImportError:
                st.error("The 'openpyxl' library is required for exporting Excel files. Install it using `pip install openpyxl`.")
