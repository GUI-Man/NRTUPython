# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import random
import time

import Bob

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')
    random.seed(time.time())
    Realbob=Bob.Bob(7,64,3)
    b=[2,1,3]
    c=[1,2,1]
    for i in range(500):
        #print(Realbob.Multiply2(b,c,3))
        Realbob.key_gen()
        Realbob.encrypt([1,1,4,5,1,4,0])
        print(Realbob.decrypt())
    #Realbob.Multiply([1, 0, 2, 0, 2, 0, 2],[0, 1, 0, 0, 0, 0, 0],7,3)
    # #print(Realbob.iv(1848,701))
    # print(Realbob.show_f(Realbob.g))
    # print(Realbob.show_f(Realbob.f))
    # print(Realbob.show_f(Realbob.InversePoly(Realbob.f,Realbob.N,Realbob.p)))
    # print(Realbob.show_f(Realbob.hx))
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
