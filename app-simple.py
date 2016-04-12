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
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, 1);

framecount = 0

colors = [(100,100,100), (0,255, 255), (0,255, 0), (0,0, 255)]

rectRadius = 100
rectDetectionAccuracy = 5

lastRect = None

approved = False

for filename in os.listdir("references"):
    img = cv2.imread(os.path.join("references", filename))
    ret, buf = cv2.imencode('.png', img)
    cv2.imshow("Video", img)
    cv2.waitKey(100)
    faceRecognizer.addFace(buf)
    cv2.waitKey(1000)

def stopBlinking():
    global approved
    GPIO.setup(outPin, GPIO.IN)
    approved = False
    faceRecognizer.clean()

def clean():
    faceRecognizer.clean()

def getFaceImage(opencv_img):
    gray = cv2.cvtColor(opencv_img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=3
    )
    faceRect = None
    for face in faces:
        if faceRect == None or face[0] > faceRect[0]:
            faceRect = face
    ret, buf = cv2.imencode( '.jpg',
                             opencv_img[faceRect[1] : faceRect[3], faceRect[0] : faceRect[2]]
                             )
    return buf

global moved
moved = False

global faceProcessed

while True:
    ret, frame = video_capture.read()

    faceImg = frame.copy()
               
    h,w,c = frame.shape;
    midx = w / 2.0;
    midy = h / 4.0;
    startx = int(midx - rectRadius/2)
    endx = int(midx + rectRadius/2)
    starty = int(midy - rectRadius/2)
    endy = int(midy + rectRadius/2)    

    rectData = frame[starty:endy, startx:endx]
    cv2.rectangle(frame, (startx, starty), (endx, endy), colors[faceRecognizer.stage], 2)

    if lastRect != None and faceRecognizer.stage == 0:
        diff = cv2.absdiff(lastRect, rectData)
        ret, diff = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
        
        countPixels = 0
        sumPixels = 0
        x = 0
        y = 0
        while x < rectRadius:
            y = 0
            while y < rectRadius:
                sumPixels += diff[y,x][0]
                countPixels += 1
                y = y + rectDetectionAccuracy
            x = x + rectDetectionAccuracy

        if sumPixels > 2000:
            moved = True
        elif moved:
            moved = False
            faceImage = getFaceImage(faceImg)
            faceRecognizer.recognizeFaceAsync(faceImage)
            threading.Timer(5, clean).start()

    if not approved and faceRecognizer.stage == msface.FaceRecognizer.STAGE_APPROVED:
        approved = True
        GPIO.setup(outPin, GPIO.OUT)
        threading.Timer(5, stopBlinking).start()
            

    lastRect = rectData
    
    # Display the resulting frame
    
    frame[10:10+processingFace.shape[0], 10:10+processingFace.shape[1]] = processingFace
    cv2.imshow('Video', frame)
    
    key = cv2.waitKey(1);
    if key == 27:
        break  # esc to quit
    elif key == ord('s'):
        filename = time.strftime("%Y%m%d-%H%M%S") + ".png";
        filepath = os.path.join("references", filename)
        cv2.imwrite(filepath, faceImg)
        ret, buf = cv2.imencode( '.png', faceImg )
        faceRecognizer.addFace(buf)

# When everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()
#print "Completed. %d images were taken" % imgindex
