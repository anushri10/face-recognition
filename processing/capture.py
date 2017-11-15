import cv2
import sys, os

faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
video_capture = cv2.VideoCapture(0)
skip_frames = 20
x=0
# personx=str(sys.argv)


def get_image():
	ret, im = video_capture.read()
	return im


for i in range(0,100):
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	print("taking images", i)
	frame = get_image()
	cv2.imshow('video', frame)
	# if not os.path.exists(personx):
		# os.mkdir(personx,0755)
	file= "/Users/Anushri-MacBook/Desktop/dataset/person1/"+str(i)+".jpg"
	cv2.imwrite(file, frame)
	x=0	
	for x in range(0,skip_frames):
		temp = get_image()
		
				   
	
				
		    

	 
	

video_capture.release()
cv2.destroyAllWindows()


	  

	# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# faces = faceCascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minsize=(30, 30), flags=cv2.cv.CV_HAAR_SCALE_IMAGE)
	# for (x, y, w, h) in faces:
		# cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
   		
