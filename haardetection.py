# Importing OpenCV package
import cv2
from imutils import face_utils
import matplotlib.pyplot as plt

# step1: read the image
image = cv2.imread("./Test/img3.jpg")

# step2: converts to gray image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# step3:Loading the required haar-cascade xml classifier file
haar_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# Applying the face detection method on the grayscale image
faces_rect = haar_cascade.detectMultiScale(gray, 1.1, 9)

# step4:Iterating through rectangles of detected faces
for (x, y, w, h) in faces_rect:
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

# step5: display the resulted image
plt.imshow(image)
plt.show()