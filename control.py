import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit
import serial_se_re
serialPort = serial_se_re.SerialPort()

def SendDataCommand():
    serialPort.Stuur("KEK")

def Verbinden():
    serialPort.Open("COM5",19200)

app = QApplication([])
window = QWidget()
layout = QVBoxLayout()

connect_button = QPushButton('Connect')
layout.addWidget(connect_button)
connect_button.clicked.connect(lambda: Verbinden())

stuur_data_button = QPushButton('Stuur message')
layout.addWidget(stuur_data_button)
stuur_data_button.clicked.connect(lambda: SendDataCommand())

tekst_veld = QLineEdit()
layout.addWidget(tekst_veld)

window.setLayout(layout)
window.show()
app.exec_()


#test in atom
