import threading

import cv2
import cvzone
import pandas as pd
from ultralytics import YOLO

from utils.tracker import Tracker


def count_object_(bbox_idx, list_arr, cy1, offset):
    for bbox in bbox_idx:
        x1, y1, x2, y2, cls = bbox
        cx = int(x1 + x2) // 2
        cy = int(y1 + y2) // 2
        if (cy + offset) > cy1 > (cy - offset):  # TODO (Garis di perbaiki garis untuk countning)
            if list_arr.count(cls) == 0:
                list_arr.append(cls)


class Camera:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.frame = None
        self.thread = None

        self.bikerider_model = YOLO('models/bikerider.pt')
        self.bikerider_class = ['other', 'bikerider']

        self.helmet_model = YOLO('models/helmet.pt')
        self.helmet_class = ['nohelmet', 'helmet']

    def start(self):
        if not self.is_running:
            self.cap = cv2.VideoCapture(0)
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop)
            self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            self.thread.join()
            self.cap.release()
            cv2.destroyAllWindows()

    def _capture_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.frame = frame

    def get_frame(self):
        if self.frame is not None:
            _, jpeg = cv2.imencode('.jpg', self.frame)
            return jpeg.tobytes()
        else:
            return None

    def generate_frame_from_model(self):
        if self.frame is not None:
            cy1 = 427
            offset = 6

            no_helmet_tracker = Tracker()
            helmet_tracker = Tracker()

            no_helmet = []
            helmet = []

            frame = cv2.resize(self.frame, (640, 640))

            bikerider_results = self.bikerider_model.predict(frame)
            bikerider_boxes = bikerider_results[0].boxes.data

            helmet_results = self.helmet_model.predict(frame)
            helmet_boxes = helmet_results[0].boxes.data

            helmet_coors = pd.DataFrame(helmet_boxes).astype("float")

            no_helmet_list = []
            helmet_list = []

            # line visualisation
            cv2.line(frame, (0, cy1), (640, cy1), (0, 255, 255))

            for index, row in helmet_coors.iterrows():
                x1 = int(row[0])
                y1 = int(row[1])
                x2 = int(row[2])
                y2 = int(row[3])

                cls = self.helmet_class[int(row[5])]

                if 'nohelmet' in cls:
                    no_helmet_list.append([x1, y1, x2, y2])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cvzone.putTextRect(frame, f'No Helmet', (x1, y1), 1, 1)
                elif 'helmet' in cls:
                    helmet_list.append([x1, y1, x2, y2])

            bbox_no_helmet_idx = no_helmet_tracker.update(no_helmet_list)
            count_object_(bbox_no_helmet_idx, no_helmet, cy1, offset)

            bbox_helmet_idx = helmet_tracker.update(helmet_list)
            count_object_(bbox_helmet_idx, helmet, cy1, offset)

            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        else:
            return None


camera = Camera()
