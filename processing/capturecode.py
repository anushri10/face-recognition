import cv2
import sys
flag=0

import requests
import base64
import threading


def uploadImage(data):
	# with open("yourfile.ext", "rb") as image_file:
 #    	imgstring = base64.b64encode(image_file.read())
	r = requests.post('http://localhost:5000/submit', data = {'image':data})
    
def threadMaker(data):
	 t = threading.Thread(target=uploadImage, args=(data,))
	 t.start()

faceCascade = cv2.CascadeClassifier("haarcascade_frontlface_default.xml")

video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
        #cv2.imwrite('test.png',frame)
        imgstring = base64.encodestring(cv2.imencode('.jpeg', frame)[1])
        print type(imgstring)
        print imgstring
        threadMaker(imgstring)

    # while (flag!=1):
        # frame2 = video_capture.read()
        # cv2.imwrite('test.png',frame2)
        # flag=0

    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()

