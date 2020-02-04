import socket
import os
import logging
from datetime import datetime
try:
    os.mkdir("ServerLogFiles/")
except :
    pass
format = "%(asctime)s: %(message)s"
logname =  "./ServerLogFiles/Log_"+str(datetime.now().month) +"_"+ str(datetime.now().day)+"_"+ str(datetime.now().hour)+"_"+ str(datetime.now().minute)+".log"
logging.basicConfig(filename=logname,format=format, level=logging.DEBUG,datefmt="%H:%M:%S")
from pocketsphinx import LiveSpeech, get_model_path

model_path = get_model_path()

#speech = LiveSpeech(
#    verbose=False,
#    sampling_rate=16000,
#    buffer_size=2048,
#    no_search=False,
#    full_utt=False,
#    hmm=os.path.join(model_path, 'en-us'),
 
#    lm=os.path.join(model_path, 'en-us.lm.bin'),
#    dic=os.path.join(model_path, 'cmudict-en-us.dict')
#)

#for phrase in speech:
#    logging.info(phrase)
#    print(phrase)


def writeloginf(log):
    logging.info(log)
    print(log)
def writelogwar(log):
    logging.warning(log)
    print(log)
def writelogerr(log):
    logging.error(log)
    print(log)

ver = "v0.14"
sk = socket.socket()
host = socket.gethostname() 
port = 6987               
sk.bind((host, port))       
data = "lol"
datacode = 0
sk.listen(5)  
logging.info("Server started")
print("Server started")
logging.info("Tung Studio ",ver)
print("Tung Studio ",ver)
def sendcommand():
    #-- terminal REGION
  while True:
    logging.info("Ready")   
    print("Ready")
    data = input(">")
    if data == "talk":
        speech = LiveSpeech(
        verbose=False,
        sampling_rate=16000,
        buffer_size=2048,
        no_search=False,
        full_utt=False,
        hmm=os.path.join(model_path, 'en-us'),
 
        lm=os.path.join(model_path, 'en-us.lm.bin'),
        dic=os.path.join(model_path, 'cmudict-en-us.dict')
        )

        for phrase in speech:
         logging.info(phrase)
         print("toi la van")
         break

    logging.info("Sending command..")
    print("Sending command..")
    try:
       c.send(data.encode()) #encode   -- nhớ decode :))
    except:
       logging.error("Cannot sent command to client:",c.getsockname())
       print("Cannot sent command to client:",c.getsockname())
    else:
           datacode = c.recv(1024)
           datacode = datacode.decode()
           logging.info("Client code: ",datacode)
           print("Client code: ",datacode)
           try:
                datacode = int(datacode)
               
           except :
               logging.info("Unexpected error")
               print("Unexpected error")
           else:
               if datacode == 0:
                   logging.info("Command not found")
                   print("Command not found")
               if datacode == 9:
                 c.close()   
                 break
  
    #--
while True:
    c, addr = sk.accept()  
    logging.info ('Got connection from', addr," C: ",c) # c client s server
    print('Got connection from', addr," C: ",c)
    if c:
       sendcommand()
       break
   
   