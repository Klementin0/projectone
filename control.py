import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit
import serial_se_re
import threading
from time import sleep

serialPort = serial_se_re.SerialPort()

def SendDataCommand():
    serialPort.Stuur("Basic Send")

def Verbinden():
    serialPort.Open("COM3",19200)
    serialPort.Lees()

def InsertText():
    serialPort.Sluiten()

def printlist():
    print(serialPort.Return_lis())


def AfstandPull():
    lis = serialPort.Return_lis()
    AfstandList = lis[2::3]
    LaatsteAfstand = lis[len(lis)-1]
    if(LaatsteAfstand == 4):
        print("Ingerolt")
        #Functie voor groen licht aan, geel licht uit
    elif(LaatsteAfstand == 170):
        print("Uitgerold")
        #Functie voor groen licht(eventueel een ander groen licht) aan, geel licht uit
    else:
        print("Aan het rollen")
        #functie voor groene lichten uit, geel licht aan

def LichtDonker():
    light = serialPort.Return_light()
    if (len(light) >= 60):
        light = light[-60:]
        sum = 0
        for i in light:
            sum += i
        if sum >= 50:
            return 2 #uitrollen als niet uitgerold!
        elif sum <= 10:
            return 1 #inrollen als niet ingerold!
        else:
            return 0 #doe niks
    else:
        return 0 #doe niks als er nog geen 3 min aan waarden is!

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()
window.setWindowTitle('Project One: Zonnescherm Bedieningseenheid')

connect_button = QPushButton('Connect')
layout.addWidget(connect_button)
connect_button.clicked.connect(lambda: Verbinden())

stuur_data_button = QPushButton('Stuur message')
layout.addWidget(stuur_data_button)
stuur_data_button.clicked.connect(lambda: SendDataCommand())

list_print_buttn = QPushButton('list')
layout.addWidget(list_print_buttn)
list_print_buttn.clicked.connect(lambda: LichtDonker())

instert_text = QPushButton('add')
layout.addWidget(instert_text)
instert_text.clicked.connect(lambda: InsertText())

#tekst_veld = QLineEdit()
#layout.addWidget(tekst_veld)

window.setLayout(layout)
window.show()
app.exec_()
