import serial.tools.list_ports
import random
import time
import  sys

class Serial_module:
    serial_handler = None
    mess = None
    processData = None
    port = None
    baudrate = None
    
    def getPort():
            ports = serial.tools.list_ports.comports()
            N = len(ports)
            commPort = "None"
            for i in range(0, N):
                port = ports[i]
                strPort = str(port)
                if "USB Serial Device" in strPort:
                    splitPort = strPort.split(" ")
                    commPort = (splitPort[0])
            return commPort
    
    def __init__(self, port, baudrate):
        self.port = port if port is not None else self.getPort() 
        self.baudrate = baudrate if baudrate is not None else 115200
        self.serial_handler = serial.Serial( self.port, self.baudrate)
        self.mess = ""
        self.processData = None
        
    def set_processData(self,func):
        self.processData = func
        
    def call_processData(self,*arg):
        if(self.processData is not None):
            self.processData(*arg)
        else: 
            print("processData hasnot been setted yet")
        
    def readSerial(self,mqtt_handler):
        bytesToRead = self.serial_handler.inWaiting()
        if (bytesToRead > 0):
            
            self.mess = self.mess + self.serial_handler.read(bytesToRead).decode("UTF-8")
            while ("#" in self.mess) and ("!" in self.mess):
                start = self.mess.find("!")
                end = self.mess.find("#")
                print(self.mess[start:end + 1])
                self.call_processData(self.mess[start:end + 1],mqtt_handler)
                if (end == len(self.mess)):
                    self.mess = ""
                else:
                    self.mess = self.mess[end + 1:]


# test in here
def processData_external(data,mqtt_handler):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print(splitData)
    
def main():
    my_serial = Serial_module("COM3",115200)
    my_serial.set_processData(processData_external)
    while True:
        try:
            my_serial.readSerial()
            time.sleep(1)
        except KeyboardInterrupt:
            break


if __name__ == "__main__":
    main()