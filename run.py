from . import create_app
import os

app = create_app()
app.config["VIDEO_UPLOAD"] = 'uploads/video'
app.config["DETECTION_RESULT"] = 'uploads/detection'
app.config["SECRET_KEY"] = "supersecretkey"
app.config["DEBUG"] = True

if not os.path.exists(app.config["VIDEO_UPLOAD"]):
    os.makedirs(app.config["VIDEO_UPLOAD"])

if not os.path.exists(app.config["DETECTION_RESULT"]):
    os.makedirs(app.config["DETECTION_RESULT"])

if __name__ == '__main__':
    app.run(debug=True)
