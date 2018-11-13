import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit
import serial_se_re
import threading
from time import sleep

serialPort = serial_se_re.SerialPort()
lis = []

def SendDataCommand():
    serialPort.Stuur("Basic Send")

def Verbinden():
    serialPort.Open("COM5",19200)

def InsertText():
    lis.append(serialPort.Lees())
    print(serialPort.Lees())
    #tekst_veld.insert(message)

def printlist():
    print(lis)

def GemiddeldeTemp():
    temp = [20, 21, 20, 19, 20, 21]
    sum = 0
    for i in temp:
        sum += i

    avg = sum / len(temp)
    return(avg)

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
layout.addWidget(tekst_veld)



window.setLayout(layout)
window.show()
app.exec_()
