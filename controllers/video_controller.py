import math
import threading

import cv2
import cvzone
import pandas as pd
from ultralytics import YOLO

from utils.tracker import Tracker


def _distance_from_point_to_line(d_x1, d_y1, d_x2, d_y2, point):
    # Tentukan koefisien A, B, dan C untuk persamaan garis Ax + By + C = 0
    a_ = d_y2 - d_y1
    b_ = -(d_x2 - d_x1)
    c_ = (d_x2 - d_x1) * d_y1 - (d_y2 - d_y1) * d_x1

    # Hitung jarak dari titik (x3, y3) ke garis
    distance = abs(a_ * point[0] + b_ * point[1] + c_) / math.sqrt(a_ ** 2 + b_ ** 2)

    return distance


def _count_object_(bbox_idx, list_arr):
    for bbox in bbox_idx:
        x_1, y_1, x_2, y_2, cls_ = bbox
        cx = int(x_1 + x_2) // 2
        cy = int(y_1 + y_2) // 2
        d = int(_distance_from_point_to_line(0, 640, 640, 160, (cx, cy)))
        radius = int(math.sqrt((x_2 - x_1) ** 2 + (y_2 - y_1) ** 2)) // 2
        if d < radius:
            if list_arr.count(cls_) == 0:
                list_arr.append(cls_)


class VideoController:
    def __init__(self):
        self.cap = None
        self.is_running = False
        self.frame = None
        self.thread = None
        self.count = 0

        self.bikerider_model = YOLO('models/bikerider.pt')
        self.bikerider_class = ['other', 'bikerider']

        self.helmet_model = YOLO('models/helmet.pt')
        self.helmet_class = ['nohelmet', 'helmet']

        self.no_helmet_tracker = Tracker()
        self.helmet_tracker = Tracker()

        self.other = []
        self.bikerider = []

        self.no_helmet = []
        self.helmet = []

    def start(self, filename):
        if not self.is_running:
            self.cap = cv2.VideoCapture(filename)
            self.is_running = True
            self.thread = threading.Thread(target=self._capture_loop)
            self.thread.start()

    def stop(self):
        if self.is_running:
            self.is_running = False
            if self.thread is not None:
                self.thread.join()
            if self.cap is not None:
                self.cap.release()
            cv2.destroyAllWindows()

    def _capture_loop(self):
        while self.is_running:
            ret, frame = self.cap.read()
            if ret:
                self.count += 1
                if self.count % 3 != 0:
                    continue
                self.frame = frame
            else:
                self.stop()

    def get_frame(self):
        if self.frame is not None:
            frame = cv2.resize(self.frame, (640, 640))

            bikerider_results = self.bikerider_model.predict(frame)
            bikerider_boxes = bikerider_results[0].boxes.data
            bikerider_coors = pd.DataFrame(bikerider_boxes).astype("float")

            bikerider_list = []
            other_list = []
            no_helmet_list = []
            helmet_list = []

            for index, row in bikerider_coors.iterrows():
                b_x1 = int(row[0])
                b_y1 = int(row[1])
                b_x2 = int(row[2])
                b_y2 = int(row[3])

                cls = self.bikerider_class[int(row[5])]

                if 'bikerider' in cls:
                    bikerider_list.append([b_x1, b_y1, b_x2, b_y2])

                    crop_frame = frame[b_y1:b_y2, b_x1:b_x2]
                    helmet_results = self.helmet_model.predict(crop_frame)
                    helmet_boxes = helmet_results[0].boxes.data
                    helmet_coors = pd.DataFrame(helmet_boxes).astype("float")

                    for i, r in helmet_coors.iterrows():
                        x1 = int(b_x1 + r[0])
                        y1 = int(b_y1 + r[1])
                        x2 = int(b_x1 + r[2])
                        y2 = int(b_y1 + r[3])

                        cls = self.helmet_class[int(r[5])]

                        if 'nohelmet' in cls:
                            no_helmet_list.append([x1, y1, x2, y2])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 1)
                            cvzone.putTextRect(frame, f'No Helmet', (x1, y1), 1, 1)
                            cxnh = int(x1 + x2) // 2
                            cynh = int(y1 + y2) // 2
                            d = int(_distance_from_point_to_line(0, 640, 640, 160, (cxnh, cynh)))
                            radius = int(math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) // 2
                            if d < radius:
                                cv2.imwrite(f'./uploads/detection/violation_{self.count}.jpg', crop_frame)
                                cv2.circle(frame, (cxnh, cynh), radius, (0, 255, 255), thickness=-1,
                                           lineType=cv2.LINE_AA)

                        elif 'helmet' in cls:
                            helmet_list.append([x1, y1, x2, y2])
                            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
                            cvzone.putTextRect(frame, f'Helmet', (x1, y1), 1, 1)

            bbox_helmet_idx = self.helmet_tracker.update(helmet_list)
            _count_object_(bbox_helmet_idx, self.helmet)

            bbox_no_helmet_idx = self.no_helmet_tracker.update(no_helmet_list)
            _count_object_(bbox_no_helmet_idx, self.no_helmet)

            countHelmet = (len(self.helmet))
            cvzone.putTextRect(frame, f'Helmet:{countHelmet}', (50, 30), 1, 1)

            countNoHelmet = (len(self.no_helmet))
            cvzone.putTextRect(frame, f'No Helmet:{countNoHelmet}', (50, 60), 1, 1)

            ret, buffer = cv2.imencode('.jpg', frame)
            return buffer.tobytes()
        else:
            return None


video_controller = VideoController()
