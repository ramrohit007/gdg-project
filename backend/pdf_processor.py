import pdfplumber
import PyPDF2
from typing import Optional
import os

class PDFProcessor:
    """Handles PDF to text conversion"""
    
    def pdf_to_text(self, file_path: str) -> str:
        """
        Convert PDF to text using multiple methods for better accuracy
        """
        text = ""
        
        # Try pdfplumber first (better for text extraction)
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Error with pdfplumber: {e}")
        
        # Fallback to PyPDF2 if pdfplumber fails or text is empty
        if not text.strip():
            try:
                with open(file_path, 'rb') as file:
                    pdf_reader = PyPDF2.PdfReader(file)
                    for page in pdf_reader.pages:
                        text += page.extract_text() + "\n"
            except Exception as e:
                print(f"Error with PyPDF2: {e}")
        
        if not text.strip():
            raise ValueError("Could not extract text from PDF")
        
        return text.strip()

