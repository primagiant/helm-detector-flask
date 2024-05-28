from flask import render_template, Response

from controllers.camera import camera
from . import stream


@stream.route("/")
def index():
    return render_template("views/stream.html")


@stream.route('/start_camera')
def start_camera():
    camera.start()
    return "Camera started"


@stream.route('/stop_camera')
def stop_camera():
    camera.stop()
    return "Camera stopped"


@stream.route('/stream')
def streaming():
    return Response(generate_frame(), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frame():
    while True:
        frame = camera.generate_frame_from_model()
        if frame:
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
