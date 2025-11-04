# Notes Generator

A small Flask app that converts an input PDF into a lined, handwritten-style PDF (extracts text and renders it using a handwriting font onto ruled pages).

This README explains how to install dependencies and run the project locally on Windows (PowerShell).

## What this project does
- Accepts a PDF upload via the web UI.
- Extracts text from the PDF and reflows it into a lined page layout using a handwriting font.
- Returns a generated PDF download (handwritten-styled, lined pages).

Important: the app currently does NOT create Word documents. It always produces a PDF file.

## Prerequisites
- Python 3.9+ (tested on CPython)
- pip
- (Optional) A virtual environment is strongly recommended

## Files of interest
- `app.py` — Flask web application and upload route.
- `format_notes.py` — core logic: extracts text and generates the lined/handwritten PDF.
- `templates/index.html` — simple front-end for uploading PDFs.
- `requirements.txt` — Python dependencies.
- `Kalam-Regular.ttf` (optional) — a handwriting TTF. If present in the project folder it will be used; otherwise the code falls back to a built-in font.

## Install dependencies (PowerShell)
Open PowerShell in the project folder (for example `C:\Users\karti\Desktop\notes generator`) and run:

```powershell
# optional: create and activate a venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r "C:\Users\karti\Desktop\notes generator\requirements.txt"
```

Note: If you created a virtual environment, make sure to activate it each time before running the app.

## Running the app (PowerShell)
From the project directory:

```powershell
python "C:\Users\karti\Desktop\notes generator\app.py"
```

By default the Flask development server will start at `http://localhost:5000`.

Open that address in your browser and use the upload control to select a PDF, then click "Upload & Convert". The server will respond with a generated PDF for download.

## Configuration notes
- `app.secret_key` in `app.py`: change to a secure random key before deploying publicly.
- `UPLOAD_FOLDER` in `app.py` uses the OS temp directory by default. You can change it to a persistent folder if you want to keep outputs.
- `MAX_CONTENT_LENGTH` in `app.py` limits the upload size (default 50 MB). Adjust as needed.
- Handwriting font: place a TTF file (e.g., `Kalam-Regular.ttf`) in the project folder; the code will register and use it automatically. If not present the app falls back to a built-in font and the output will still work but will not look like handwriting.

## Behavior and fidelity
This tool extracts the plain text from the PDF and reflows it into the handwriting font on ruled pages. That means:
- Text content is preserved, but original visual styles (bold/italic, bullet indentation, exact font faces) are not guaranteed to be exactly retained in the generated PDF.
- If you need an exact visual replica of the input PDF (bit-for-bit), we can instead render each page as an image and overlay lined paper; that option is available but creates a non-selectable (image) PDF.

If your requirement is to exactly preserve bold, bullets and sizes in the output PDF as selectable text, we can implement a more advanced pipeline (parsing font spans and mapping them to ReportLab styling). Tell me if you want that and I will add it.

## Troubleshooting
- If uploads fail with an error about missing modules, re-run the pip install step and verify the active Python interpreter (especially inside a virtualenv).
- If the server reports a permissions error writing to the temp folder, set `UPLOAD_FOLDER` in `app.py` to a folder where the Flask process has write permissions.
- If the handwriting font doesn't show, ensure the TTF file name in the project root matches the `FONT_FILE` variable in `format_notes.py` or update the code to point to your font file.

## License
This project is provided as-is for personal use. Add a license file if you plan to redistribute.

## Next steps (optional)
- Add a background cleanup job to remove temporary generated files after download.
- Add an OCR fallback (Tesseract) for scanned PDFs with no selectable text.
- Implement an alternate pipeline that preserves original PDF styles in a regenerated, selectable PDF.

---
If you want, I can now run a quick syntax check for the repository and/or walk you through testing with a sample PDF.