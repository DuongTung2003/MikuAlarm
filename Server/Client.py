import sys
import socket             
import pygame
import RPi.GPIO as GPIO
from time import sleep
import time
import threading
import logging
import os
from Commandlist import Commands
from datetime import datetime
import schedule
import random
import pyowm

key = "41b26fc85ad1fd789f3064de7fa81cd6"
location = 'Lang Son,VN'
sys.setrecursionlimit(1500)
try:
    os.mkdir("LogFiles/")
except :
    pass
format = "%(asctime)s: %(message)s"
logname =  "./LogFiles/Log_"+str(datetime.now().month) +"_"+ str(datetime.now().day)+"_"+ str(datetime.now().hour)+"_"+ str(datetime.now().minute)+".log"
logging.basicConfig(filename=logname,format=format, level=logging.DEBUG,datefmt="%H:%M:%S")

def writeloginf(log):
    logging.info(log)
    print(log)
def writelogwar(log):
    logging.warning(log)
    print(log)
def writelogerr(log):
    logging.error(log)
    print(log)
writeloginf("Client started")                        
start_time = time.time()
try:
    pwm=GPIO.PWM(5, 50)
except :
    writelogerr("pwm failed")

s = socket.socket() #socket module (socket_family,socket_type,protocol=0)       tcp 
host = '192.168.0.105' #IP server
host = input("IP: ")
port = 6987              
data = b""
decoded = ""
sendserver = "0"
#socket.setdefaulttimeout(5)
#writeloginf("Timeout: ",s.gettimeout())
GPIO.setmode(GPIO.BOARD)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(26, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(22, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.output(12, False)
retrying = False
connected = False

def startfacedt(runnedcv):
   
     writeloginf(runnedcv)
     import PythonCV
    
#   ----------------------------------
def playalarm():
   
    willrain = False
    try:
     owm = pyowm.OWM(key)
     location = owm.three_hours_forecast(location)
     wstatus = "Rain: "+ location.will_have_rain()
     willrain = location.will_have_rain()
     writeloginf(wstatus)
    except:
        writelogerr("Weather fetch fail")
    
    quotelist = ["./morning/wakeup.mp3"]
    rand = random.choice(quotelist)
    writeloginf(rand)
    musicdic = os.listdir("./music/")
    randomsong = random.choice(musicdic)
    if willrain == True:
        rand = "./morning/goodmoringrain.mp3"

    
    writeloginf("ohayo :D")
    try:
     pygame.mixer.init()
    except:
         writelogerr("Cannot init")
    
    pygame.mixer.music.load(rand)
    pygame.mixer.music.play()
   
    GPIO.output(18,True)
    sendserver = "1"

    while pygame.mixer.music.get_busy() == True:
        GPIO.output(12, True)
        sleep(0.1)
        GPIO.output(12, False)
        continue
    randomsong = "./music/" + randomsong
    pygame.mixer.music.load(randomsong)
    pygame.mixer.music.play()
    GPIO.output(18,True)
    sendserver = "1"
    reportlog = "Current song: "+ randomsong
    writeloginf(reportlog)
    while pygame.mixer.music.get_busy() == True:
        
        sleep(0.5)
        if GPIO.input(22) == GPIO.HIGH:
             pygame.mixer.music.stop()
             sleep(2)
             pygame.mixer.music.load("./morning/afteroff.mp3")
             pygame.mixer.music.play()
             GPIO.output(12, True)
             while pygame.mixer.music.get_busy() == True:
                 continue
             sleep(1)
             writeloginf("Good morning!")
             break

        GPIO.output(12, True)
        sleep(0.1)
        GPIO.output(12, False)
        


    GPIO.output(18, False)
  
    try:
        s.send(sendserver.encode())
    except:
        writelogerr("Cannot sent to server")
def wakeup():

    pass






#   ----------------------------------

def communicate():
    
    while True:
      rantime = time.time() - start_time
      rantime = int(rantime)
      timeranstr = "Client ran for: " + str(rantime)
      writeloginf(timeranstr)
      sendserver = "0"
      data = s.recv(1024)
      decoded = data.decode() # chuyển byte sang str
      writeloginf(decoded) #for debug
      GPIO.output(18,True)
      sleep(0.5)
      GPIO.output(18,False)
      if decoded == Commands.testalarm:
          sendserver = "1"
          try:
              s.send(sendserver.encode())
          except:
              writwritelogerr("Cannot sent to server")
          playalarm()
      if decoded == Commands.setalarm:
          pygame.mixer.init()
          schedule.every().day.at('14:00').do(playalarm)

          sendserver = "1"
          try:
              s.send(sendserver.encode())
          except:
              writwritelogerr("Cannot sent to server")
          while True:
             schedule.run_pending()
             sleep(30) 
             if GPIO.input(22) == GPIO.HIGH:
                  writeloginf("pressed")
                  musicdic = os.listdir("./music/")
                  randomsong = random.choice(musicdic)
                  randomsong = "./music/" + randomsong
                  pygame.mixer.music.load(randomsong)
                  pygame.mixer.music.play()
             if  pygame.mixer.music.get_busy() == False:
              if GPIO.input(26) == GPIO.HIGH:
                  writeloginf("pressed")
                  musicdic = os.listdir("./music/")
                  randomsong = random.choice(musicdic)
                  randomsong = "./music/" + randomsong
                  pygame.mixer.music.load(randomsong)
                  pygame.mixer.music.play()
             else:
                 if GPIO.input(26) == GPIO.HIGH:
                  pygame.mixer.music.stop()
                 #else:
                 # try:
                 #     randomsong = random.choice(musicdic)
                 #     randomsong = "./music/" + randomsong
                 #     pygame.mixer.music.load(randomsong)
                 #     pygame.mixer.music.play()
                 # except:
                 #   wrwritelogerr("Error ocurred")
      if decoded == Commands.testspeech:
            writeloginf("ohayo :)")
            try:
               pygame.mixer.init()
               pygame.mixer.music.load("goodmorning.mp3")
               pygame.mixer.music.play()
            except:
                wrwritelogerr("Error ocurred")
            GPIO.output(18,True)
            sendserver = "1"
            while pygame.mixer.music.get_busy() == True:
             GPIO.output(12, False)
             sleep(0.05)
             GPIO.output(12, True)
             continue
             try:
              s.send(sendserver.encode())
             except:
              writwritelogerr("Cannot sent to server")
      if decoded == Commands.detectface:
          sendserver = "1"
          try:
              s.send(sendserver.encode())
          except:
              writwritelogerr("Cannot sent to server")
          x = threading.Thread(target=startfacedt, args=(False,))
          x.start()
          logging.critical("STARTED")
         
          while True:
           data = s.recv(1024)
           state = data.decode() # chuyển byte sang str
           logging.critical("recv ",state)
           print(state)
           print(state.format())
           sendserver = "1"
          
           if state == 'stop facedetect':
               threading._shutdown()
               GPIO.output(12, False)
               sendserver = "1"
               break
               try:
                s.send(sendserver.encode())
               except:
                writwritelogerr("Cannot sent to server")
      if decoded == Commands.readlog:
          files = os.listdir("./LogFiles/")
          files.sort()
          writeloginf(("Found ",str(len(files))," file(s):"))
          for file in files:
              print(files.index(file)," : ",file)
             # with open(file, 'r') as f:
              #     data = f.read()
          print("Read file:")
          getfilenum = input(">")
         
          try:
              getfilenum = int(getfilenum)
              test = files[getfilenum]
          except :
              writelogerr("File index not found")
          else:
              getfilenum = int(getfilenum)
              path = "./LogFiles/" + files[getfilenum]
              f = open(str(path), 'r')
              data = f.read()
              print(data)
          sendserver = "1"
         #  with open()
      if decoded == Commands.stopmusic:
          pygame.mixer.music.stop()
          sendserver = "1"
      if decoded == Commands.playussr:
        pygame.mixer.init()
        pygame.mixer.music.load("USSR.mp3")
        pygame.mixer.music.play()
        GPIO.output(18,True)
        sendserver = "1"
        #while pygame.mixer.music.get_busy() == True:
          #  continue
      if decoded == Commands.Quit:
         sendserver = "9"
         try:
              s.send(sendserver.encode())
         except:
              writwritelogerr("Cannot sent to server")
         break
     
         try:
              s.send(sendserver.encode())
         except:
              writwritelogerr("Cannot sent to server")
      
def connect(hostip):
    retrying = False
    host = '192.168.0.104'
    writeloginf(("Connecting to server: ",hostip,":",port))
    try: 
      
      s.connect((hostip, port))
    except :
      writelogerr("Unexpected Error")
      writeloginf("Backup command ready")
      connected = False
      while True:
                
                command = input(">")
                if command == Commands.retry:
                    host = input("IP: ")
                    writeloginf("Reconnecting..")
                    retrying = True
                    writeloginf(retrying)
                   
                    break
                if command == Commands.offlinemode:
                    writeloginf("OFFLINE mode activated")
                    import ClientOFFLINE
                elif command == Commands.Quit:
                    writeloginf("Quiting..")
                    break
                else:  
                    writelogerr("Unknown command")
    else:
     writeloginf(("Connected to server: ",hostip,":",port))
     connected = True
    return retrying,connected,host

while True:
    if host == "":
        host = "192.168.0.104"
    arr = connect(host)
    retrying = arr[0]
    connected = arr[1]
    host = arr[2]

    print(retrying,"   ",connected)
    if retrying == True:
        retrying = False
       
    else:
        if connected == True:
            communicate()
        else:
            break

 
