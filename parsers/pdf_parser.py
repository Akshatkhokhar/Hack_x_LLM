import PyPDF2

def extract_text_from_pdf(file_path):
    text = ""
    with open(file_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            content = page.extract_text()
            if content:
                text += content + "\n"
    return text
