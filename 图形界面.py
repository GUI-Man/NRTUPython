# coding=utf8
import random
import time
from concurrent.futures import ThreadPoolExecutor
import Bob
import Alice
from PySide6.QtWidgets import QMainWindow,QPushButton,QLabel,QApplication
from 加解密界面 import Ui_MainWindow
class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowOpacity(0.8)
        self.ui=Ui_MainWindow()
        self.ui.setupUi(self)
        self.bind()
        self.Realbob = Bob.Bob(32, 63, 2)  # 设置N,p,q
        self.RealAlice = Alice.Alice(32, 63, 2)  # 设置N,p,q
        self.Realbob.key_gen()
        temp = []

        while (1):
            for index in range(32):
                temp.append(random.randint(0, 1))
            self.Realbob.encrypt(temp)
            x = self.Realbob.decrypt()
            if (x[0] == temp):
                break
            else:
                self.Realbob.key_gen()
    def bind(self):
        self.ui.StartButton.clicked.connect(self.FirstStep)
        self.ui.BobMakeHx.clicked.connect(self.BobMakeHx)
        self.ui.SharePublicKey.clicked.connect(self.SharePublicKey)
        self.ui.AliceEncrypt.clicked.connect(self.CalcualteE)
        self.ui.DecryptMessage.clicked.connect(self.BobDecrypt)
    def BobDecrypt(self):
        self.ui.FirstStepShow.setText("Bob接收Alice发的密文，依次解密出明文")
        E=self.RealAlice.returnE()
        mingwen=self.Realbob.DecryptMessage(e=E)
        self.ui.Decrypt_Message.setText(mingwen)
    def FirstStep(self):
        x=self.ui.Encrypt_content.text()
        messgebit=self.Realbob.TranMessageBit(x)
        self.ui.FirstStepShow.setText("预备工作：将字符串转换为二进制多项式，各项系数如下：")
        message=""
        for i in messgebit:
            for index in i:
                message=message+str(index)+","
            message=message+"\n"
        self.ui.FirstStepShow.append(message)
    def SharePublicKey(self):
        self.ui.FirstStepShow.setText("Bob向Alice分享自己的公钥")
        hx=self.Realbob.ReturnHx()
        self.RealAlice.Receive(hx)
        message=""
        for i in hx:
            message+=str(i)
        self.ui.Aliceh.setText(message)
    def CalcualteE(self):
        self.ui.FirstStepShow.setText("Alice进行加密操作")
        message=self.ui.Encrypt_content.text()
        self.RealAlice.EncryptMessage(message)
        returnE=self.RealAlice.returnE()
        text=""
        xi=0
        for i in returnE:
            xi+=1
            message=""
            for index in i:
                message+=str(i)
            text+=f"第{xi}个字符的密文:"+message+"\n"
        print(text)
        self.ui.EncryptMessage.setText(text)
    def BobReceive(self):
        print(self.Realbob.DecryptMessage(self.RealAlice.returnE()))
    def BobMakeHx(self):
        self.ui.FirstStepShow.setText("Bob开始生成公钥和私钥，Bob更新自己的公钥和私钥")
        self.Realbob.key_gen()
        Hx=self.Realbob.ReturnHx()
        f=self.Realbob.f
        fq=self.Realbob.Fq
        message=""
        for i in Hx:
            message+=str(i)
        self.ui.Bobh.setText(message)
        message=""
        for i in f:
            message+=str(i)
        self.ui.Bobf.setText(message)
        message=""
        for i in fq:
            message+=str(i)
        self.ui.BobFp.setText(message)
if __name__ == '__main__':
    app=QApplication([])
    window=MyWindow()
    window.show()
    app.exec()
# coding=utf8
