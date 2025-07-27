import os
import json
from PyPDF2 import PdfReader
from docx import Document

# ========== TEXT EXTRACTORS ========== #
def extract_text_from_pdf(file_path):
    try:
        reader = PdfReader(file_path)
        pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            pages.append({"page_num": i + 1, "text": text.strip()})
        return pages
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

def extract_text_from_docx(file_path):
    try:
        doc = Document(file_path)
        full_text = "\n".join([para.text for para in doc.paragraphs])
        return [{"page_num": 1, "text": full_text.strip()}]  # Treat DOCX as one page
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return []

# ========== TEXT CHUNKER ========== #
def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = start + chunk_size
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

# ========== MAIN PARSER ========== #
def parse_and_save_all_docs(folder_path):
    os.makedirs("parsed_output", exist_ok=True)

    for file in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file)
        extension = os.path.splitext(file)[1].lower()
        pages = []

        if extension == ".pdf":
            pages = extract_text_from_pdf(file_path)
        elif extension == ".docx":
            pages = extract_text_from_docx(file_path)
        else:
            print(f"⚠️ Skipping unsupported file: {file}")
            continue

        print(f"✅ Parsed: {file}")

        all_chunks = []
        chunk_index = 0

        for page in pages:
            page_num = page["page_num"]
            text = page["text"]
            chunks = chunk_text(text)

            for chunk in chunks:
                all_chunks.append({
                    "file": file,
                    "chunk_index": chunk_index,
                    "text": chunk,
                    "metadata": {
                        "source": file,
                        "page": page_num
                    }
                })
                chunk_index += 1

        # Save JSON
        json_path = os.path.join("parsed_output", f"{os.path.splitext(file)[0]}_chunked.json")
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(all_chunks, f, indent=2, ensure_ascii=False)

        print(f"📝 Chunked JSON saved to: {json_path}\n")

# ========== RUN ========== #
if __name__ == "__main__":
    parse_and_save_all_docs("docs")
