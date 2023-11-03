from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
import os
import io
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    if 'pdf_file' not in request.files:
        return jsonify({'error': 'No pdf_file in request'}), 400

    pdf_file = request.files['pdf_file']
    folder_name = "files"
    file_name = pdf_file.filename
    if pdf_file.filename == '':
        return jsonify({'error': 'No filename found'}), 400
    if pdf_file and pdf_file.filename.lower().endswith('.pdf') == False:
        return jsonify({'error': 'Invalid file type'}), 400

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
        print(f"Folder '{folder_name}' created.")

    file_extension = os.path.splitext(file_name)[1]
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    file_name_without_extension = os.path.splitext(file_name)[0]
    file_name_with_timestamp = f"{file_name_without_extension}_{current_time}{file_extension}"
    save_path = os.path.join(folder_name, file_name_with_timestamp)
    pdf_file.save(save_path)
    print(f"File save - {save_path}")

    if pdf_file and pdf_file.filename.lower().endswith('.pdf'):
        try:
            pdf_reader = PdfReader(save_path)
            print(pdf_reader, len(pdf_reader.pages))
            data = extract_text_from_pdf(pdf_reader)
            pdf_file.close()
            return jsonify({'content_text': data[0], 'content_appended': data[1], 'save_path': save_path}, 201)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

def extract_text_from_pdf(pdf_reader):
    print("in extract_text_from_pdf")
    text = ""
    pdf_content = []
    print(f"len(pdf_reader.pages) - {len(pdf_reader.pages)}")
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        page_txt = page.extract_text()
        text += page_txt
        pdf_content.append(page_txt)
    return (text, pdf_content)

if __name__ == '__main__':
    app.run(debug=True)
