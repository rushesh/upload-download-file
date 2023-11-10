import os
import openai
import streamlit as st
from PyPDF2 import PdfReader
import requests
from io import BytesIO
# Set up OpenAI API
# openai.api_key = os.getenv("OPENAI_API_KEY")
from langchain.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain.document_loaders import TextLoader
from langchain.document_loaders import UnstructuredImageLoader
from langchain.document_loaders import UnstructuredFileLoader
from langchain.document_loaders import PyPDFLoader
import os
# import nltk

os.environ["OPENAI_API_KEY"] = "test_api_key"
embeddings = OpenAIEmbeddings()
chain = load_qa_chain(OpenAI(), chain_type="map_rerank", return_intermediate_steps=True)

def get_file_content(fileName, file):
    if fileName.endswith('.jpg') or fileName.endswith('.jpeg') or fileName.endswith('png'):
        loader = UnstructuredImageLoader(file)
    elif fileName.endswith('pdf'):
        loader = UnstructuredFileLoader(file)
    documents=loader.load()
    document_content = '\n'.join(doc.page_content for doc in documents)
    print("returning from func - get_file_content")
    return document_content

def doc_answer(file_name, file_content, question_query):

    # if runnning this was to extract data pass location i.e.
    # print(f"File Name - {file_name} - file path - {file_path}")
    # file_content=get_file_content(file_name, file_path)
    # print(f"file content")
    # updated_file_content=file_content
    text_splitter = CharacterTextSplitter(
        separator="\n\n", chunk_size=1000, chunk_overlap=200, length_function=len
    )
    file_content_new = file_content[:60:]
    print(f"TYPE OF CONTENT  - {type(file_content_new)} - lenght is - {len(file_content_new)}")
    text_splitter = text_splitter.split_text(file_content_new)
    document_search = FAISS.from_texts(text_splitter, embeddings)
    documents = document_search.similarity_search(question_query)
    results = chain(
        {"input_documents": documents, "question": question_query}, return_only_outputs=True
    )
    answers = results["intermediate_steps"][0]
    return answers

folder_path = "uploaded_files"
def save_uploaded_file(uploaded_file, folder_path):
    try:
        if not os.path.exists(folder_path):
            os.makedirs(folder_path) 
        with open(os.path.join(folder_path, uploaded_file.name), "wb") as file:
            file.write(uploaded_file.getbuffer())
        return True
    except Exception as e:
        st.write(f"Error: {e}")
        return False



st.title("QNA using doc")
st.header('Company Name', divider='rainbow')

uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded_file is not None:
    pdf_content = ""
    save_uploaded_file(uploaded_file, folder_path)
    file_path = os.path.join(folder_path, uploaded_file.name)
    with BytesIO(uploaded_file.read()) as data:
        pdf_reader = PdfReader(data)
        for page in range(len(pdf_reader.pages)):
            pdf_content += pdf_reader.pages[page].extract_text()
    st.text(f"{uploaded_file.name} uploaded successfully")
    st.divider()
    st.markdown(''':red[File] :orange[content] :green[is] :blue[:]''')
    st.text(pdf_content)
    st.divider()
    question = st.text_input("Enter your question:", max_chars=30, help="Max number of characters is 30.")
    if st.button("Submit"):
        if not question:
            st.markdown(''':red[Enter] :violet[your] :green[question]''')
        else:
            st.text("Asking your question...")
            question_query=question
            print(f"Question by user is - {question}")
            answer=doc_answer(uploaded_file.name,pdf_content, question_query)
            print(f"answer - {answer}")
            st.write(f"Answer: {answer}")
else:
    st.text("Please upload a PDF file.")
