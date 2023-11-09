import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
import requests
from io import BytesIO
from get_answers import doc_answer
# Set up OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app

folder_path = "uploaded_files"
def save_uploaded_file(uploaded_file, folder_path):
    try:
        with open(os.path.join(folder_path, uploaded_file.name), "wb") as file:
            file.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.write(f"Error: {e}")
        return False
st.title("PDF Question Answering using Generative AI")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF file uploaded successfully! Now you can ask questions based on the content of the document.")
    pdf_content = ""
    save_uploaded_file(uploaded_file, folder_path)
    file_path = os.path.join(folder_path, uploaded_file.name)
    with BytesIO(uploaded_file.read()) as data:
        pdf_reader = PdfReader(data)

        for page in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page].extract_text()

    question = st.text_input("Enter your question:")

    if st.button("Submit"):
        if not question:
            st.warning("Please enter a question.")
        else:
            st.write("Asking your question...")

            doc_answer(uploaded_file.name,file_path)

            # answer = response.choices[0].text.strip()
            st.write(f"Answer: {answer}")
else:
    st.write("Please upload a PDF file.")
