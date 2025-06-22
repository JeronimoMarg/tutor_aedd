import fitz
import os

class DocumentService(object):
    def __init__(self):
        pass

    def extract_text_from_pdf(self, path):
        doc = fitz.open(path)
        text = ""
        for page in doc:
            text += page.get_text()
        return text

    def load_pdf_files(self, pdf_dir):
        pass

