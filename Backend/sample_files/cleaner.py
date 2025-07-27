import re

def clean_text(text):
    text = re.sub(r'\s+', ' ', text)  # Replace multiple whitespaces with single space
    text = text.replace('\x0c', ' ')  # Remove form feed
    return text.strip()

def chunk_text(text, chunk_size=750):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
