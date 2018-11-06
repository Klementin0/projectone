import serial_se_re
from tkinter import *

root = Tk() # Root word main Tk()

serialPort = serial_se_re.SerialPort()

def SendDataCommand():
    serialPort.Stuur("KEK")

def Verbinden():
    serialPort.Open("COM5",19200)

button1 = Button(root, text="Connect", command=Verbinden())
button1.pack()

button2 = Button(root,text="Send Message",command=SendDataCommand)
button2.pack()

root.mainloop() # Zorg er voor dat de window niet in een keer weggaat door er een loop van te maken.
