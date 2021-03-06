import cv2
import sys
import os
import time

cascPath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascPath)

video_capture = cv2.VideoCapture(0)


print "======= Training =========="
print "This will take a few images of you face to train on"
facename = raw_input('What is your name? ')



try:
    amount = int(input("Thank you " + facename + ", how many images would you like to take? (4) "))
except:
    amount = 4

imgindex = 0


cv2.namedWindow("Video", cv2.WINDOW_NORMAL);
cv2.setWindowProperty("Video", cv2.WND_PROP_FULLSCREEN, 1);

framecount = 0

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    #frame = cv2.resize(frame, (0,0), fx=.1, fy=.1)

    faces = []
    if(framecount == 15):    
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.resize(gray, (0,0), fx=.2, fy=.2)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5
        )
        framecount = 0
    else:
       framecount += 1
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        x = x * 5
        y = y * 5
        w = w * 5
        h = h * 5
        face = gray[y: y + h, x: x + h]
        #print "Face size in image: %d x %d"  % (w, h)
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, str("face"), (x+2, y+h-2), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
        break;
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) == 27:
        break  # esc to quit


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
print "Completed. %d images were taken" % imgindex
