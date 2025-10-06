from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

import os


from practicals import *


def create_blank_slide_with_lines(width, height):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFont("Helvetica", 10)

    num_lines = 6
    line_height = 85
    margin = 40
    margin_top = 85
    c.setLineWidth(2)

    for i in range(num_lines):
        c.line(margin, height - (i * line_height) - margin_top, width - margin, height - (i * line_height) - margin_top)

    c.save()
    packet.seek(0)
    return packet

def create_title_slide(width, height, title):
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=(width, height))
    c.setFont("Helvetica-Bold", 24)
    text_width = c.stringWidth(title, "Helvetica-Bold", 24)
    c.drawString((width - text_width) / 2, height / 2, title)
    c.save()
    packet.seek(0)
    return packet

def insert_handouts_from_list(input_pdf_paths:list, output_path, addTitles = False, overwrite = False):
        writer = PdfWriter()

        for input_pdf_path in input_pdf_paths:

            if os.path.splitext(os.path.basename(output_path))[0] in input_pdf_path:    #if there's a file with combined_handout in it, it's likely an older combined handout. To avoid mistakes and large files i'ts ignored
                print(f"Found and ignored a file contaning \"{output_path}\": {input_pdf_path}")
                continue

            reader = PdfReader(input_pdf_path)
            first_page = reader.pages[0]
            width = float(first_page.mediabox[2])
            height = float(first_page.mediabox[3])

            #adds first page
            writer.add_page(first_page)

            if addTitles:
                # Add title slide with filename
                title = os.path.basename(input_pdf_path)
                title_slide = create_title_slide(width, height, title)
                title_slide_pdf = PdfReader(title_slide)
                writer.add_page(title_slide_pdf.pages[0])

            # Create blank slide template
            blank_slide = create_blank_slide_with_lines(width, height)

            for page in reader.pages[1:]:
                writer.add_page(page)
                blank_slide_pdf = PdfReader(blank_slide)
                writer.add_page(blank_slide_pdf.pages[0])

        try:
            with open(output_path,"wb") as output:
                writer.write(output)
        except FileNotFoundError:
            print(f"[ERROR] The file called {output} was not found. Please check if the file exists and if you're working in the right directory.S")