import serial_se_re
from tkinter import *

root = Tk() # Root word main Tk()

def command(d):
    print(d)

button1 = Button(root, text="click me", command=lambda : command("1"))
button1.pack()

root.mainloop() # Zorg er voor dat de window niet in een keer weggaat door er een loop van te maken.
