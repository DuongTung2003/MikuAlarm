
            
import pygame
import RPi.GPIO as GPIO
from time import sleep
import time
import threading
import logging
import os
from datetime import datetime
from Commandlist import Commands
try:
    os.mkdir("LogFiles/")
except :
    pass
format = "%(asctime)s: %(message)s"
logname =  "./LogFiles/OFFLINELog_"+str(datetime.now().month) +"_"+ str(datetime.now().day)+"_"+ str(datetime.now().hour)+"_"+ str(datetime.now().minute)+".log"
logging.basicConfig(filename=logname,format=format, level=logging.DEBUG,datefmt="%H:%M:%S")
start_time = time.time()

decoded = ""

GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.output(12, False)
def startfacedt(runnedcv):
   
     logging.info(runnedcv)
     import PythonCV
    
   

def communicate():
    
    while True:
      logging.info("Client ran for: " , str(time.time() - start_time))
     
    
      decoded = input(">") # chuyển byte sang str
      logging.info(decoded) #for debug
      GPIO.output(18,True)
      sleep(0.5)
      GPIO.output(18,False)
      if decoded == Commands.detectface:
       

          x = threading.Thread(target=startfacedt, args=(False,))
          x.start()
          logging.critical("STARTED")
         
          while True:
          
           state = input(">") # chuyển byte sang str
           logging.critical("recv ",state)
           print(state)
           print(state.format())
       
          
           if state == Commands.stopdetect:
               threading._shutdown()
               GPIO.output(12, False)
               pwm.stop()
               GPIO.cleanup()
               break
          
          
      if decoded == "stop music":
          pygame.mixer.music.stop()
         
      if decoded == Commands.playussr:
        pygame.mixer.init()
        pygame.mixer.music.load("USSR.mp3")
        pygame.mixer.music.play()
        GPIO.output(18,True)
     
        #while pygame.mixer.music.get_busy() == True:
          #  continue
      if decoded == Commands.Quit:
    
         break
     
      
      

communicate()

   
 
