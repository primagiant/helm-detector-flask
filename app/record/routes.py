import os

from flask import render_template, Response
from controllers.video_controller import video_controller

from . import record


@record.route("/<filename>")
def index(filename):
    return render_template("views/record.html", filename=filename)


@record.route('/video_feed/<filename>')
def video_feed(filename):
    video_path = os.path.join('uploads', 'video', filename)
    video_controller.start(video_path)
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames():
    while True:
        frame = video_controller.get_frame()
        if frame is None:
            video_controller.stop()  # Stop processing when no frames are available
            break
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
