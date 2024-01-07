import cv2
import sys
import numpy
from helpers import track
from ultralytics import YOLO
import serial
import json
import requests

# model_seg = YOLO('./models/best_seg.pt')
model_ocr = YOLO('./models/best_ocr.pt')
#create val
API_ENDPOINT = "http://localhost:3001/vehicle_in_out_post"

ser = serial.Serial('COM3', 115200)
alive = True
s = 0
if len(sys.argv) > 1:
    s = sys.argv[1]

win_name = "Parking Camera"

cv2.namedWindow(win_name, cv2.WINDOW_NORMAL)

source = cv2.VideoCapture(s)

while alive:
    has_frame, frame = source.read()
    if not has_frame:
        break
    result = frame
    cv2.imshow(win_name, result)
    frame = cv2.flip(frame, 1)

    key = cv2.waitKey(1)
    if key == ord("Q") or key == ord("q") or key == 27:
        alive = False
    elif key == ord("C") or key == ord("c"):
        plate = track(frame, model_ocr)
        if plate == "No plate detect":
            print(plate)
        elif len(plate) == 8:
            ser.write(plate.encode())
            plate_json = {'license_plate': plate}
            print(plate_json)
            r = requests.post(url=API_ENDPOINT, json=plate_json)

source.release()
cv2.destroyWindow(win_name)
