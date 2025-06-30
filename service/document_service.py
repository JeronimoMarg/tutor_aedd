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

    def load_pdf_files(self, pdf_dir: str) -> list[str]:
        text_list = []
        for file in os.listdir(pdf_dir):
            full_path = os.path.join(pdf_dir, file)
            if os.path.isfile(full_path):
                text_list.append(self.extract_text_from_pdf(full_path))

        return text_list


