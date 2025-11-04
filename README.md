# Notes Generator

A small Flask app that converts an input PDF into a lined, handwritten-style PDF. The app extracts text from an uploaded PDF and reflows it onto ruled pages using a handwriting font (if provided).

This README explains how to install dependencies and run the project locally on Windows (PowerShell).

## Quick summary
- Start the Flask server, open http://localhost:5000 in your browser, upload a PDF, and download the generated handwritten-styled PDF.

## Prerequisites
- Python 3.9+ (CPython recommended)
- pip
- (Optional but recommended) virtual environment

## Project files
- `app.py` — Flask web app and upload route.
- `format_notes.py` — core logic: extracts text and generates the lined/handwriting-styled PDF.
- `templates/index.html` — frontend upload UI.
- `requirements.txt` — Python dependencies (Flask, PyMuPDF, reportlab, Pillow).
- `Kalam-Regular.ttf` (optional) — a handwriting TTF. If present in the project root it will be used; otherwise the code falls back to a built-in font.

## Install (PowerShell)
Open PowerShell in the project folder (for example `C:\Users\karti\Desktop\notes-generator`) and run:

```powershell
# optional: create and activate a venv (recommended)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install dependencies
pip install -r requirements.txt
```

If you skip the venv, install directly into your system Python environment.

## Run the app (PowerShell)
From the project directory run:

```powershell
python app.py
```

By default the Flask development server starts on http://localhost:5000. Open that URL in your browser to use the upload UI.

## How it works (short)
- The web UI (`templates/index.html`) posts the selected PDF to `/upload`.
- `app.py` saves the uploaded PDF to a temp file and calls `generate_formatted_notes(input_path, output_path)` from `format_notes.py`.
- `format_notes.py` extracts text using PyMuPDF and writes a lined, handwriting-styled PDF using ReportLab.

## Configuration notes
- Secret key: change `app.secret_key` in `app.py` before exposing the app publicly.
- Upload folder: `app.config['UPLOAD_FOLDER']` defaults to the OS temp folder (safe for development). Change it to a persistent folder if you want to keep generated files.
- Max upload size: `MAX_CONTENT_LENGTH` is set to 50 MB by default in `app.py`.
- Handwriting font: place a TTF (e.g. `Kalam-Regular.ttf`) in the project root. `format_notes.py` looks for `Kalam-Regular.ttf` and uses it if present; otherwise it falls back to a built-in font.

## Troubleshooting
- Module import errors: activate your virtualenv (if used) and reinstall with `pip install -r requirements.txt`.
- Permission errors writing files: set `UPLOAD_FOLDER` to a directory where the running user has write permission.
- If resulting PDF is not in a handwriting style, ensure your `.ttf` font file is present and named `Kalam-Regular.ttf`, or update `FONT_FILE` in `format_notes.py`.

## Notes on fidelity and limitations
- This tool extracts selectable text from the input PDF and reflows it into a handwritten-style PDF. That means layout, exact font sizes, and some styling (bold/italic/indentation) may be lost during conversion.
- For scanned PDFs (images), text extraction will produce empty text. To support scanned PDFs you can add an OCR step (Tesseract). I can help add that on request.

## Next steps (optional improvements)
- Add automatic cleanup of generated files after download to avoid disk growth.
- Add an OCR fallback for scanned PDFs.
- Add support to preserve richer formatting (bold, italics, lists) when reflowing text.

## License
Add a license file if you plan to redistribute this project.

---

If you'd like, I can also:
- Run a quick syntax check or start the server here and confirm routes work locally.
- Add a sample PDF to `examples/` and a short integration test that uploads and verifies a generated PDF.

If you want me to apply one of those, tell me which and I'll proceed.