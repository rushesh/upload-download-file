import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
import requests
from io import BytesIO

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Streamlit app
st.title("PDF Question Answering using Generative AI")

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    st.write("PDF file uploaded successfully! Now you can ask questions based on the content of the document.")
    pdf_content = ""

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

            response = openai.Completion.create(
                engine="davinci-codex",
                prompt=f"Document Text:\n{pdf_content}\n\nQuestion: {question}\nAnswer:",
                temperature=0.5,
                max_tokens=150,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )

            answer = response.choices[0].text.strip()
            st.write(f"Answer: {answer}")
else:
    st.write("Please upload a PDF file.")
