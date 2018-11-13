import serial
import sys
import _thread
import threading
import time

class SerialPort:
    def __init__(self):
        self.comportName = "COM5"
        self.baud = 19200
        self.isopen = False
        self.timeout = None
        self.serialport = serial.Serial()
        temp = {}


    def __del__(self):
        try:
            if self.serialport.is_open():
                self.serialport.close()
        except:
            print("Kan de COM port niet sluiten, error: ", sys.exc_info()[0] )

    def CheckOpen(self):
        return self.isopen

    def Open(self,port,baud):
        if not self.isopen:
            self.serialport.port = port
            self.serialport.baudrate = baud
            try:
                self.serialport.open()
                self.isopen = True
            except:
                print("Kan port niet openen, error: ", sys.exc_info()[0])

    def Sluiten(self):
        if self.isopen:
            try:
                self.serialport.close()
                self.isopen = False
            except:
                print("Kan port niet sluiten, error: ", sys.exc_info()[0])


    def Stuur(self,message):
        if self.isopen:
            try:
                # Ensure that the end of the message has both \r and \n, not just one or the other
                newmessage = message.strip()
                newmessage += '\r\n'
                self.serialport.write(newmessage.encode('utf-8'))
            except:
                print("Error sending message: ", sys.exc_info()[0] )
            else:
                return True
        else:
            return False

    def Lees(self):
        if self.isopen:
            try:
                while(1):
                    message = self.serialport.read()
                    time.sleep(0.01)

                    #split and check
                    #key, value = message.split('b')
                    #pair = {key:value}
                    #if key == 1:
                    #    temp.update(pair)
                    #if key == 2:
                    #    print(pair)
                    #if key == 3:
                    #    print(pair)
                    return(message)
            except Exception:
                print("error")
        else:
            print("Cannot open serial port")
