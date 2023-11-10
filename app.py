import os

from flask import Flask, render_template, url_for, flash, redirect, request, send_from_directory
from PIL import Image


app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['UPLOAD_FOLDER'] = 'compressed'


ALLOWED_EXTENSIONS = {"jpeg", "jpg", "gif", "png"}

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def valid_image(file):
    return file and allowed_file(file.filename)

def compress(input_path, output_path, quality=90):
    try:
        image = Image.open(input_path)
        image.save(output_path, optimize=True, quality=quality)
        return True
    except Exception as error:
        print(f"Compression error: {error}")
        return str(error)

@app.route("/")
def welcome_page():
    return render_template("index.html")

@app.route("/home", methods=["GET", "POST"])
def img_compressor():
    if request.method == "POST":
        uploaded_image = request.files["file"]
        if uploaded_image.filename != "":
            if not valid_image(uploaded_image):
                return "Invalid format", 400

            if not os.path.exists("uploads"):
                os.makedirs("uploads")

            if not os.path.exists("compressed"):
                os.makedirs("compressed")

            input_path = os.path.join("uploads", uploaded_image.filename)
            output_path = os.path.join("compressed", uploaded_image.filename)
            uploaded_image.save(input_path)

            compressed_image = compress(input_path, output_path)
            if compressed_image is True:
                if os.path.exists(output_path):
                    return redirect(url_for("download_compressed", filename=uploaded_image.filename))
                else:
                    return "Error: Compressed image not found", 500
            else:
                print(f"Error: {compressed_image}")
                flash(f"Error: {compressed_image}", "error")
            print(f"Compressed image saved at: {output_path}")

    return render_template("home.html")


@app.route("/download/<filename>")
def download_compressed(filename):
    compression_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
