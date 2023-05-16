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
        self.ui.FirstStep.clicked.connect(self.FirstStep)
        self.ui.SecondStep.clicked.connect(self.SecondStep)
        self.ui.AVerify1.clicked.connect(self.AFirstStep)
        self.ui.AVerify2.clicked.connect(self.ASecondStep)
        self.ui.AVerify3.clicked.connect(self.AThirdStep)
        self.ui.AVerify1_2.clicked.connect(self.BFirstStep)
        self.ui.AVerify2_2.clicked.connect(self.BSecondStep)
        self.ui.AVerify3_2.clicked.connect(self.BThirdStep)

    def FirstStep(self):
        self.ui.textEdit.setText("第一步，A和B彼此互相生成公私钥对，具体参数参考隔壁状态框")
        self.Realbob = Bob.Bob(32, 63, 2)  # 设置N,p,q
        self.RealAlice = Alice.Alice(32, 63, 2)  # 设置N,p,q
        self.Realbob.key_gen()
        self.RealAlice.key_gen()
        Bf, Bfp, Bhx = self.Realbob.returnSecret()
        Af, Afp, Ahx = self.RealAlice.returnSecret()
        message=""
        for i in Ahx:
            message=message+str(i)+","
        self.ui.ApublicKey1.setText(message)
        message=""
        for i in Af:
            message=message+str(i)+","
        self.ui.Af1.setText(message)

        message=""
        for i in Afp:
            message=message+str(i)+","
        self.ui.AFp1.setText(message)

        message=""
        for i in Bhx:
            message=message+str(i)+","
        self.ui.B2.setText(message)

        message=""
        for i in Bf:
            message=message+str(i)+","
        self.ui.BF2.setText(message)

        message=""
        for i in Bfp:
            message=message+str(i)+","
        self.ui.BFP2.setText(message)
    def SecondStep(self):
        self.ui.textEdit.setText("A和B会互相交换公私钥对,此时A和B已经拥有他们彼此的公私钥对，对于他们来说，他们是完全透明的，这一步的私钥交换必须是绝对安全的")
        Bf, Bfp, Bhx = self.Realbob.returnSecret()
        Af, Afp, Ahx = self.RealAlice.returnSecret()
        self.RealAlice.ReceiveOtherF_Fp(Bf, Bfp, Bhx)
        self.Realbob.ReceiveOtherF_Fp(Af, Afp, Ahx)

        message=""
        for i in Ahx:
            message=message+str(i)+","
        self.ui.AP2.setText(message)
        message=""
        for i in Af:
            message=message+str(i)+","
        self.ui.Af2.setText(message)

        message=""
        for i in Afp:
            message=message+str(i)+","
        self.ui.AFp2.setText(message)

        message=""
        for i in Bhx:
            message=message+str(i)+","
        self.ui.Bp1.setText(message)

        message=""
        for i in Bf:
            message=message+str(i)+","
        self.ui.BF1.setText(message)

        message=""
        for i in Bfp:
            message=message+str(i)+","
        self.ui.BFp1.setText(message)
    def AFirstStep(self):
        self.ui.textEdit.setText("现在进入验证环节，此时A并不知道B的身份，A生成一串随机验证码并且发送给B,随机生成的验证码见“A随机生成的验证码：”处")
        tempB = []
        message=""
        # Bob生成自己的验证码
        for index in range(32):
            x=random.randint(0,1)
            tempB.append(x)
            message+=str(x)
        self.ui.lineEdit.setText(message)
        self.Realbob.encrypt(tempB)  # A加密自己的密文
    def ASecondStep(self):
        self.ui.textEdit.setText("A对自己生成的随机验证码进行加密，并且将其发送给B")
        tempB=self.Realbob.returnE()
        message=""
        for index in tempB:
            message+=str(index)
        self.ui.lineEdit_2.setText(message)
    def AThirdStep(self):
        self.ui.textEdit.setText("B将其验证码进行解密，将验证码返回给B，A可以通过比较B能否解密出验证码来判断验证是否正确")
        temp2 = self.RealAlice.decrypt2(self.Realbob.returnE())  # Alice用Bob的私钥解密出密文验证码
        message=""
        for index in temp2:
            for i in index:
                message+=str(i)
        self.ui.lineEdit_3.setText(message)
    def BFirstStep(self):
        self.ui.textEdit.setText("现在进入验证环节，此时B并不知道A的身份，B生成一串随机验证码并且发送给A,随机生成的验证码见“B随机生成的验证码：”处")
        tempB = []
        message=""
        # Bob生成自己的验证码
        for index in range(32):
            x=random.randint(0,1)
            tempB.append(x)
            message+=str(x)
        self.ui.lineEdit_5.setText(message)
        self.RealAlice.encrypt(tempB)  # A加密自己的密文
    def BSecondStep(self):
        self.ui.textEdit.setText("B对自己生成的随机验证码进行加密，并且将其发送给A")
        tempB=self.RealAlice.returnE()
        message=""
        for index in tempB:
            message+=str(index)
        self.ui.lineEdit_6.setText(message)
    def BThirdStep(self):
        self.ui.textEdit.setText("A将其验证码进行解密，将验证码返回给B，B可以通过比较A能否解密出验证码来判断验证是否正确")
        temp2 = self.Realbob.decrypt2(self.RealAlice.returnE())  # Alice用Bob的私钥解密出密文验证码
        message=""
        for index in temp2:
            for i in index:
                message+=str(i)
        self.ui.lineEdit_4.setText(message)
if __name__ == '__main__':
    app=QApplication([])
    window=MyWindow()
    window.show()
    app.exec()
