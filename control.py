import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit
import serial_se_re
import threading

serialPort = serial_se_re.SerialPort()

def SendDataCommand():
    serialPort.Stuur("Basic Send")

def Verbinden():
    serialPort.Open("COM13",19200)

def InsertText():
    print(serialPort.Lees())
    #tekst_veld.insert(message)

thread = threading.Thread(target=InsertText)
thread.start()

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

instert_text = QPushButton('add')
layout.addWidget(instert_text)
instert_text.clicked.connect(lambda: InsertText())

tekst_veld = QLineEdit()
layout.addWidget(tekst_veld)

window.setLayout(layout)
window.show()
app.exec_()
