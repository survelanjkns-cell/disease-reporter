import streamlit as st
import pandas as pd

st.set_page_config(page_title="Wabak Report Generator", layout="centered")

st.title("📄 Disease Report Generator")
st.write("Upload your Excel file to generate the Selangor Disease Table.")

# 1. File Uploader
uploaded_file = st.file_uploader("Drop your Excel file here", type=["xlsx"])

if uploaded_file:
    try:
        # 2. Read the specific sheet
        df = pd.read_excel(uploaded_file, sheet_name="SELANGOR 2")
        
        # 3. Process Column F (Penyakit)
        # We use iloc[:, 5] because F is the 6th column (0-indexed)
        disease_col = df.iloc[:, 5].dropna().astype(str)
        
        # Clean data: Remove the header if it's in the rows and strip spaces
        disease_col = disease_col[disease_col.str.upper() != "PENYAKIT"]
        disease_counts = disease_col.value_counts().reset_index()
        disease_counts.columns = ['Disease Name', 'Cumulative Count']

        # 4. Display Results
        st.subheader("Summary Table: SELANGOR 2")
        st.table(disease_counts)

        # 5. Export to CSV (Simple alternative to PDF for now)
        csv = disease_counts.to_csv(index=False).encode('utf-8')
        st.download_button("Download Report as CSV", data=csv, file_name="disease_report.csv")

    except Exception as e:
        st.error(f"Error: Could not find 'SELANGOR 2' or Column F. {e}")
