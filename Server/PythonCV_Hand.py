import cv2
import sys
import RPi.GPIO as GPIO
from time import sleep
import logging
import os
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")
count = 0
trycap = False

ismoving = False


def cap():
    trycap = True
    count += 1

trycap = False
cascPath = "Hand.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
    
video_capture = cv2.VideoCapture(0)
ret, frame = video_capture.read()
logging.info(frame.shape[0])
width = frame.shape[1]
height = frame.shape[0]
logging.info(frame.shape[1])
minx = int(width/3 + width/10)
maxx = int((width*2 )/3 - width/10)
miny = int(height /3 + height /10)
maxy = int((height*2 )/3 - height /10 )
    

while True:

        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if trycap == True:
            path = "./Capture"
            cv2.imwrite(os.path.join(path , "frame_%S_%M_%H_%D.jpg"), frame)
            
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )
      
        GPIO.output(12, False)
        for (x, y, w, h) in faces:
            logging.info(str(int(w/2) + x) + ' , ' + str(int(h/2) + y))
            GPIO.output(12, True)
            facelocationx = int(w/2) + x
            facelocationy = int(h/2) + y
            X = int((x / width)*100)
            Y = int((x / height)*100)
            print("X: "+ str(X))
            print("Y: "+ str(Y))
            sleep(0.2)
            try :
             datafile = open("Handpos.data","w+")
    
            except:
             print("cannot open file")
            datafile.write(str(X)+ " "+str(Y))
            datafile.flush()
            datafile.close()

    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
trycap = False

    # When everything is done, release the capture

video_capture.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()