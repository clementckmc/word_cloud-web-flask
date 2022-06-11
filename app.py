import os
from flask import Flask, flash, jsonify, redirect, render_template, request, send_from_directory, url_for
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.utils import secure_filename
    
from generate import apology, wc_txt, wc_doc, wc_pdf

# file uploading
script_dir = os.path.dirname(__file__)
rel_path = "static\\tmp"
UPLOAD_FOLDER = os.path.join(script_dir, rel_path)
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx', 'jpeg', 'gif', 'png', 'jpg'}

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# file uploading
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 

# set files allowed
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/upload", methods=["GET", "POST"])
def upload():
    # upload page
    if request.method == "GET":
        return render_template("upload.html")
    else:
        # get file
        if request.files:
            textfile = request.files["textfile"]
            mask = request.files["mask"]

            # ensure and secure file
            if textfile.filename == "":
                flash("No selected file")
                return redirect(request.url)
            
            if not allowed_file(textfile.filename):
                flash("file type not allowed")
                return redirect(request.url)
            
            else:
                filename = secure_filename(textfile.filename)
                maskname = secure_filename(mask.filename)
                lang = request.form.get("lang")
                # without mask
                if maskname == "":
                    textfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return redirect(url_for("uploaded_file", filename=filename, lang=lang))
                # with mask
                else:
                    textfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    mask.save(os.path.join(app.config['UPLOAD_FOLDER'], maskname))
                    return redirect(url_for("uploaded_file_mask", filename=filename, maskname=maskname, lang=lang))

            

@app.route("/tmp/<filename>?<lang>")
def uploaded_file(filename, lang):
    if filename.endswith(".txt"):
        wc_txt(filename, lang=lang)
    elif filename.endswith(".doc") or filename.endswith(".docx"):
        wc_doc(filename, lang=lang)
    else:
        wc_pdf(filename, lang=lang)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return render_template("output.html", filename=filename)


@app.route("/tmp/<filename>?<maskname>?<lang>")
def uploaded_file_mask(filename, maskname, lang):
    if filename.endswith(".txt"):
        wc_txt(filename, maskname, lang)
    elif filename.endswith(".doc") or filename.endswith(".docx"):
        wc_doc(filename, maskname, lang)
    else:
        wc_pdf(filename, maskname, lang)
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    os.remove(os.path.join(app.config['UPLOAD_FOLDER'], maskname))
    return render_template("output.html", filename=filename, maskname=maskname)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


if __name__ == '__main__':
   app.run(debug = True)