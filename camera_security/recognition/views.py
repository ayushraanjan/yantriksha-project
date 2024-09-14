import cv2
import numpy as np
from django.http import StreamingHttpResponse
from twilio.rest import Client

# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC56b4f427fa04f084c2b8d94ff48f0be2'
TWILIO_AUTH_TOKEN = '5cb7c369000fa8b2164480715a528358'
TWILIO_PHONE_NUMBER = '+12072887804'
EMERGENCY_PHONE_NUMBER = '+919064295486'

def send_emergency_alert():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body="Emergency alert! Captive situation detected",
        from_=TWILIO_PHONE_NUMBER,
        to=EMERGENCY_PHONE_NUMBER
    )
    print("Alert sent with SID:", message.sid)

def detect_gesture(frame):
    """
    Detect a simple gesture (thumbs up) in the video frame.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        epsilon = 0.02 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        
        if len(approx) > 10:
            return True

    return False

def gen(camera):
    while True:
        ret, frame = camera.read()
        if not ret:
            break

        if detect_gesture(frame):
            # Trigger emergency action
            send_emergency_alert()

        _, jpeg = cv2.imencode('.jpg', frame)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    camera = cv2.VideoCapture(0)
    return StreamingHttpResponse(gen(camera),
                                 content_type='multipart/x-mixed-replace; boundary=frame')
