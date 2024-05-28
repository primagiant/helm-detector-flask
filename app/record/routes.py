import os

import cv2
from flask import render_template, Response

from . import record


@record.route("/<filename>")
def index(filename):
    return render_template("views/record.html", filename=filename)


@record.route('/video_feed/<filename>')
def video_feed(filename):
    video_path = os.path.join('uploads', 'video', filename)
    return Response(generate_frames(video_path), mimetype='multipart/x-mixed-replace; boundary=frame')


def generate_frames(video_path):
    cap = cv2.VideoCapture(video_path)
    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
 
