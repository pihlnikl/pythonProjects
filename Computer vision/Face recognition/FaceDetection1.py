import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\haarcascade_frontalface_alt.xml')

eye_cascade = cv2.CascadeClassifier('C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\haarcascade_eye_tree_eyeglasses.xml')

video = ("C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\VID_2.mp4")

cap = cv2.VideoCapture(video) 
while 1:

    ret, img = cap.read()

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.5, 5)

    for (x,y,w,h) in faces:

        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)

        roi_gray = gray[y:y+h, x:x+w]

        roi_color = img[y:y+h, x:x+w]

        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex,ey,ew,eh) in eyes:

            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)

    print ("found " +str(len(faces)) +" face(s)")

    cv2.imshow('img',img)

    k = cv2.waitKey(30) & 0xff

    if k == 27:

        break

cap.release()

cv2.destroyAllWindows()