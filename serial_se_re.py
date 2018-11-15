import serial
import sys
import _thread
import threading
from threading import Thread
import time

class SerialPort(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.comportName = "COM3"
        self.baud = 19200
        self.isopen = False
        self.timeout = None
        self.min = 20
        self.max = 140
        self.lis = []
        self.serialport = serial.Serial()

        #Thread.__init__(self)
        #self.val = val

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
                self.serialport.write(newmessage.encode('utf-8'))
            except:
                print("Error sending message: ", sys.exc_info()[0] )
            else:
                return True
        else:
            return False

    def _Lees(self):
        if self.isopen:
            try:
                while(1):
                    message = ord(self.serialport.read())
                    time.sleep(0.01)
                    self.lis.append(message)
            except Exception:
                print("error")
        else:
            print("Cannot open serial port")

    def Lees(self):
        if self.isopen:
            threading.Thread(target=self._Lees).start()
        else:
            print("Cannot start thread for _Lees")

    def Return_lis(self):
        if self.isopen:
            return self.lis
        else:
            print("cant return list")

    def Return_temp(self):
        if self.isopen:
            temp = self.lis[::3]
            return temp
        else:
            print("Cant return temperature list")

    def Return_licht(self):
        if self.isopen:
            licht = self.lis[1::3]
            return licht
        else:
            print("Cant return licht list")

    def Return_afstand(self):
        if self.isopen:
            afstand = self.lis[2::3]
            return afstand
        else:
            print("Cant return aftand list")

    def Return_min(self):
        if self.isopen:
            min = self.min
            return min
        else:
            print("Cant return min value")

    def Update_min(self, update):
        if self.isopen:
            newvalue = update
            min = update
            self.min = min
        else:
            print("Cant return licht list")

    def Return_max(self):
        if self.isopen:
            max = self.max
            return max
        else:
            print("Cant return max value")

    def Update_max(self, update):
        if self.isopen:
            newvalue = update
            max = update
            self.max = max
        else:
            print("Can't update max value")
