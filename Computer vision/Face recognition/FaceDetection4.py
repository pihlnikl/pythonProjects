import numpy as np
import cv2

face_cascade = cv2.CascadeClassifier('C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\haarcascade_frontalface_alt.xml')
eye_cascade = cv2.CascadeClassifier('C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\haarcascade_eye_tree_eyeglasses.xml')

video = ("C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\VID_2.mp4")
cap = cv2.VideoCapture(video)
rec = cv2.face.LBPHFaceRecognizer_create() 
rec.read("C:\\Users\\nikla\\OneDrive - Arcada\\Datorseende\\trainingdata.yml")

font=cv2.FONT_HERSHEY_SIMPLEX
while 1:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.5, 5)
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        id,conf=rec.predict(gray[y:y+h,x:x+w])
        if id==1:
            id="Niklas"
        if id !=1:
            id="Not Niklas"
        cv2.putText(img,id,(10,500), font, 4,(0,0,0),2,cv2.LINE_AA)

        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        for (ex,ey,ew,eh) in eyes:

            cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    cv2.imshow('img',img)
    
    if cv2.waitKey(1) == ord('q'):
        break
cap.release()

cv2.destroyAllWindows()