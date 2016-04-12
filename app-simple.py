import cv2
import sys
import os
import msface
import RPi.GPIO as GPIO
import threading
import time

GPIO.setmode(GPIO.BCM)
outPin = 17
GPIO.setup(outPin, GPIO.IN)

faceRecognizer = msface.FaceRecognizer()

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

cv2.namedWindow("Video", cv2.WINDOW_NORMAL);
#cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, 1);

framecount = 0

faces = []
scaleFactor = 2.0

rectColor = (0,255,255)

rectRadius = 10

lastRect = None

approved = False

processing = False

def stopBlinking():
    global approved
    print "BLINK COMPLETE. SETTING GPIO 17 TO FALSE"
    GPIO.setup(outPin, GPIO.IN)
    approved = False
    faceRecognizer.clean()

while True:
    ret, frame = video_capture.read()

    h,w,c = frame.shape;
    midx = w / 2.0;
    midy = h / 2.0;
    startx = int(midx - rectRadius/2)
    endx = int(midx + rectRadius/2)
    starty = int(midy - rectRadius/2)
    endy = int(midy + rectRadius/2)

    rectData = frame[starty:endy, startx:endx]
    cv2.rectangle(frame, (startx, starty), (endx, endy), rectColor, 2)

    if lastRect != None:
        print cv2.absdiff(lastRect, rectData).size

    lastRect = rectData
    # Display the resulting frame
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1);
    if key == 27:
        break  # esc to quit
    elif key == ord('s'):
        filename = time.strftime("%Y%m%d-%H%M%S") + ".png";
        filepath = os.path.join("references", filename)
        cv2.imwrite(filepath, face)
        ret, buf = cv2.imencode( '.png', frame )
        faceRecognizer.addFace(buf)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
#print "Completed. %d images were taken" % imgindex
