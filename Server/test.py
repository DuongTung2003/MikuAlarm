import serial
from time import sleep
import sys
import os
try:
    arddata = serial.Serial('/dev/ttyACM0',9600,timeout = 5)
    ardconnected = True
except:
    print("Cannot connect to arduino")
else:
    ardconnected = True


def writeir(data):
    name = "IR"
    count = 1
    filelist = os.listdir("./IRList/")
    if filelist:
        for IR in filelist:
          
          IR = "./IRList/" + IR
          print(IR)
          with open(IR,"r") as checkfile:
           check = checkfile.read()
           if check == data.decode():
                    print(data.decode() +" is already exist")
                    with open("./IRList/"+name,"w") as file:
                        file.write(data.decode())
                        file.close()
           else:
             if count == len(filelist) and IR !="./IRList/"+ name +str(count)+".txt":
                
            #write
              name += str(count)+ ".txt"
              print("Creating file.. " + name)
              
              with open("./IRList/"+name,"w+") as file:
                file.write(data.decode())
                file.close()
             else:
                count += 1
while True :
    data = b''
    variable = "99/n"
    data = arddata.read(64)   
    print(str(data))
    if data != b'':
        writeir(data)
   # coded = variable.encode()
    #try:
    #    arddata.write(coded)
    #except:
    #    pass
    #rec = None
    sleep(1)