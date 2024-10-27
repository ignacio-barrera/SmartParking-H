from picamera2 import Picamera2
import time
import requests
import datetime
import cv2
from ultralytics import YOLO

picam2 = Picamera2()
picam2.start()

SERVER_URL = 'http://192.168.100.177:5000/upload'
CAMERA_ID = 'R-Parking01'

model = YOLO('yolov8n.pt')

def send_image(data):
    picam2.capture_file('image.jpg')
    img = cv2.imread('image.jpg')
    results = model(img)
    for result in results:
        for box in result.boxes:
            if int(box.cls[0]) == 0:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(img, "Person", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    cv2.imwrite('image_detected.jpg', img)
    with open('image_detected.jpg', 'rb') as img_file:
        files = {'image': img_file}
        current_time = datetime.datetime.now().isoformat()
        data = {
            'camera_id': CAMERA_ID,
            'timestamp': current_time,
            'data': data
        }
        response = requests.post(SERVER_URL, files=files, data=data)
        print(response.text)

while True:
    send_image("some data from " + CAMERA_ID)
    time.sleep(5)
