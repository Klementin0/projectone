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

def LichtPull():
    lis = serialPort.Return_lis()
    Lichtlis = lis[1::3]
    #kevins check op 3 minuten licht of niet
    #check of variabele licht aan of uit is voor 3 minuten
    Licht = 0
    if(Licht == 0):
        print("Het is donker")
    elif(Licht == 1):
        print("Het is licht")
    else:
        print("Ik kijk niet meer naar het licht")

def LichtDonker():
    sum = 0
    for i in lis:
        sum += i

    avg = sum / 60
    return(avg)

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
list_print_buttn.clicked.connect(lambda: printlist())

instert_text = QPushButton('add')
layout.addWidget(instert_text)
instert_text.clicked.connect(lambda: InsertText())

#tekst_veld = QLineEdit()
#layout.addWidget(tekst_veld)

window.setLayout(layout)
window.show()
app.exec_()
