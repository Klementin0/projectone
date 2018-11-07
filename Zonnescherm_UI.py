import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):

    def setupUi(self, MainWindow):

        #main venster
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(500, 100)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #button minimale stand
        self.minimale_stand = QtWidgets.QPushButton(self.centralwidget)
        self.minimale_stand.setGeometry(QtCore.QRect(250, 10, 100, 30))
        self.minimale_stand.setObjectName("minimale_stand")
        self.minimale_stand.clicked.connect(self.minimale_stand_action)

        #button maximale stand
        self.maximale_stand = QtWidgets.QPushButton(self.centralwidget)
        self.maximale_stand.setGeometry(QtCore.QRect(350, 10, 100, 30))
        self.maximale_stand.setObjectName("maximale_stand")
        self.maximale_stand.clicked.connect(self.maximale_stand_action)

        #button inrollen
        self.inrollen = QtWidgets.QPushButton(self.centralwidget)
        self.inrollen.setGeometry(QtCore.QRect(250, 50, 100, 31))
        self.inrollen.setObjectName("inrollen")
        self.inrollen.clicked.connect(self.inrollen_action)

        #button uitrollen
        self.uitrollen = QtWidgets.QPushButton(self.centralwidget)
        self.uitrollen.setGeometry(QtCore.QRect(350, 50, 100, 30))
        self.uitrollen.setObjectName("uitrollen")
        self.uitrollen.clicked.connect(self.uitrollen_action)

        #button meer informatie
        self.meer_informatie = QtWidgets.QPushButton(self.centralwidget)
        self.meer_informatie.setGeometry(QtCore.QRect(20, 50, 100, 30))
        self.meer_informatie.setObjectName("meer_informatie")
        self.meer_informatie.clicked.connect(self.meer_informatie_action)


        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionVerversen = QtWidgets.QAction(MainWindow)
        self.actionVerversen.setObjectName("actionVerversen")
        self.vertalen(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)



    #actie wanneer de knop minimale_stand_action wordt ingedrukt
    def minimale_stand_action(self):
        print("Minimale afstand")

    # actie wanneer de knop maximale_stand_action wordt ingedrukt
    def maximale_stand_action(self):
        print("Maximale stand")

    # actie wanneer de knop inrollen_action wordt ingedrukt
    def inrollen_action(self):
        print("Inrollen")

    # actie wanneer de knop uitrollen_action wordt ingedrukt
    def uitrollen_action(self):
        print("Uitrullen")

    # actie wanneer de knop meer_informatie_action wordt ingedrukt
    def meer_informatie_action(self):
        print("Meer informatie")

    #namen definiëren
    def vertalen(self, MainWindow):
        _vertalen = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_vertalen("MainWindow", "MainWindow"))
        self.minimale_stand.setText(_vertalen("MainWindow", "Minimale stand"))
        self.maximale_stand.setText(_vertalen("MainWindow", "Maximale stand"))
        self.inrollen.setText(_vertalen("MainWindow", "Inrollen"))
        self.uitrollen.setText(_vertalen("MainWindow", "Uitrollen"))
        self.meer_informatie.setText(_vertalen("MainWindow", "Meer informatie"))
        self.actionVerversen.setText(_vertalen("MainWindow", "Verversen"))




app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
sys.exit(app.exec_())

