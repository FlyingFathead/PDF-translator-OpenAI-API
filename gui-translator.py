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
    
# create the class
class PDFTranslatorApp(tk.Tk):
    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path
        self.title("PDF Translator")
        self.geometry("800x600")
        
        self.pdf_document = fitz.open(self.pdf_path)
        self.pdf_pages = len(self.pdf_document)

        self.create_widgets()

    def create_widgets(self):
        # Navigation panel
        navigation_frame = ttk.Frame(self)
        navigation_frame.pack(side='top', fill='x')

        # First page button
        first_page_button = ttk.Button(navigation_frame, text='|<', command=self.first_page)
        first_page_button.pack(side='left')

        # Previous page button
        prev_page_button = ttk.Button(navigation_frame, text='<', command=self.prev_page)
        prev_page_button.pack(side='left')

        # Page number entry
        self.page_number_var = tk.StringVar()
        self.page_number_entry = ttk.Entry(navigation_frame, textvariable=self.page_number_var, width=5)
        self.page_number_entry.bind('<Return>', self.jump_to_page)
        self.page_number_entry.pack(side='left')

        # Total pages label
        total_pages_label = ttk.Label(navigation_frame, text=f' / {self.pdf_pages}')
        total_pages_label.pack(side='left')

        # Next page button
        next_page_button = ttk.Button(navigation_frame, text='>', command=self.next_page)
        next_page_button.pack(side='left')

        # Last page button
        last_page_button = ttk.Button(navigation_frame, text='>|', command=self.last_page)
        last_page_button.pack(side='left')

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # Move the for loop here, to create content when the GUI initializes
        for i in range(self.pdf_pages):
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

    def first_page(self):
        self.notebook.select(0)

    def last_page(self):
        self.notebook.select(self.pdf_pages - 1)

    def prev_page(self):
        current = self.notebook.index(self.notebook.select())
        self.notebook.select(max(0, current - 1))

    def next_page(self):
        current = self.notebook.index(self.notebook.select())
        self.notebook.select(min(self.pdf_pages - 1, current + 1))

    def jump_to_page(self, event=None):
        page = int(self.page_number_var.get()) - 1
        self.notebook.select(max(0, min(self.pdf_pages - 1, page)))

        pdf_document = fitz.open(self.pdf_path)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py path_to_your_pdf.pdf", flush=True)
        sys.exit(1)

    pdf_file_path = sys.argv[1]
    try:
        pdf_document = fitz.open(pdf_file_path)
        pdf_pages = len(pdf_document)
        pdf_document.close()
        print(f"PDF file opened with a total of {pdf_pages} pages.", flush=True)
        
        app = PDFTranslatorApp(pdf_file_path)
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}", flush=True)