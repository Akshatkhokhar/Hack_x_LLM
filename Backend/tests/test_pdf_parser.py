from parsers.pdf_parser import extract_text_from_pdf

def test_extract_text_from_pdf():
    text = extract_text_from_pdf("sample_files/sample.pdf")
    assert isinstance(text, str)
    assert len(text) > 0
