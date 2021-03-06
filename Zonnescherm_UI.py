import serial_se_re
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import meer_informatie

#Maak nieuw Zonnescherm
serialPort = serial_se_re.SerialPort()
increment = 5

def InsertText():
    tekst_veld.insert("kek")

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        #main venster
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 180)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")



        self.minimale_stand_kleiner = QtWidgets.QPushButton(self.centralwidget)
        self.minimale_stand_kleiner.setGeometry(QtCore.QRect(250, 30, 20, 30))
        self.minimale_stand_kleiner.setObjectName("minimale_stand_kleiner")
        self.minimale_stand_kleiner.clicked.connect(self.minimale_stand_action_min)

        #weergave minimale stand
        self.minimale_stand_stand_weergave = QtWidgets.QLabel(self.centralwidget)
        self.minimale_stand_stand_weergave.setGeometry(QtCore.QRect(265, 0, 80, 40))
        self.minimale_stand_stand_weergave.setObjectName("minimale_stand_stand_weergave")

        #weergave minimale stand
        self.minimale_stand = QtWidgets.QLabel(self.centralwidget)
        self.minimale_stand.setGeometry(QtCore.QRect(290, 30, 60, 30))
        self.minimale_stand.setObjectName("minimale_stand")


        self.minimale_stand_groter = QtWidgets.QPushButton(self.centralwidget)
        self.minimale_stand_groter.setGeometry(QtCore.QRect(330, 30, 20, 30))
        self.minimale_stand_groter.setObjectName("minimale_stand_groter")
        self.minimale_stand_groter.clicked.connect(self.minimale_stand_action_plus)



        #button maximale stand
        self.maximale_stand_kleiner = QtWidgets.QPushButton(self.centralwidget)
        self.maximale_stand_kleiner.setGeometry(QtCore.QRect(350, 30, 20, 30))
        self.maximale_stand_kleiner.setObjectName("maximale_stand_kleiner")
        self.maximale_stand_kleiner.clicked.connect(self.maximale_stand_action_min)

        #weergave minimale stand
        self.maximale_stand_stand_weergave = QtWidgets.QLabel(self.centralwidget)
        self.maximale_stand_stand_weergave.setGeometry(QtCore.QRect(360, 0, 80, 40))
        self.maximale_stand_stand_weergave.setObjectName("minimale_stand_stand_weergave")

        self.maximale_stand = QtWidgets.QLabel(self.centralwidget)
        self.maximale_stand.setGeometry(QtCore.QRect(390, 30, 60, 30))
        self.maximale_stand.setObjectName("maximale_stand")

        self.maximale_stand_groter = QtWidgets.QPushButton(self.centralwidget)
        self.maximale_stand_groter.setGeometry(QtCore.QRect(430, 30, 20, 30))
        self.maximale_stand_groter.setObjectName("maximale_stand_groter")
        self.maximale_stand_groter.clicked.connect(self.maximale_stand_action_plus)


        #button inrollen
        self.inrollen = QtWidgets.QPushButton(self.centralwidget)
        self.inrollen.setGeometry(QtCore.QRect(250, 70, 100, 30))
        self.inrollen.setObjectName("inrollen")
        self.inrollen.clicked.connect(self.inrollen_action)

        #button uitrollen
        self.uitrollen = QtWidgets.QPushButton(self.centralwidget)
        self.uitrollen.setGeometry(QtCore.QRect(350, 70, 100, 30))
        self.uitrollen.setObjectName("uitrollen")
        self.uitrollen.clicked.connect(self.uitrollen_action)

        #button meer informatie
        self.meer_informatie = QtWidgets.QPushButton(self.centralwidget)
        self.meer_informatie.setGeometry(QtCore.QRect(20, 70, 100, 30))
        self.meer_informatie.setObjectName("meer_informatie")
        self.meer_informatie.clicked.connect(self.meer_informatie_action)

        #button verbinden
        self.verbinden = QtWidgets.QPushButton(self.centralwidget)
        self.verbinden.setGeometry(QtCore.QRect(350, 120, 100, 30))
        self.verbinden.setObjectName("verzenden")
        self.verbinden.clicked.connect(self.verbinden_action)

        #verbinding verbreken
        self.verbinding_verbreken = QtWidgets.QPushButton(self.centralwidget)
        self.verbinding_verbreken.setGeometry(QtCore.QRect(200, 120, 150, 30))
        self.verbinding_verbreken.setObjectName("verbinding verbreken")
        self.verbinding_verbreken.clicked.connect(self.verbinding_verbreken_action)

        #Automatisch button
        self.automatisch_manual = QtWidgets.QPushButton(self.centralwidget)
        self.automatisch_manual.setGeometry(QtCore.QRect(135, 30, 100, 30))
        self.automatisch_manual.setObjectName("automatisch_manual")
        self.automatisch_manual.clicked.connect(self.automatisch_manual_action)

        #status updaten
        self.status_update = QtWidgets.QPushButton(self.centralwidget)
        self.status_update.setGeometry(QtCore.QRect(20, 30, 100, 30))
        self.status_update.setObjectName("status update")
        self.status_update.clicked.connect(self.status_update_action)

        #status label
        self.status_label = QtWidgets.QLabel(self.centralwidget)
        self.status_label.setGeometry(QtCore.QRect(30, 120, 100, 30))
        self.status_label.setObjectName("status_label")


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionVerversen = QtWidgets.QAction(MainWindow)
        self.actionVerversen.setObjectName("actionVerversen")
        self.vertalen(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    #minimale_stand -5 maken.
    def minimale_stand_action_min(self):

        if self.stand_min > 9:
            self.stand_min = self.stand_min - 5
            serialPort.Stuur(5)

        minvalue = serialPort.Return_min()
        if minvalue > 9:
            minvalue = minvalue - 5
            serialPort.Update_min(minvalue)
            minvalue = str(minvalue)
            serialPort.Stuur("5")
            self.minimale_stand.setText(minvalue)
        else:
            print("Minimale stand is nu 5, deze kan niet kleiner worden gemaakt.")

    #minimale_stand +5 maken.
    def minimale_stand_action_plus(self):
        minvalue = serialPort.Return_min()
        if minvalue < 36:
            minvalue = minvalue + 5
            serialPort.Update_min(minvalue)
            minvalue = str(minvalue)
            serialPort.Stuur("4")
            self.minimale_stand.setText(minvalue)
        else:
            print("Minimale stand is nu 40, deze kan niet groter worden gemaakt.")

    #maximale_stand -5 maken.
    def maximale_stand_action_min(self):
        maxvalue = serialPort.Return_max()
        if maxvalue > 139:
            maxvalue = maxvalue - 5
            serialPort.Update_max(maxvalue)
            maxvalue = str(maxvalue)
            serialPort.Stuur("3")
            self.maximale_stand.setText(maxvalue)
        else:
            print("Maximale stand van 140 is bereikt, kan niet kleiner worden gemaakt.")

    #maximale_stand +5 maken.
    def maximale_stand_action_plus(self):
        maxvalue = serialPort.Return_max()
        if maxvalue < 156:
            maxvalue = maxvalue + 5
            serialPort.Update_max(maxvalue)
            maxvalue = str(maxvalue)
            serialPort.Stuur("2")
            self.maximale_stand.setText(maxvalue)
        else:
            print("Maximale stand van 160 is bereikt, kan niet groter worden gemaakt.")

    # actie wanneer de knop inrollen_action wordt ingedrukt
    def inrollen_action(self):
        serialPort.Stuur("6")

    # actie wanneer de knop uitrollen_action wordt ingedrukt
    def uitrollen_action(self):
        serialPort.Stuur("7")

    # actie wanneer de knop meer_informatie_action wordt ingedrukt
    def meer_informatie_action(self):
        temp = serialPort.Return_temp()
        licht = serialPort.Return_licht()
        afstand = serialPort.Return_afstand()
        if not afstand:
            print("Opflikkeren, ie krijgt geen grafiek")
        else:
            meer_informatie.maak_grafiek(temp, licht, afstand)

    # actie wanneer de knop verbinden_action wordt ingedrukt
    def verbinden_action(self):
        serialPort.Open("COM6", 19200)
        serialPort.Lees()
        serialPort.Stuur("8")

    # actie wanneer de knop verbinding_verbreken_action wordt ingedrukt
    def verbinding_verbreken_action(self):
        #print("verbinding verbreken")
        #serialPort.Stuur("Basic Send")
        serialPort.Sluiten()

    def automatisch_manual_action(self):
        t = self.automatisch_manual.text()
        if (t == "Manual"):
            self.automatisch_manual.setText("Automatisch")
        else:
            self.automatisch_manual.setText("Manual")
        serialPort.Stuur("1")

    # status updaten
    def status_update_action(self):
        _vertalen = QtCore.QCoreApplication.translate
        temp = serialPort.Return_temp()

        if not temp:
            lasttemp = "-"
        else:
            lasttemp = temp[-1:]
            lasttemp = lasttemp[0]

        self.status_label.setText(_vertalen("MainWindow", " "+str(lasttemp)+" ℃ / Uitgerold"))

    def temp_return():
        temp = serialPort.Return_temp()
        return temp

    #namen definiëren
    def vertalen(self, MainWindow):
        _vertalen = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_vertalen("MainWindow", "MainWindow"))
        self.status_update.setText(_vertalen("MainWindow", "Status updaten"))

        self.minimale_stand_kleiner.setText(_vertalen("MainWindow", "<"))
        self.minimale_stand_stand_weergave.setText(_vertalen("MainWindow", "Minimale stand:"))
        self.minimale_stand.setText(_vertalen("MainWindow", "20"))
        self.minimale_stand_groter.setText(_vertalen("MainWindow", ">"))

        self.maximale_stand_kleiner.setText(_vertalen("MainWindow", "<"))
        self.maximale_stand_stand_weergave.setText(_vertalen("MainWindow", "Maximale stand:"))
        self.maximale_stand.setText(_vertalen("MainWindow", "140"))
        self.maximale_stand_groter.setText(_vertalen("MainWindow", ">"))


        self.inrollen.setText(_vertalen("MainWindow", "Inrollen"))
        self.uitrollen.setText(_vertalen("MainWindow", "Uitrollen"))
        self.meer_informatie.setText(_vertalen("MainWindow", "Meer informatie"))
        self.automatisch_manual.setText(_vertalen("MainWindow", "Manual"))
        self.actionVerversen.setText(_vertalen("MainWindow", "Verversen"))
        self.verbinden.setText(_vertalen("MainWindow", "Verbinden"))
        self.verbinding_verbreken.setText(_vertalen("MainWindow", "Verbinding verbreken"))
        self.status_update.setText(_vertalen("MainWindow", "Status updaten"))





app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_(), serialPort.Sluiten())
