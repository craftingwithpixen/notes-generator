# app.py
import os
from flask import Flask, request, render_template, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
import tempfile
from format_notes import generate_formatted_notes

ALLOWED_EXTENSIONS = {"pdf"}
UPLOAD_FOLDER = tempfile.gettempdir()  # or set to a persistent folder
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB max

app = Flask(__name__)
app.secret_key = "replace-with-a-secure-random-key"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        tmp_in = os.path.join(app.config["UPLOAD_FOLDER"], f"input_{next(tempfile._get_candidate_names())}_{filename}")
        tmp_out = os.path.join(app.config["UPLOAD_FOLDER"], f"formatted_{next(tempfile._get_candidate_names())}.pdf")
        file.save(tmp_in)

        try:
            # Process synchronously
            generate_formatted_notes(tmp_in, tmp_out)
        except Exception as e:
            # cleanup and show error
            if os.path.exists(tmp_in):
                os.remove(tmp_in)
            flash(f"Error processing file: {e}")
            return redirect(url_for("index"))

        # remove input file, keep output for download
        if os.path.exists(tmp_in):
            os.remove(tmp_in)

        # send the generated file
        return send_file(tmp_out, as_attachment=True, download_name=f"formatted_{filename}")
    else:
        flash("Allowed file: PDF")
        return redirect(request.url)

if __name__ == "__main__":
    # debug only for local development
    app.run(host="0.0.0.0", port=5000, debug=True)
