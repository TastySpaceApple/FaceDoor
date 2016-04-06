import cv2
import sys
import os
import msface
import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BCM)
outPin = 17
GPIO.setup(outPin, GPIO.IN)

faceRecognizer = msface.FaceRecognizer()

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)

cv2.namedWindow("Video", cv2.WINDOW_NORMAL);
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, 1);

framecount = 0

faces = []
scaleFactor = 4.0

hasFaces = False
colors = [(0,255,255), (0,255,0), (0,0,255)]

def stopBlinking():
    GPIO.setup(outPin, GPIO.IN)

while True:
    ret, frame = video_capture.read()

    if framecount == 10: 
        #print "scanning for faces"
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (0,0), fx=1.0/scaleFactor, fy=1.0/scaleFactor)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5
        )
        #print "faces found : %d " % len(faces)
        if len(faces) > 0 and not hasFaces: # New face detected
            ret, buf = cv2.imencode( '.jpg', frame )
            rectColor = (0,255,255)
            faceRecognizer.recognizeFaceAsync(buf)
	elif len(faces) == 0:
            faceRecognizer.clean()
            
        hasFaces = len(faces) > 0
        framecount = 0
    else:
       framecount = framecount + 1
       
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        rectColor = colors[faceRecognizer.stage]
        if faceRecognizer.stage == FaceRecognizer.STAGE_APPROVED:
            GPIO.setup(outPin, GPIO.OUT)
        else
            GPIO.setup(outPin, GPIO.IN)
        x = int(x * scaleFactor)
        y = int(y * scaleFactor)
        w = int(w * scaleFactor)
        h = int(h * scaleFactor)
        face = gray[y: y + h, x: x + h]
        cv2.rectangle(frame, (x, y), (x+w, y+h), rectColor, 2)
        cv2.putText(frame, str("face"), (x+2, y+h-2), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
        break;
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    key = cv2.waitKey(1);
    if key == 27:
        break  # esc to quit
    elif key == ord('s'):
        ret, buf = cv2.imencode( '.jpg', frame )
        faceRecognizer.addFace(buf)


##    if face is not None:
##        imgindex += 1
##        filename = "%s.%d.png" % (facename, imgindex)
##        filepath = os.path.join("references", filename)
##        cv2.imwrite(filepath, face)
##        print ("Image %d Taken" % imgindex);
##    else:
##        print "No face was detected. Please try again"

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
#print "Completed. %d images were taken" % imgindex
