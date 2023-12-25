import sys
import tkinter as tk
from tkinter import ttk
from pdfminer.high_level import extract_text
import fitz  # PyMuPDF
from PIL import Image, ImageTk

def extract_text_from_page(pdf_path, page_number):
    try:
        text = extract_text(pdf_path, page_numbers=[page_number])
        return text
    except Exception as e:
        print(f"Error extracting text from page {page_number}: {e}", flush=True)
        return ""

def load_pdf_page_image(pdf_path, page_number):
    try:
        print(f"Loading page {page_number}...", flush=True)
        pdf_document = fitz.open(pdf_path)
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        pdf_document.close()
        return img
    except Exception as e:
        print(f"Error loading PDF page {page_number} as image: {e}", flush=True)
        return None
    
class PDFTranslatorApp(tk.Tk):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.title("PDF Translator")
        self.geometry("800x600")
        self.create_widgets()

    def create_widgets(self):
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        pdf_document = fitz.open(self.pdf_path)

        for i in range(len(pdf_document)):
            page_frame = ttk.Frame(self.notebook)
            self.notebook.add(page_frame, text=f'Page {i + 1}')

            # Display PDF Page Image
            img = load_pdf_page_image(self.pdf_path, i)
            img = ImageTk.PhotoImage(img)
            image_label = ttk.Label(page_frame, image=img)
            image_label.image = img  # Keep reference
            image_label.pack(side='left')

            # Display Text Area with inverted colors
            text = extract_text_from_page(self.pdf_path, i)
            text_area = tk.Text(page_frame, wrap='word', fg='white', bg='black')
            text_area.insert('1.0', text)
            text_area.pack(side='right', fill='both', expand=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path_to_your_pdf.pdf", flush=True)
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    try:
        app = PDFTranslatorApp(pdf_file_path)
        app.mainloop()
    except Exception as e:
        print(f"Error initializing PDFTranslatorApp: {e}", flush=True)