#!/usr/bin/python

# Import the required modules
import cv2, os
import numpy as np

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer 
recognizer = cv2.createLBPHFaceRecognizer()

def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        img = cv2.imread(image_path, 0)
        filename = os.path.basename(image_path)
        label = filename.rsplit(".", 2)[0]
        images.append(img)
        labels.append(label)
##        # Read the image and convert to grayscale
##        image_pil = Image.open(image_path).convert('L')
##        # Convert the image format into numpy array
##        image = np.array(image_pil, 'uint8')
##        # Get the label of the image
##        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
##        # Detect the face in the image
##        faces = faceCascade.detectMultiScale(image)
##        # If face is detected, append the face to images and the label to labels
##        for (x, y, w, h) in faces:
##            images.append(image[y: y + h, x: x + w])
##            labels.append(nbr)
##            cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
##            cv2.waitKey(50)
    # return the images list and labels list
    return images, labels

# Path to the Yale Dataset
path = './faces'
# Call the get_images_and_labels function and get the face images and the 
# corresponding labels
print "Loading images"
images, labels = get_images_and_labels(path)
cv2.destroyAllWindows()

# Perform the tranining
print "Training"
recognizer.train(images, np.array(labels))
print "Training Complete"

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5
    )
    # Draw a rectangle around the faces
    for (x, y, w, h) in faces:
        face = gray[y: y + h, x: x + h]
        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        cv2.putText(frame, str(conf) + "%", (x+2, y+h-2), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        
    cv2.imshow("Video", gray)    
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
        

### Append the images with the extension .sad into image_paths
##image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.sad')]
##for image_path in image_paths:
##    predict_image_pil = Image.open(image_path).convert('L')
##    predict_image = np.array(predict_image_pil, 'uint8')
##    faces = faceCascade.detectMultiScale(predict_image)
##    for (x, y, w, h) in faces:
##        nbr_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
##        nbr_actual = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
##        if nbr_actual == nbr_predicted:
##            print "{} is Correctly Recognized with confidence {}".format(nbr_actual, conf)
##        else:
##            print "{} is Incorrect Recognized as {}".format(nbr_actual, nbr_predicted)
##        cv2.imshow("Recognizing Face", predict_image[y: y + h, x: x + w])
##        cv2.waitKey(1000)
