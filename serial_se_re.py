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
                newmessage += '\r\n'
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
<<<<<<< HEAD
                    print(message)
=======
                    return message
>>>>>>> f8eac772772af5f6b955d634ce5d45b661ddef1f
            except Exception:
                print("error")
        else:
            print("Cannot open serial port")

<<<<<<< HEAD
    def Lees(self):
        if self.isopen:
            threading.Thread(target=self._Lees).start()
=======
    def Add_lis(self,message):
        if self.isopen:
            try:
                self.lis = lis.append(message)
            except:
                print("Nog geen lis: ", sys.exc_info()[0] )
            else:
                return True
        else:
            return False

    def Return_lis(self):
        if self.isopen:
            try:
                return self.lis
            except:
                print("Nog geen lis: ", sys.exc_info()[0] )
            else:
                return True
>>>>>>> f8eac772772af5f6b955d634ce5d45b661ddef1f
        else:
            print("Cannot start thread for _Lees")
