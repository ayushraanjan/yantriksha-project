import cv2
import numpy as np
from twilio.rest import Client


TWILIO_ACCOUNT_SID = 'AC56b4f427fa04f084c2b8d94ff48f0be2'
TWILIO_AUTH_TOKEN = '[Replace with your Twilio Auth Token]'
TWILIO_PHONE_NUMBER = '+12072887804'
EMERGENCY_PHONE_NUMBER = '+919064295486'

alert_sent = False

def send_emergency_alert():
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    message = client.messages.create(
        body="Emergency alert! A gesture was detected.",
        from_=TWILIO_PHONE_NUMBER,
        to=EMERGENCY_PHONE_NUMBER
    )
    print("Alert sent with SID:", message.sid)

def detect_gesture(frame):
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

def main():
    global alert_sent
    camera = cv2.VideoCapture(0)

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        if detect_gesture(frame) and not alert_sent:
            send_emergency_alert()
            alert_sent = True

        cv2.imshow('Camera Preview', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
