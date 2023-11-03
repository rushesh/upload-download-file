const fileInput = document.getElementById('file-input');
const uploadButton = document.getElementById('upload-button');
const savePath = document.getElementById('savePath');
const pdfContent = document.getElementById('pdfContent');

uploadButton.addEventListener('click', async () => {
    if (!fileInput.files[0]) {
        statusText.textContent = 'No file selected';
        return;
    }
    const formData = new FormData();
    formData.append('pdf_file', fileInput.files[0]);
    try {
        const response = await fetch('http://localhost:5000/upload_pdf', {
            method: 'POST',
            body: formData
        });
        if (!response.ok) {
            throw new Error('An error occurred while uploading the file');
        }

        const result = await response.json();
        console.log('result - ',result);
        savePath.textContent = "File saved at -  " + result[0].save_path;
        pdfContent.textContent = "File content_text -  " + result[0].content_text;
    } catch (error) {
        savePath.textContent = error.message;
    }
});
