# coding=utf8
import random
import time
from concurrent.futures import ThreadPoolExecutor
import Bob
import Alice
from PySide6.QtWidgets import QMainWindow,QPushButton,QLabel,QApplication
from 验证界面 import Ui_MainWindow
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.8)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind()
        temp = []
    def bind(self):
        self.ui.StartButton.clicked.connect(self.FirstStep)
        self.ui.BobMakeHx.clicked.connect(self.BobMakeHx)
        self.ui.SharePublicKey.clicked.connect(self.SharePublicKey)
        self.ui.AliceEncrypt.clicked.connect(self.CalcualteE)
        self.ui.DecryptMessage.clicked.connect(self.BobDecrypt)
    def Firststep(self):
        pass
    def SecondStep(self):
        pass

if __name__ == '__main__':
    app=QApplication([])
    window=MyWindow()
    window.show()
    app.exec()
