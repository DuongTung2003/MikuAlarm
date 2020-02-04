import cv2
import sys
from time import sleep
import logging
import os
format = "%(asctime)s: %(message)s"
logging.basicConfig(format=format, level=logging.INFO,datefmt="%H:%M:%S")




  #duty = angle / 18 + 2
  #ismoving = True
  #GPIO.output(5, True)
  #pwm.ChangeDutyCycle(duty)
  #GPIO.output(12, False)
  #sleep(0.3)
  #GPIO.output(12, True)
  #sleep(1)
  #GPIO.output(12, False)
  #ismoving = False
  #GPIO.output(5, False)
  #pwm.ChangeDutyCycle(0)
  #logging.info("Angle: ",angle)
  #sleep(0.2)
  #GPIO.output(12, True)


#control_pins = [7,11,13,15]
#for pin in control_pins:
#  GPIO.setup(pin, GPIO.OUT)
#  GPIO.output(pin, 0)

#  halfstep_seq = [
#  [1,0,0,0],
#  [1,1,0,0],
#  [0,1,0,0],
#  [0,1,1,0],
#  [0,0,1,0],
#  [0,0,1,1],
#  [0,0,0,1],
#  [1,0,0,1]
#]
#  backhalfstep_seq = [
#    [1,0,0,1],
#    [0,0,0,1], 
#    [0,0,1,1],
#    [0,0,1,0], 
#    [0,1,1,0],
#    [0,1,0,0], 
#    [1,1,0,0], 
#    [1,0,0,0],
#]

#def gof():
#    for halfstep in range(8):
#     for pin in range(4):
#      GPIO.output(control_pins[pin], halfstep_seq[halfstep][pin])
#     time.sleep(0.001)


#def gob():
#    for backhalfstep in range(8):
#     for pin in range(4):
#      GPIO.output(control_pins[pin], backhalfstep_seq[backhalfstep][pin])
#     time.sleep(0.001)
def cap():
    trycap = True
    count += 1

trycap = False
cascPath = "haarcascade_frontalface_default.xml"   #Hand
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
      
       
        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.rectangle(frame,(minx,miny),(maxx,maxy),(0, 255, 0),1)
            cv2.line(frame,(int(w/2) + x,0),(int(w/2) + x,y),(0, 255, 0),2 )
            cv2.line(frame,(int(w/2) + x,height),(int(w/2) + x,y+ h),(0, 255, 0),2 )
            cv2.line(frame,(0,int(h/2) + y),(x,int(h/2) + y),(0, 255, 0),2 )
            cv2.line(frame,(width,int(h/2) + y),(x+ w,int(h/2) + y),(0, 255, 0),2 )
            cv2.putText(frame,str("X:"+ str(w/2 + x) +" Y: "+ str(h/2 + y)),(int(width * 4/7),int(height * 1/6)),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            cv2.line(frame,(0,int(height/2)),(0,int(w/2)),(0, 255, 0),9 )
            logging.info(str(int(w/2) + x) + ' , ' + str(int(h/2) + y))
        
            facelocationx = int(w/2) + x
            facelocationy = int(h/2) + y
            X = int((x / width)*100)
            Y = int((y / height)*100)
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
            #if facelocationx > maxx:
            #    logging.info("X too high")
            #   # gof()
            #    if  currentang < 180 & ismoving == False:
            #      logging.info("Setting angle")
            #      currentang = currentang + 4
            #      SetAngle(180)
    
    
            #if facelocationx < minx:
            #     logging.info("X too low")
            #     if  currentang >= 4 & ismoving == False:
            #         logging.info("Setting angle")
            #         currentang = currentang - 4
            #         SetAngle(0)
                 
            #    # gob()
            #if facelocationy > maxy:
            #    logging.info("Y too low")
            #if facelocationy < miny:
            #     logging.info("Y too high")
            #if (facelocationy > miny) & (facelocationy < maxy )& (facelocationx > minx) & (facelocationx < maxx) :
            #     logging.info("In range")
        # Display the resulting frame
        cv2.imshow('Video', frame)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
trycap = False

    # When everything is done, release the capture

video_capture.release()
cv2.destroyAllWindows()
pwm.stop()
GPIO.cleanup()