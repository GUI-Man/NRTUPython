
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
    temp=[]
    while(1):
        for index in range(32):
            temp.append(random.randint(0, 1))
        Realbob.encrypt(temp)
        x=Realbob.decrypt()
        if(x[0]==temp):
            break
        else:
            Realbob.key_gen()
    Public_key=Realbob.ReturnHx()
    RealAlice.Receive(Public_key)
    temp=[]
    for index in range(32):
        temp.append(random.randint(0, 1))
    RealAlice.encrypt(temp)
    e=RealAlice.returnE()
    temp2=Realbob.decrypt(e)
    print(temp)
    print(temp2)
    RealAlice.estore=[]
    RealAlice.EncryptMessage("哈布斯堡将会统治世界")
    e=RealAlice.returnE()
    Realbob.DecryptMessage(e=e)