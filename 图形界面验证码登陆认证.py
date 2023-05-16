# coding=utf8

import random
import time
from concurrent.futures import ThreadPoolExecutor
import Bob
import Alice
import threading
def getresult(future):
    print(future.result())
if __name__ == '__main__':
    # random.seed(time.time())
    #测试加解密字符串
    Realbob=Bob.Bob(32,63,2)#设置N,p,q
    RealAlice=Alice.Alice(32,63,2)#设置N,p,q
    Realbob.key_gen()
    RealAlice.key_gen()
    Bf,Bfp,Bhx=Realbob.returnSecret()
    Af,Afp,Ahx=RealAlice.returnSecret()
    RealAlice.ReceiveOtherF_Fp(Bf,Bfp,Bhx)
    Realbob.ReceiveOtherF_Fp(Af,Afp,Ahx)
    tempB=[]
    #Bob生成自己的验证码
    for index in range(32):
        tempB.append(random.randint(0, 1))
    Realbob.encrypt(tempB)#A加密自己的密文

    temp2=RealAlice.decrypt2(Realbob.returnE())#Alice用Bob的私钥解密出密文验证码
    print(temp2)
    print(tempB)
    tempA=[]
    for index in range(32):
        tempA.append(random.randint(0, 1))
    #Alice生成自己的验证码
    RealAlice.encrypt(tempA)
    temp2=Realbob.decrypt2(RealAlice.returnE())
    print(temp2)
    print(tempA)