import numpy as np
import cv2

def detectFaces(frame):
    #grayscale the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #forward pass greyscale image into face classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    #return an array of detected faces
    return faces

cap = cv2.VideoCapture(0)
#premade face detection cascade classifier
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    #greyscale the image
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #detect faces
    faces = detectFaces(frame)
    #draw bounding boxes around detected faces
    for(x,y,w,h) in faces:
        img = cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = frame[y:y+h, x:x+w]
        if len(faces) > 0:
            eyes = eye_cascade.detectMultiScale(roi_color, minSize = (int(w/20),int(h/20)), maxSize=(int(w/6),int(h/6)), minNeighbors=5)
            for(x2,y2,w2,h2) in eyes[0:((len(faces))*2)]:
                img2 = cv2.rectangle(roi_color, (x2,y2), (x2+w2, y2+h2), (0,255,0), 2)

    # Display the resulting frame
    cv2.imshow('frame', frame)
    #kill with q key
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything is done, release the capture
cap.release()
cv2.destroyAllWindows()
