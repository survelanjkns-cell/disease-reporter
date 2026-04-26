import streamlit as st
import pandas as pd
from fpdf import FPDF
import base64

st.set_page_config(page_title="Wabak Report Generator", layout="centered")

def create_pdf(df):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 16)
    
    # Title
    pdf.cell(190, 10, "Laporan Ringkasan Penyakit (SELANGOR 2)", ln=True, align="C")
    pdf.ln(10)
    
    # Table Header
    pdf.set_font("Arial", "B", 12)
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(140, 10, "Nama Penyakit", 1, 0, "C", True)
    pdf.cell(50, 10, "Jumlah", 1, 1, "C", True)
    
    # Table Body
    pdf.set_font("Arial", "", 12)
    for index, row in df.iterrows():
        pdf.cell(140, 10, str(row['Disease Name']), 1)
        pdf.cell(50, 10, str(row['Cumulative Count']), 1, 1, "C")
    
    return pdf.output(dest="S").encode("latin-1")

st.title("📄 Disease Report Generator")

uploaded_file = st.file_uploader("Drop your Excel file here", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file, sheet_name="SELANGOR 2")
        
        # Data Processing
        disease_col = df.iloc[:, 5].dropna().astype(str)
        disease_col = disease_col[disease_col.str.upper() != "PENYAKIT"]
        disease_counts = disease_col.value_counts().reset_index()
        disease_counts.columns = ['Disease Name', 'Cumulative Count']

        # Display Table
        st.subheader("Summary Table: SELANGOR 2")
        st.table(disease_counts)

        # PDF Generation
        pdf_data = create_pdf(disease_counts)
        
        st.download_button(
            label="Download Report as PDF",
            data=pdf_data,
            file_name="Laporan_Penyakit_Selangor.pdf",
            mime="application/pdf",
        )

    except Exception as e:
        st.error(f"Error processing file: {e}")
