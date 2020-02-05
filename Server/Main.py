
#voice from
#https://www.youtube.com/watch?v=ZBfAwU8NXB0




#Button: 7 inside 25 outside
#LED: 18 red 14 yellow  4 blinking led 24 green

#Note: assignment  a= x if x else y


#----------------------------------------------------IMPORT AND SETUP----------------------------------------------------------------------------------------------------
import sys
import cv2           
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
import serial
import socket
import netifaces as ni
import codecs
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


try :
    backupfile = open("./data/backup.data","r+")
    commnew = backupfile.read()
    
except:
    writelogerr("Cannot open file")
comm = ''
                      

try:
    pwm=GPIO.PWM(5, 50)
except :
    writelogerr("pwm failed")
writeloginf("File:" + commnew + "/end")
writeloginf("TungStudio v0.7")

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(7, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(25, GPIO.IN,pull_up_down=GPIO.PUD_DOWN)
GPIO.output(18, False)
GPIO.output(14, False)
GPIO.output(4, False)
GPIO.output(24, False)
sleep(1)
start_time = time.time()
ardconnected = False

def startup():
    quotelist = ["./conversation/hi.mp3","./conversation/hellonicetomeetyoutoday.mp3","./conversation/hello.mp3"]
    rand = random.choice(quotelist)
    writeloginf(rand)
    writeloginf("Startup..")
    try:
        pygame.mixer.init()
    except:
            writelogerr("Cannot init")
    pygame.mixer.music.set_volume(0.9)
    pygame.mixer.music.load(rand)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue
    pygame.mixer.music.set_volume(0.5)

startup()

try:
    arddata = serial.Serial('/dev/ttyACM0',9600)
    ardconnected = True
except:
    writelogerr("Cannot connect to arduino")
else:
    ardconnected = True
def sendard(variable):

    
    coded = variable.encode()
    try:
        arddata.write(coded)
    except:
        pass
    writeloginf("Sent: " + str(coded.decode()))
    arddata.timeout = 1
    rec = None
    sleep(1)
    data = arddata.read_until('\n')
    return str(data)
    #while rec == None or rec == b'' :
    #    sleep(2)
    #    if rec == None or rec == b'':
    #        arddata.write(coded)
    #        rec.decode()
   
        #writeloginf(rec)

    
#   ------------------------------------------------------  FUNCTION BLOCK  ----------------------------------------------------------------------------------
def playalarm():
        writelogerr("Cannot write to data.dat")
        key = "41b26fc85ad1fd789f3064de7fa81cd6"
        location = 'Lang Son,VN'
        willrain = False
        try:
            owm = pyowm.OWM(key)
            location = owm.three_hours_forecast(location)
            wstatus = "Rain: "+ str(location.will_have_rain())
            willrain = location.will_have_rain()
            writeloginf(wstatus)
        except:
         writelogerr("Can't fetch weather data")
    
        quotelist = ["./conversation/wakeup.mp3"]
        if willrain == True:
            quotelist = ["./conversation/goodmorningrain.mp3","./conversation/wakeup.mp3"]
        rand = random.choice(quotelist)
        writeloginf(rand)
        musicdic = os.listdir("./music/")
        
        

    
        writeloginf("ohayo :D")
        try:
         pygame.mixer.init()
        except:
             writelogerr("Cannot init")
    
        pygame.mixer.music.load(rand)
        pygame.mixer.music.play()
   
        GPIO.output(24,True)


        while pygame.mixer.music.get_busy() == True:
            GPIO.output(18, True)
            sleep(0.1)
            GPIO.output(18, False)
            continue
        while GPIO.input(25) == GPIO.LOW:
                    randomsong = random.choice(musicdic)
                    randomsong = "./music/" + randomsong
                    pygame.mixer.music.load(randomsong)
                    pygame.mixer.music.play()
                    pygame.mixer.music.set_volume(0.9)
                    GPIO.output(24,True)
                    reportlog = "Current song: "+ randomsong
                    writeloginf(reportlog)
                    while pygame.mixer.music.get_busy() == True:
                    
                        sleep(0.5)
            
                        if GPIO.input(25) == GPIO.HIGH:
                            
                             sleep(3)
                             if GPIO.input(25) == GPIO.HIGH and GPIO.input(7) == GPIO.HIGH:
                                 pygame.mixer.music.stop()
                                 quotelist1 = ["./conversation/afteroff.mp3","./conversation/afteroff2.mp3"]
                                 rand1 = random.choice(quotelist1)
                                 if rand1 == "./conversation/afteroff2.mp3" :
                                     pygame.mixer.music.set_volume(0.9)
                                 pygame.mixer.music.load(rand1)
                                 pygame.mixer.music.play()
                                 GPIO.output(18, True)
                                 while pygame.mixer.music.get_busy() == True:
                                     continue
                                 sleep(1)
                                 writeloginf("Good morning!")
                                 #open("backup.data", 'w').close()
                                 try: 
                                     backupfile.close()
                                 except:
                                     writelogerr("Cannot close file")
                                 backupfile = open("./data/backup.data","w")
                                 backupfile.write("10")
                                 backupfile.flush()
                                 backupfile.close()
                                 break
                        if GPIO.input(7) == GPIO.HIGH:
                             pygame.mixer.music.stop()
                             for x in range(0,10):
                                 sleep(30)
                             playalarm()
                        GPIO.output(18, True)
                        sleep(0.1)
                        GPIO.output(18, False)
                    
        GPIO.output(4,True)
        sleep(2)
        GPIO.output(4,False)

        GPIO.output(24, False)
  






def playrandomloop(turnalarm,dir,customplaylist):
    musicvol = 10.0
    commandcode = [0,0]
    limitsong = 0
    if comm == "pending":
        commandcode = [0,1]
    if comm == "playing music":
        commandcode = [2,0]
    start_time = time.time()

    musicdic = os.listdir(dir)
    order = musicdic
    random.shuffle(order)
    order = customplaylist if customplaylist else order
    limitsong = len(order)
    for x in customplaylist:
        writeloginf("Loading.. "+ x)
    for song in order:
       writeloginf("Playing: "+ song)
       if song == "":
           break
       
       if limitsong > 0 :
        limitsong -= 1
        if commandcode[0] == 1:
                 commandcode = [0,0]
                 writeloginf("Exiting..")
                 if ardconnected == True:
                  sendard(("10" + "/n"))
                 break
        randomsong = song
        randomsong = dir + randomsong
        try:
         pygame.mixer.init()
        except:
             writelogerr("Cannot init")
    
        pygame.mixer.music.load(randomsong)
        pygame.mixer.music.play()
        if musicvol >= 1.1:
           pygame.mixer.music.set_volume(0.3) 
        else:
            pygame.mixer.music.set_volume(musicvol) 
        pin26 = 0
        pin22 = 0
        timeout = 0.0
        lastsecond = 0.0
        delay = False
        betw = 0.5
        
        while pygame.mixer.music.get_busy() == True:
         # if turnalarm == True:
              #schedule.run_pending()
          #    pass

          
          sleep(0.25)
          if GPIO.input(7) == GPIO.HIGH:
                   sleep(0.01)
          rantime = time.time() - start_time
          if delay == False:
            if GPIO.input(25) == GPIO.HIGH:
                GPIO.output(18, True)
                GPIO.output(14, True)
                pin22 += 1
                timeout = 2.0
                delay = True
                writeloginf(str("Pin 22 pressed: "+ str(pin22)))

                #writeloginf(str("timeout:"+ str(timeout)))
            if GPIO.input(7) == GPIO.HIGH:
                GPIO.output(18, True)
                GPIO.output(14, True)
                pin26 += 1
                timeout = 2.0
                delay = True
                writeloginf(str("Pin 26 pressed: "+str(pin26)))
          if int(rantime*10) >= int(lastsecond*10) and timeout*10 > 0 :
            if delay == True:
             timeout -= 0.25 + betw
            else:
                 timeout -= 0.25
            lastsecond = rantime
            #writeloginf(str("timeout:"+ str(int(timeout))))
          if delay == True:
           sleep(betw)
           GPIO.output(14, False)
           delay = False
          if timeout <= 0:
                    if pin22 != 0 or pin26 != 0:
                     if commandcode[0] == 0 or commandcode[1] == 0:
            
                      commandcode[0] = pin22
                      commandcode[1] = pin26
                      #if ardconnected == True:
                      #   stringint = pin22 or pin26       
                      #   sendard((str(stringint) + "/n"))
                      sleep(1)
                      writeloginf(str("Command: "+ str(commandcode[0]) + " "+ str(commandcode[1])))

                    pin22 = 0
                    pin26 = 0

                    GPIO.output(18, False)
          if not commandcode[0] == 0 or not commandcode[1] == 0:
             #command
             if commandcode[0] == 2:
                  pin26 = 0
                  pin22 = 0
                  timeout = 0.0
                  lastsecond = 0.0
                  delay = False
                  betw = 0.5
                  while GPIO.input(25) == GPIO.LOW:

                                    sleep(0.25)
                                    GPIO.output(24, True)
                                    rantime = time.time() - start_time
                                    if delay == False:
                                        

                                            #writeloginf(str("timeout:"+ str(timeout)))
                                        if GPIO.input(7) == GPIO.HIGH:
                                            GPIO.output(18, True)
                                            GPIO.output(14, True)
                                            pin26 += 1
                                            timeout = 2.0
                                            delay = True
                                            writeloginf(str("Pin 26 pressed: "+str(pin26)))
                                    if timeout*10 != 0 and int(rantime*10) >= int(lastsecond*10) and timeout*10 > 0 :
                                     if delay == True:
                                        timeout -= 0.25 + betw
                                     else:
                                            timeout -= 0.25
                                    lastsecond = rantime
                                    #writeloginf(str("timeout:"+ str(int(timeout))))
                                    if delay == True:
                                     sleep(betw)
                                     GPIO.output(14, False)
                                     delay = False
                                    if timeout <= 0:
                                            if pin22 != 0 or pin26 != 0:
                                                if commandcode[0] == 0 or commandcode[1] == 0:
            
                                                 commandcode[0] = pin22
                                                 commandcode[1] = pin26
                                                 if ardconnected == True:
                                                    stringint = pin22 or pin26
                                                    sendard((str(stringint) + "/n"))
                                                 sleep(1)
                                                 writeloginf(str("Command: "+ str(commandcode[0]) + " "+ str(commandcode[1])))
                                                 limitsong = commandcode[1]
                                                 writeloginf("Song limit: "+ str(limitsong))
                                                 commandcode = [0,0]

                                            pin22 = 0
                                            pin26 = 0

                                            GPIO.output(24, False)
                                            sleep(0.5)
                  GPIO.output(24, True)
                  sleep(1)
                  GPIO.output(24, False)
                  commandcode = [0,0]
                  sleep(3)
             if commandcode[1] == 2:
                  pin26 = 0
                  pin22 = 0
                  timeout = 0.0
                  lastsecond = 0.0
                  delay = False
                  betw = 0.5
                  while GPIO.input(25) == GPIO.LOW:

                                    sleep(0.25)
                                    GPIO.output(24, True)
                                    rantime = time.time() - start_time
                                    if delay == False:
                                        

                                            #writeloginf(str("timeout:"+ str(timeout)))
                                        if GPIO.input(7) == GPIO.HIGH:
                                            GPIO.output(18, True)
                                            GPIO.output(14, True)
                                            pin26 += 1
                                            timeout = 2.0
                                            delay = True
                                            writeloginf(str("Pin 26 pressed: "+str(pin26)))
                                    if timeout*10 != 0 and int(rantime*10) >= int(lastsecond*10) and timeout*10 > 0 :
                                     if delay == True:
                                        timeout -= 0.25 + betw
                                     else:
                                            timeout -= 0.25
                                    lastsecond = rantime
                                    #writeloginf(str("timeout:"+ str(int(timeout))))
                                    if delay == True:
                                     sleep(betw)
                                     GPIO.output(14, False)
                                     delay = False
                                    if timeout <= 0:
                                            if pin22 != 0 or pin26 != 0:
                                                if commandcode[0] == 0 or commandcode[1] == 0:
            
                                                 commandcode[0] = pin22
                                                 commandcode[1] = pin26
                                                 if ardconnected == True:
                                                    stringint = pin22 or pin26
                                                    sendard((str(stringint) + "/n"))
                                                 sleep(1)
                                                 writeloginf(str("Command: "+ str(commandcode[0]) + " "+ str(commandcode[1])))
                                                 musicvol = commandcode[1] /10
                                                 pygame.mixer.music.set_volume((commandcode[1] /10)) 
                                                 commandcode = [0,0]

                                            pin22 = 0
                                            pin26 = 0

                                            GPIO.output(24, False)
                                            sleep(0.5)
                  GPIO.output(24, True)
                  sleep(1)
                  GPIO.output(24, False)
                  commandcode = [0,0]
                  sleep(3)
             if commandcode[1] == 1:
                 if ardconnected == True:
                  sendard((str("5") + "/n"))
                 commandcode = [0,0]
                 break
             if commandcode[0] == 1:
                 writeloginf("Stop")

                 
                 
                 pygame.mixer.music.set_volume(0.9)
                 pygame.mixer.music.load("./conversation/wantmore.mp3")
                 pygame.mixer.music.play()
                 GPIO.output(18, True)
                 confirm = False
                 while pygame.mixer.music.get_busy() == True:
                     if GPIO.input(7) == GPIO.HIGH:
                         confirm = True
                         GPIO.output(14, True)
                 if confirm == False:
                     pygame.mixer.music.set_volume(0.9)
                     pygame.mixer.music.load("./conversation/quitmusic.mp3")
                     pygame.mixer.music.play()
                     GPIO.output(14, False)
                     GPIO.output(18, False)
                     confirm = False
                     while pygame.mixer.music.get_busy() == True:
                         continue
                     if ardconnected == True:
                      sendard((str("10") + "/n"))
                     break
                 else:
                      GPIO.output(14, False)
                      GPIO.output(18, False)
                      confirm = False
                      commandcode = [0,0]
                
        try:
         pygame.mixer.music.stop()
        except:
         writelogerr("Music stop failed")
       else:
           break
    writeloginf("Completed")


def getmusiclist():
    musicdic = os.listdir("./music/")
    musicdic.sort()
    GPIO.output(4, True)
    with codecs.open("./data/songlist.data","w+","utf-8") as clientcommandfile:
        for index in musicdic:
            sleep(0.1)
            text = str(musicdic.index(index)) + " | " + index
            writeloginf("Writing list: " + text)
            clientcommandfile.write(text+"~"+"\n")
        GPIO.output(4, False)
        clientcommandfile.close()




def onclient(c,addr,data):

        writeloginf('Establishing connection with client'+ str(addr) + " C: "+ str(c))
        GPIO.output(4, True)


        c.send(data.encode())
        sleep(3)
        file = open("./data/playlist.data","r").read()
        file.replace(" ","")
        if file != "" or file != None:
            c.send(file.encode())
        while True :
            datacode = c.recv(1024)
            datacode = datacode.decode()
            if datacode:
             writeloginf(("Data: "+datacode))
            clientcommandfile =  open("./data/clientcomm.data","w+")
            clientcommandfile.write(datacode)
            clientcommandfile.flush()    
            datafile = clientcommandfile.read()
            clientcommandfile.close()
            datafile = datafile.replace(' ','')
            commandlist = datafile.split('|')
        
            if commandlist[0] == '00':
                writeloginf("Breaking loop")
                #lol = LOL     exception => break thread
                break

                        
                


def serverhandler(alarm):
        alarmtime = alarm
        with open("./data/songlist.data","r") as filedata:
            listl = filedata.read().split("~")
        senddata = alarm + " " + str(len(listl))
        command = 0
        sk = socket.socket()
        try:
         ni.ifaddresses('wlan0')
         host = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
        except:
            writelogerr("Cant get IP through netifaces")
            host = "192.168.0.106"
        writeloginf("IP: "+ host)
        port = 3939    
        try:
          sk.bind((host, port))  
          sk.listen(5)
          datafilehandler(host,2)
        except:
            GPIO.output(18,True)
            writelogerr("Cannot open port")
        c, addr = sk.accept() 
        writeloginf('Got connection from'+ str(addr) + " C: "+ str(c))
        serverthread = threading.Thread(target=onclient, args=(c,addr,senddata,))
        serverthread.start()
        while GPIO.input(25) == GPIO.LOW:
            sleep(2)
            with open("./data/clientcomm.data","r+") as clientcommandfile:
                clientcommand = clientcommandfile.read()
                #clientcommand = clientcommand.replace(' ','')
                commandlist = clientcommand.split('|')
                if commandlist[0]:
                 writeloginf("Reading client command.. "+ str(commandlist[0]))
                clientcommandfile.close()

                if commandlist[0] == "00":
                    backupfile = open("./data/clientcomm.data","w")
                    backupfile.write("01")
                    backupfile.flush()
                    backupfile.close()
                    break
                elif commandlist[0] == '02':
                    # can use Quete
                    cam = threading.Thread(target=camera, args=())
                    cam.start()
                    writeloginf("Starting Camera detection")
                    while commandlist[0] == '02' and commandlist[1] == '01':
                     sleep(0.1)
                     if  commandlist[1] == '01':
                       with open("./data/CamState.data","w+") as State:
                        State.write("False")
                        State.close()
                       with open("./data/Handpos.data","r") as sendfile:
                        senddata = sendfile.read()
                        sendfile.close()
                        c.send(str(senddata))
                      
                    if commandlist[1] == '02':
                          with open("./data/CamState.data","w+") as State:
                            State.write("True")
                            State.close()
                elif commandlist[0] == "03":
                    alarmtime = commandlist[1]
                    command = 1
                elif commandlist[0] =="04":
                    #playlist
                    with open("./data/playlist.data","w") as playlist:
                        stringwrite = clientcommand
                        stringwrite = stringwrite.replace("04 ","")
                        playlist.write(stringwrite)
                        playlist.close()

                    command = 2
        GPIO.output(4, False)
        
        return alarmtime,command


def camera():
   
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
    with open("./data/CamState.data","w+") as State:
        State.write("False")
        State.close()
    while True:
            try :
                 state = open("./data/CamState.data","r").read()
                 
                 if state =="True" :
                     break;
            except:
                 print("cannot open file")
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
                writeloginf(str(int(w/2) + x) + ' , ' + str(int(h/2) + y))
                GPIO.output(12, True)
                facelocationx = int(w/2) + x
                facelocationy = int(h/2) + y
                X = int((x / width)*100)
                Y = int((x / height)*100)
                print("X: "+ str(X)) #  %
                print("Y: "+ str(Y))
                sleep(0.2)
                try :
                 datafile = open("./data/Handpos.data","w+")
    
                except:
                 print("cannot open file")
                datafile.write(str(X)+ "|"+str(Y))
                datafile.flush()
                datafile.close()

    #video_capture.release()
    #cv2.destroyAllWindows()
#   --------------------------------------------------------------------VARIABLE AND FILES OPERATION--------------------------------------------------------------------


pin26 = 0
pin22 = 0
timeout = 0.0
lastsecond = 0.0
delay = False
betw = 0.5
commandcode = [0,0]
alarmtime = '07:20'

try:
    alarmtime = open("./data/alarm.data","r").read()
except:
    writeloginf("Cannot read alarm")
sleep(1)
backupfile.truncate(2)
commnew = commnew.replace(' ','')
def datafilehandler(inputdata,mode):
    pass

  #FIX LATER
    #datafile = open("./data/data.data","r+")
    #print(datafile.read() + "/")
    #datals = datafile.readline()
    #data = float(datals)
    #data += 1.0
    #datafile.write(str(data))
    #datafile.close()
    #writeloginf("Version: "+ str(data/100.0))





    #datafile = open("./data/data.dat","r+")
    #print(datafile.readline())
    #datals = datafile.readlines()
    #data = [[],[],[],[],[],[],[],[],[]]
    #writeloginf("Handling file..")
    #print(datals)
    #count = 0
    #for line in datals:
    #    writeloginf("Reading file..")
    #    writeloginf(str(datals.index(line)) + " : "+ line)
    #    data[count] = line.split(':')
    #    count += 1
    #datafile.seek(0,0)
    #datafile.write("TungStudio\n")
    #data[0][1] = str(float(data[0][1]) + 0.01)
    #data[1][1] = inputdata if mode == 1 else data[1][1]
    #data[2][1] = inputdata if mode == 2 else data[2][1]
    #data[3][1] = inputdata if mode == 3 else data[3][1]
    #count = 0
    #for writeln in datals:
    #    writedata = data[count][0] +":"+  data[count][1] + "\n"
    #    datafile.writelines(writedata)
    #    datafile.flush()
    #    count += 1
    #datafile.close()
    
try :
    datafile = open("./data/data.data","r")
    datals = datafile.read()
    datafilehandler(logname,3)
    
except:
    writelogerr("Cannot open file data")
def returnfile():
    commnew = open("./data/backup.data","r").read()
    commnew = commnew.replace(' ','')
    comm = ''
    for i in range(0, len(commnew)): 
     if i <= 2: 
        comm = comm + commnew[i] 

    return comm
def returnalarm(data):
    writeloginf("Setting up alarm..")
    commnew = open("./data/alarm.data","r").read()
    commnew = commnew.replace(' ','')
    comm = ''
    for i in range(0, len(commnew)): 
     if i <= 2: 
        comm = comm + commnew[i] 
    
    try:
        writeal = open("./data/alarm.data","w")
        writeal.write(data)
        writeal.close()
    except:
        writelogerr("Cannot write file")
    writeloginf("Alarm set at "+ data)
    return comm       
writeloginf("File:" + comm + "/end")
for i in range(0, len(commnew)): 
    if i <= 2: 
        comm = comm + commnew[i] 
        
writeloginf("File:" + comm + "/end")
try: 
    backupfile.close()
except:
    writelogerr("Cannot close file")
backupfile = open("./data/backup.data","w")
backupfile.write("")
backupfile.flush()
backupfile.close()
#lcd.main()
#---------------------------------------------------------------  MAIN  -------------------------------------------------------------------------
while True:

    sleep(0.01)
    GPIO.output(24, True)
    if comm == "01":
        writeloginf("Pending detected")
        GPIO.output(4, True)
        sleep(3)
        if GPIO.input(25) == GPIO.HIGH:
            commandcode = [0,0]
            GPIO.output(14, True)
            sleep(1)
            GPIO.output(14, False)
        else:
            commandcode = [0,1]
        GPIO.output(4, False)
        #open("./data/backup.data", 'w').close()
        
        sleep(0.5)
        #backupfile.write("10")
        #backupfile.truncate(2)
        #backupfile.flush()
        try: 
            backupfile.close()
        except:
            writelogerr("Cannot close file")
        backupfile = open("./data/backup.data","w")
        backupfile.write("10")
        backupfile.flush()
        backupfile.close()
        comm = returnfile()
    if comm == "02":
        writeloginf("Music detected")
        commandcode = [2,0]
       # open("./data/backup.data", 'w').close()
        sleep(0.5)
        #backupfile.write("10")
        #backupfile.truncate(2)
        #backupfile.flush()
        try: 
            backupfile.close()
        except:
            writelogerr("Cannot close file")
        backupfile = open("./data/backup.data","w")
        backupfile.write("10")
        backupfile.flush()
        backupfile.close()
        comm = returnfile()
    if comm == "03":
        #open("./data/backup.data", 'w').close()
        #sleep(0.5)
        #backupfile.write("10")
        #backupfile.truncate(2)
        #backupfile.flush()
        try: 
            backupfile.close()
        except:
            writelogerr("Cannot close file")
        backupfile = open("./data/backup.data","w")
        backupfile.write("10")
        backupfile.flush()
        backupfile.close()
        writeloginf("Test file")
        comm = returnfile()
    rantime = time.time() - start_time
    if delay == False:
        if GPIO.input(25) == GPIO.HIGH:
            GPIO.output(18, True)
            GPIO.output(14, True)
            pin22 += 1
            timeout = 4.0
            delay = True
            writeloginf(str("Pin 22 pressed: "+ str(pin22)))
            #writeloginf("File:" + comm + "/end")
            if ardconnected == True:
             stringint = pin22 or pin26  
             sendard((str(stringint) + "/n"))
            #writeloginf(str("timeout:"+ str(timeout)))
        if GPIO.input(7) == GPIO.HIGH:
            GPIO.output(18, True)
            GPIO.output(14, True)
            pin26 += 1
            timeout = 4.0
            delay = True
            writeloginf(str("Pin 26 pressed: "+str(pin26)))
            #writeloginf("File:" + comm + "/end")
    if timeout*10 != 0 and int(rantime*10) >= int(lastsecond*10) and timeout*10 > 0 :
        if delay == True:
         timeout -= 0.01 + betw
        else:
             timeout -= 0.01
        lastsecond = rantime
       
            
        #writeloginf(str("timeout:"+ str(int(timeout))))
    if delay == True:
       sleep(betw)
       GPIO.output(14, False)
       delay = False
    if timeout <= 0:
                if pin22 != 0 or pin26 != 0:
                 if commandcode[0] == 0 or commandcode[1] == 0:
            
                  commandcode[0] = pin22
                  commandcode[1] = pin26
                  if ardconnected == True:
                     stringint = pin22 or pin26
                     sendard((str(stringint) + "/n"))
                  sleep(1)
                  writeloginf(str("Command: "+ str(commandcode[0]) + " "+ str(commandcode[1])))

                pin22 = 0
                pin26 = 0

                GPIO.output(18, False)
    if not commandcode[0] == 0 or not commandcode[1] == 0:
         GPIO.output(24, False)
         # ---------------------COMMANDS------------------------------------------
        
         if commandcode[0] == 2 and commandcode[1] == 0:
             #play music
             #open("./data/backup.data", 'w').close()
             
             #backupfile.write("02")
             #backupfile.flush()
             try: 
                 backupfile.close()
             except:
                 writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w")
             backupfile.write("02")
             backupfile.flush()
             backupfile.close()
             playrandomloop(False,"./music1/",[])
             #open("./data/backup.data", 'w').close()
             
             #backupfile.write("10")
             #backupfile.flush()
             try: 
                 backupfile.close()
             except:
                 writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w")
             backupfile.write("10")
             backupfile.flush()
             backupfile.close()
             commandcode = [0,0]
         elif commandcode[0] == 4:
             playlist =  open("./data/playlist.data","r") 
             plstr = playlist.read()
             plstr = plstr.replace(' ','')
             plstrls = plstr.split('|')
             
             musicdic = os.listdir("./music/")
             musicdic.sort()
             pllist = [""] *( len(plstrls)+1)
             print(pllist)
             writeloginf("Range "+str(len(pllist))+" | "+ str(len(plstrls)))
             listcount = 0
             for i in plstrls:
                 #index = plstrls.index(i)
                 index = int(i)   #str(musicdic[index])
                 writeloginf("Reading playlist.. "+ str(musicdic[index])+" ID: "+ str(i))
                 pllist[listcount] = ( str(musicdic[index]))
                 listcount += 1
                 writeloginf("File: "+ pllist[listcount])
             playlist.close()
             if  commandcode[1] == 0:
                 playrandomloop(False,"./music/",pllist)
                 commandcode = [0,0]
             elif commandcode[1] == 1:
                 try: 
                    backupfile.close()
                 except:
                  writelogerr("Cannot close file")
                 backupfile = open("./data/backup.data","w+")
                 backupfile.write("01")
                 backupfile.flush()
                 comm = backupfile.read()
                 backupfile.flush()
                 backupfile.close()
                 playrandomloop(False,"./music/",pllist)
                 commandcode = [0,1]
                 try:
                  pygame.mixer.init()
                 except:
                  writelogerr("Cannot init")
             
                 pygame.mixer.music.load("./conversation/setupcomplete.mp3")
                 pygame.mixer.music.play()
         elif commandcode[0] == 5 and commandcode[1] == 0:
             #play music
             #open("./data/backup.data", 'w').close()
             
             #backupfile.write("02")
             #backupfile.flush()
             try: 
                 backupfile.close()
             except:
                 writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w")
             backupfile.write("02")
             backupfile.flush()
             backupfile.close()
             playrandomloop(False,"./music/",[])
             #open("./data/backup.data", 'w').close()
             
             #backupfile.write("10")
             #backupfile.flush()
             try: 
                 backupfile.close()
             except:
                 writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w")
             backupfile.write("10")
             backupfile.flush()
             backupfile.close()
             commandcode = [0,0]
         elif commandcode[1] == 5 and commandcode[0] == 2:
             getmusiclist()
             commandcode = [0,0]
         elif commandcode[0] == 4 and commandcode[1] == 2:
             camerathread = threading.Thread(target=camera,)
             camerathread.start()
         elif commandcode[0] == 0 and commandcode[1] == 3:
             #try:
             # schedule.every().day.at(alarmtime).do(playalarm)
             #except:
             #    writelogerr("Cannot set alarm")
             try: 
              backupfile.close()
             except:
              writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w+")
             backupfile.write("01")
             backupfile.flush()
             comm = backupfile.read()
             backupfile.flush()
             backupfile.close()
             playrandomloop(True,"./sleep/",[])
             commandcode = [0,1]
             try:
                 pygame.mixer.init()
             except:
                writelogerr("Cannot init")
             
             pygame.mixer.music.load("./conversation/setupcomplete.mp3")
             pygame.mixer.music.play()
         elif commandcode[0] == 2 and commandcode[1] == 1:
             #try:
             # schedule.every().day.at(alarmtime).do(playalarm)
             #except:
             #    writelogerr("Cannot set alarm")
             playrandomloop(True,"./music1/",[])
             commandcode = [0,1]
             try:
                 pygame.mixer.init()
             except:
                writelogerr("Cannot init")
             
             pygame.mixer.music.load("./conversation/setupcomplete.mp3")
             pygame.mixer.music.play()
         elif commandcode[0] == 5 and commandcode[1] == 1:
             #try:
             # schedule.every().day.at(alarmtime).do(playalarm)
             #except:
             #    writelogerr("Cannot set alarm")
             try: 
              backupfile.close()
             except:
              writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w+")
             backupfile.write("01")
             backupfile.flush()
             comm = backupfile.read()
             backupfile.flush()
             backupfile.close()
             playrandomloop(True,"./music/",[])
             commandcode = [0,1]
             try:
                 pygame.mixer.init()
             except:
                writelogerr("Cannot init")
             
             pygame.mixer.music.load("./conversation/setupcomplete.mp3")
             pygame.mixer.music.play()
         elif commandcode[1] == 3 and commandcode[0] == 3:
             writeloginf("Test")
             #open("./data/backup.data", 'w').close()
             
             #backupfile.write("03")
             #backupfile.flush()
             try: 
                 backupfile.close()
             except:
                 writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w")
             backupfile.write("03")
             backupfile.flush()
             backupfile.close()
             playalarm()
             commandcode = [0,0]
         elif commandcode[1] == 1 and commandcode[0] == 0:
             count = 0
             delay = 600   #sec    10m
            
             #open("./data/backup.data", 'w').close()
             
             #backupfile.write("01")
             #backupfile.flush()
             try: 
                 backupfile.close()
             except:
                 writelogerr("Cannot close file")
             backupfile = open("./data/backup.data","w+")
             backupfile.write("01")
             backupfile.flush()
             comm = backupfile.read()
             backupfile.flush()
             backupfile.close()
             
             writeloginf("Alarm set at "+ alarmtime)
             try:
                 schedule.every().day.at(alarmtime).do(playalarm)
                 schedule.every().day.at("13:20").do(playalarm)
             except :
                 writelogerr("Cannot set alarm")
             
             if ardconnected == True:
                     sendard(("11/n"))
             writeloginf("File:" + comm + "/end")
             schedulecheck = 0
             while True:
                 count += 1
                 if GPIO.input(25) == GPIO.HIGH:
                     commandcode = [2,0]
                     writeloginf("Breaking loop..")
                     break
                 if count > delay:
                    sleep(30)
                    schedule.run_pending()
                    schedulecheck += 1
                    if schedulecheck % 60 == 0:
                        writeloginf("Checked number"+str(schedulecheck))
                    if count == delay + 1:
                         writeloginf("30s delay started..")
                 else:
                     sleep(1)
                     schedule.run_pending()
                     if count == delay:
                         writeloginf("30s delay starting..")
                 schedule.run_pending()
                 if comm == "03":
                      try: 
                        backupfile.close()
                      except:
                        writelogerr("Cannot close file")
                        backupfile = open("./data/backup.data","w")
                        backupfile.write("10")
                        backupfile.flush()
                        backupfile.close()
                     #backupfile.write("10")
                     #backupfile.flush()
                      break 

         elif commandcode[0] == 3:
             #start communication
             writeloginf("Server started")
             GPIO.output(14,GPIO.HIGH)
             sleep(1)
             GPIO.output(14,GPIO.LOW)
             

             alarmtime,command = serverhandler(alarmtime)
             if command == 1:
                alarmtime = alarmtime[:5] #cut string
                returnalarm(alarmtime)
                try:
                 pygame.mixer.init()
                except:
                 writelogerr("Cannot init")
             
                pygame.mixer.music.load("./conversation/setupcomplete.mp3")
                pygame.mixer.music.play()
             GPIO.output(4, False)
             commandcode = [0,0]


         elif commandcode[0] == 1 and commandcode[1] == 0:
             try:
                 pygame.mixer.init()
             except:
                writelogerr("Cannot init")
             
             pygame.mixer.music.load("USSR.mp3")
             pygame.mixer.music.play()
             commandcode = [0,0]
             while pygame.mixer.music.get_busy() == True:
                 continue
         elif commandcode[0] == 9:

               #open("./data/backup.data", 'w').close()
               #backupfile.flush()
               #backupfile.write("10")
               #backupfile.flush()
               #backupfile.close()
                try: 
                 backupfile.close()
                except:
                    writelogerr("Cannot close file")
                    backupfile = open("./data/backup.data","w")
                    backupfile.write("10")
                    backupfile.flush()
                    backupfile.close()
                    GPIO.cleanup()
                break
         else:
          commandcode = [0,0]
#------------------------------------------------------------------END--------------------------------------------------------------------------------------------------------
