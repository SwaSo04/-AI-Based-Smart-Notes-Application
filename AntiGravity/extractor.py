import warnings
warnings.filterwarnings("ignore")

try:
    import pymupdf as fitz
except ImportError:
    import fitz

import re

def extract_text_from_pdf(file_bytes):
    """
    Extracts and cleans text from PDF bytes using PyMuPDF.
    """
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    full_text = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text")
        if text:
            full_text.append(text)

    raw_text = "\n".join(full_text)
    
    # Preprocessing: Clean extra spaces, redundant linebreaks
    cleaned = re.sub(r'\n{3,}', '\n\n', raw_text)
    cleaned = re.sub(r'[ \t]+', ' ', cleaned)
    
    return cleaned.strip()
