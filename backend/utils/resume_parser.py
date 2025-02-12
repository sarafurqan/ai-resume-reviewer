import fitz  # PyMuPDF for PDF parsing
from io import BytesIO
from docx import Document

def extract_text_from_pdf(pdf_file):
    """Extracts text from a PDF file."""
    doc = fitz.open(stream=pdf_file, filetype="pdf")
    text = "\n".join([page.get_text("text") for page in doc])
    return text.strip()

def extract_text_from_docx(docx_file):
    """Extracts text from a DOCX file."""
    doc = Document(BytesIO(docx_file))
    text = "\n".join([para.text for para in doc.paragraphs])
    return text.strip()

def parse_resume(file_bytes, file_type):
    """Determines the resume type and extracts text accordingly."""
    if file_type == "pdf":
        return extract_text_from_pdf(file_bytes)
    elif file_type == "docx":
        return extract_text_from_docx(file_bytes)
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or DOCX.")
