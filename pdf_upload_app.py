import os
import streamlit as st
from PyPDF2 import PdfReader

def save_uploaded_file(uploaded_file, folder_path):
    try:
        with open(os.path.join(folder_path, uploaded_file.name), "wb") as file:
            file.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.write(f"Error: {e}")
        return False

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PdfReader(file)
        pages = len(pdf_reader.pages)
        content = ""
        for page_num in range(pages):
            page = pdf_reader.pages[page_num]
            content += page.extract_text()

    return content

st.title("PDF Upload and Display")
folder_path = "uploaded_files"

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file is not None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    if save_uploaded_file(uploaded_file, folder_path):
        st.write("File uploaded successfully.")
        file_path = os.path.join(folder_path, uploaded_file.name)
        pdf_content = read_pdf(file_path)
        st.write("PDF Content:")
        st.write(pdf_content)
