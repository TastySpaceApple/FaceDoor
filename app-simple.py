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

colors = [(100,100,100), (0,255, 255), (0,255, 0), (0,0, 255)]

rectRadius = 100
rectDetectionAccuracy = 5

lastRect = None

approved = False

processing = False

for filename in os.listdir("references"):
    img = cv2.imread(os.path.join("references", filename))
    cv2.imshow("Video", img)
    faceRecognizer.addFace(img)
    cv2.waitKey(1)

def stopBlinking():
    global approved
    print "BLINK COMPLETE. SETTING GPIO 17 TO FALSE"
    GPIO.setup(outPin, GPIO.IN)
    approved = False
    faceRecognizer.clean()

def clean():
    faceRecognizer.clean()
    processing = False

while True:
    ret, frame = video_capture.read()

    faceImg = frame.copy()
               
    h,w,c = frame.shape;
    midx = w / 2.0;
    midy = h / 2.0;
    startx = int(midx - rectRadius/2)
    endx = int(midx + rectRadius/2)
    starty = int(midy - rectRadius/2)
    endy = int(midy + rectRadius/2)

    rectData = frame[starty:endy, startx:endx]
    cv2.rectangle(frame, (0, 0), (10, 10), colors[faceRecognizer.stage], 2)

    if lastRect != None and faceRecognizer.stage == 0:
        diff = cv2.absdiff(lastRect, rectData)
        ret, diff = cv2.threshold(diff, 100, 255, cv2.THRESH_BINARY)
        
        #cv2.imshow("Video", diff)
        countPixels = 0
        sumPixels = 0
        x = 0
        y = 0
        while x < rectRadius:
            y = 0
            while y < rectRadius:
                #print(lastRect[x,y] - rectData[x,y])
                sumPixels += diff[y,x][0]#abs(lastRect[y,x] - rectData[y,x])
                countPixels += 1
                y = y + rectDetectionAccuracy
            x = x + rectDetectionAccuracy

        print(sumPixels)
        if sumPixels > 2000:
            print("HIT")
	    ret, buf = cv2.imencode( '.jpg', frame )
            faceRecognizer.recognizeFaceAsync(buf)
            processing = True
            threading.Timer(5, clean).start()

    if not approved and faceRecognizer.stage == msface.FaceRecognizer.STAGE_APPROVED:
        global approved
        print "APPROVING. SET GPIO to TRUE"
        approved = True
        GPIO.setup(outPin, GPIO.OUT)
        threading.Timer(10, stopBlinking).start()
    "print(faceRecognizer.stage)"
            

    lastRect = rectData
    
    # Display the resulting frame
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
