from parsers.docx_parser import extract_text_from_docx

def test_extract_text_from_docx():
    text = extract_text_from_docx("sample_files/sample.docx")
    assert isinstance(text, str)
    assert len(text) > 0
