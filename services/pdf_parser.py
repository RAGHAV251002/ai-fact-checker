import fitz  # PyMuPDF


def extract_text_from_pdf(uploaded_file):
    """
    Extract text from an uploaded PDF file.

    Parameters:
        uploaded_file: Streamlit UploadedFile object

    Returns:
        str: Extracted text
    """

    try:
        pdf = fitz.open(stream=uploaded_file.read(), filetype="pdf")

        text = ""

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"Error reading PDF: {e}")