# format_notes.py
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import io
from PIL import Image

# Register font (place Kalam-Regular.ttf or any handwriting ttf in same folder)
FONT_NAME = "Kalam"
FONT_FILE = "Kalam-Regular.ttf"
if os.path.exists(FONT_FILE):
    pdfmetrics.registerFont(TTFont(FONT_NAME, FONT_FILE))
else:
    # fallback to built-in if custom font missing
    FONT_NAME = "Helvetica-Oblique"

def extract_text_from_pdf(pdf_path):
    """Extract plain text from a PDF using PyMuPDF"""
    text = ""
    with fitz.open(pdf_path) as doc:
        for p in doc:
            text += p.get_text("text") + "\n"
    return text

def draw_lined_background(c, page_size=A4, line_gap=20, left_margin=70):
    """Draw simple ruled lines and a left margin line"""
    width, height = page_size
    c.setStrokeColorRGB(0.85, 0.85, 0.85)
    c.setLineWidth(0.5)
    for y in range(50, int(height) - 50, line_gap):
        c.line(40, y, width - 40, y)

    # optional red margin line
    c.setStrokeColorRGB(1, 0.2, 0.2)
    c.setLineWidth(1)
    c.line(left_margin, 40, left_margin, height - 40)

def create_handwritten_pdf_from_text(text, output_path, page_size=A4, font_name=FONT_NAME):
    """Write extracted text onto lined pages using handwriting font"""
    c = canvas.Canvas(output_path, pagesize=page_size)
    width, height = page_size

    line_gap = 20  # spacing between ruled lines -> also text line-height
    left_margin = 80
    right_margin = 40
    top_margin = 60
    bottom_margin = 60
    font_size = 14

    # split text into lines. We'll do a naive wrap to page width.
    # ReportLab measures width to wrap longer lines to fit.
    from reportlab.pdfbase.pdfmetrics import stringWidth

    draw_lined_background(c, page_size, line_gap=line_gap, left_margin=left_margin)
    c.setFont(font_name, font_size)

    y = height - top_margin

    for paragraph in text.split("\n"):
        if not paragraph.strip():
            # empty line -> skip one ruled line space
            y -= line_gap
            if y < bottom_margin:
                c.showPage()
                draw_lined_background(c, page_size, line_gap=line_gap, left_margin=left_margin)
                c.setFont(font_name, font_size)
                y = height - top_margin
            continue

        # naive wrapping based on characters -> use width measurement for better results
        words = paragraph.strip().split(" ")
        current_line = ""
        for w in words:
            test_line = (current_line + " " + w).strip()
            # measure width
            if stringWidth(test_line, font_name, font_size) < (width - left_margin - right_margin):
                current_line = test_line
            else:
                # write current_line
                if y < bottom_margin:
                    c.showPage()
                    draw_lined_background(c, page_size, line_gap=line_gap, left_margin=left_margin)
                    c.setFont(font_name, font_size)
                    y = height - top_margin
                c.drawString(left_margin + 10, y, current_line)
                y -= line_gap
                current_line = w

        # write last part of paragraph
        if current_line:
            if y < bottom_margin:
                c.showPage()
                draw_lined_background(c, page_size, line_gap=line_gap, left_margin=left_margin)
                c.setFont(font_name, font_size)
                y = height - top_margin
            c.drawString(left_margin + 10, y, current_line)
            y -= line_gap

    c.save()

def generate_formatted_notes(input_pdf_path, output_pdf_path):
    """Main helper: extract text and create formatted pdf"""
    text = extract_text_from_pdf(input_pdf_path)
    create_handwritten_pdf_from_text(text, output_pdf_path)
