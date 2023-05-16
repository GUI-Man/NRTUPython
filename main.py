# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time
from concurrent.futures import ThreadPoolExecutor
import Bob
import Alice
import threading
def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.
    return name

def getresult(future):
    print(future.result())
# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # random.seed(time.time())
    #测试加解密字符串
    Realbob=Bob.Bob(32,63,2)
    RealAlice=Alice.Alice(32,63,2)
    Realbob.key_gen()
#     print("Finished")
#     for i in Realbob.hx:
#         RealAlice.hx.append(i)
#     RealAlice.EncryptMessage("""身躯凛凛，相貌堂堂，一双眼光射寒星，两弯眉浑如刷漆，胸脯横阔，有万夫难敌之威风，话语轩昂，吐千丈凌云之志气，心雄胆大，是撼天狮子下云端，骨健筋强，如摇地貔貅临座上，如同天上降魔主，真是人间太岁神
# """)
#     print("Finished")
#     for i in RealAlice.estore:
#         Realbob.estore.append(i)
#     Realbob.DecryptMessage()
    #测试正确率，加密成功后再解密
    # correct=0
    # Realbob.key_gen()
    # for i in range(500):
    #     temp=[]
    #     Realbob.estore=[]
    #     for index in range(32):
    #         temp.append(random.randint(0,1))
    #
    #     Realbob.encrypt(temp)
    #     x=Realbob.decrypt()
    #     if(x[0]==temp):
    #         correct+=1
    #         print("True")
    #
    #
    #     else:
    #         print("False")
    # print(correct,500-correct,correct/500)


    # #测试单纯公钥生成的时间效率
    # for i in range(8):
    #     correct=0
    #     start=time.time()
    #     for i in range(500):
    #         Realbob.key_gen()
    #     end=time.time()
    #     print(f"耗时：{end-start}")



    #测试加解密效率
    for i in range(8):
        Realbob.key_gen()
        start=time.time()
        for i in range(500):
            temp=[]
            Realbob.estore=[]
            for index in range(32):
                temp.append(random.randint(0,1))

            Realbob.encrypt(temp)
            x=Realbob.decrypt()
        end=time.time()
        print(f"耗时：{end - start}")




    #Realbob.Multiply([1, 0, 2, 0, 2, 0, 2],[0, 1, 0, 0, 0, 0, 0],7,3)
    # #print(Realbob.iv(1848,701))
    # print(Realbob.show_f(Realbob.g))
    # print(Realbob.show_f(Realbob.f))
    # print(Realbob.show_f(Realbob.InversePoly(Realbob.f,Realbob.N,Realbob.p)))
    # print(Realbob.show_f(Realbob.hx))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
