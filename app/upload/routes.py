import os

from flask import render_template, request, flash, redirect, url_for

from . import upload


@upload.route("/")
def index():
    files = os.listdir('uploads/video')
    return render_template("views/upload.html", files=files)


@upload.route('/upload_video', methods=['POST'])
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
        return redirect(url_for('upload.index'))


@upload.route('/delete/<filename>', methods=['POST'])
def delete(filename):
    video_path = os.path.join('uploads/video', filename)
    os.remove(video_path)
    flash("File deleted successfully!")
    return redirect(url_for('upload.index'))
