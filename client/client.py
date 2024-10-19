from picamera2 import Picamera2
import time
import requests
import datetime

# Camera cfg
picam2 = Picamera2()
picam2.start()

# Parameters
SERVER_URL = 'http://${IP}:${PORT}/upload'
CAMERA_ID = 'R-Parking01'

# Function to send images to the server
def send_image(data):
    picam2.capture_file('image.jpg')
    with open('image.jpg', 'rb') as img:
        files = {'image': img}
        current_time = datetime.datetime.now().isoformat()  # Get actual hour to use as id
        data = {
        'camera_id': CAMERA_ID,
        'timestamp': current_time,
        'data': data
        }
        response = requests.post(SERVER_URL, files=files, data=data)
        print(response.text)

# While loop to send images every 60 seconds
while True:
    send_image("some data from " + CAMERA_ID)
    time.sleep(60)