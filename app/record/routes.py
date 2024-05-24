import os

from flask import render_template, request, flash, redirect, url_for

from . import record


@record.route("/")
def index():
    return render_template("views/record.html")


@record.route('/upload_video', methods=['POST'])
def upload_video():
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files['file']
    if file.filename == '':
        flash("No selected file")
        return redirect(request.url)

    if file:
        filename = file.filename
        file.save(os.path.join('uploads/video', filename))
        flash('File saved successfully!')
        return redirect(url_for('record.index'))
