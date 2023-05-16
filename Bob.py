# coding=utf8
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor
class Bob:
    N=0
    p=0
    q=0
    def __init__(self,N,p,q):
        self.N=N
        self.p=p
        self.q=q
        self.t=[]
        self.estore=[]
    def returnSecret(self):
        return self.f,self.Fq,self.hx
    def ReceiveOtherF_Fp(self,F1,Fq1,hx1):
        self.F1=F1
        self.Fq1=Fq1
        self.hx1=hx1
    def encrypt2(self,message):
        if(len(message)<self.N):
            for i in range(self.N-len(message)):
                message.append(0)
        temp2=self.Multiply2(self.r,self.hx1,self.N)#r*h
        self.e=self.add(temp2,message)#r*h+m
        self.e=self.MultiplyModm(self.e,self.p)
        self.estore.append(self.e)
        return self.e
    #解密过程
    def decrypt2(self,e=[]):
        c=[]
        if(len(e)==0):
            pass
        for i in e:
            temp=self.Multiply2(self.F1,i,self.N)#f*e
            temp=self.MultiplyModm(temp,self.p)
            temp2=self.center_lift(temp,self.p)#temp2=a
            b=[]
            for i in temp2:
                b.append(i%self.q)
            #b=a%q
            temp3=self.Multiply2(self.Fq1,b,self.N)
            c.append(self.MultiplyModm(temp3,self.q))
        return c
    #N---NRTU的标准参数,N1,1的个数，N2,-1的个数
    def Rand_Poly(self,N,N1,N2):
        x=[]#将会返回的多项式
        temp=[]#暂时使用
        for i in range(N1):
            temp.append(1)
        for i in range(N2):
            temp.append(-1)
        for i in range(N-N1-N2):
            temp.append(0)
        for i in range(N):
            up= len(temp)-1
            x.append(temp.pop(random.randint(0,up)))
        return x
    def MultiplyModm(self,a,m):
        for i in range(len(a)):
            a[i]=a[i]%m
        return a
    #a,b----参与运算的多项式，N————NTRU的标准参数，m---模(p或q)
    def Multiply2(self,a,b,N):
        c=[]
        for i in range(N):
           c.append(0)
        for k in range(N):
            for i in range(N):
                c[(k+i)%N]+=a[k]*b[i]
        return c
    def Multiply(self,a,b,N,m):
        if(m==0):
            if (type(a) == int):
                c = []
                for i in b:
                    c.append(i * a)
                return c
            c = []
            for i in range(N):
                c.append(0)
            for i in range(N - 1, -1, -1):
                K = 0
                for j in range(0, i + 1, 1):
                    c[i] += a[j] * b[i - j]
                    c[i] = c[i]
                for j in range(1, N - i, 1):
                    K += a[i + j] * b[N - j]
                    K = K
                c[i] += K
                c[i] = c[i]
            return c
        if(type(a)==int):
            c=[]
            for i in b:
                c.append((i*a)%m)
            return c
        c=[]
        for i in range(N):
            c.append(0)
        for i in range(N-1,-1,-1):
            K=0
            for j in range(0,i+1,1):
                c[i]+=a[j]*b[i-j]
                c[i]=(c[i])%m
            for j in range(1,N-i,1):
                K+=a[i+j]*b[N-j]
                K=K%m
            c[i]+=K
            c[i]=c[i]%m
        return c
    #多项式带入
    def PolyValue(self,f,p,m):
        value=0
        for i in range(len(f)):
            value+=(p**i*f[i])%m
            value=value%m
        return value
    #多项式求次数
    def deg(self,f):
        for i in range(len(f)-1,-1,-1):
            if(f[i]!=0):
                return i
        return 0
    #整数求逆,x为输入，使用扩展欧几里得算法
    def iv(self,a,b):
        x,y,gcd=self.ext_gcd(a,b)
        if(gcd!=1):
            return -1
        elif(x>0):
            return x
        else:
            return b+x
    def ext_gcd(self,a, b):  # 扩展欧几里得算法
        if b == 0:
            return 1, 0, a
        else:
            x, y, gcd = self.ext_gcd(b, a % b)  # 递归直至余数等于0(需多递归一层用来判断)
            x, y = y, (x - (a // b) * y)  # 辗转相除法反向推导每层a、b的因子使得gcd(a,b)=ax+by成立
            return x, y, gcd
    #center-lift,让所有的系数都在[-p/2---p/2]之间
    def center_lift(self,a,p):
        for i in range(len(a)):
            if(a[i]>int(p/2)):
                a[i]-=p
            elif(a[i]<int(-p/2)):
                a[i]+=p
        return a
    #多项式相加
    def add(self,a,b):
        c=[]
        for i in range(self.N):
           c.append((a[i]+b[i])%self.p)
        return c

    #生成密钥
    #生成密钥需要的线程函数
    def Threading(self):
        x1 = random.randint(1, int(self.N / 2))
        f = self.Rand_Poly(self.N, x1, x1 - 1)
        Fp2 = self.InversePoly(f, self.N, self.q)
        Fp1 = self.InversePoly(f, self.N, self.p)
        if (Fp1 != -1 and Fp2 != -1 and self.Multiply(Fp1, f, self.N, self.p)[0] == 1 and
                self.Multiply(Fp2, f, self.N, self.q)[0] == 1):
                    return [f,Fp1,Fp2]
        else:
            return 0
    #生成线程的回调函数
    def ThreadCallBack(self,future):
        if(future.result()!=0):
            print(future.result())
            self.t.append(future.result())

    def key_gen_Weak(self):
        Fp=-1
        index=1
        while(Fp==-1):
            # index+=1
            # random.seed(time.time()+index)
            self.g=self.Rand_Poly(self.N,12,11)
            self.f=self.Rand_Poly(self.N,15,14)
            Fp2=self.InversePoly(self.f,self.N,self.q)
            Fp1=self.InversePoly(self.f,self.N,self.p)
            if(Fp1!=-1 and Fp2!=-1 and self.Multiply(Fp1,self.f,self.N,self.p)[0]==1 and self.Multiply(Fp2,self.f,self.N,self.q)[0]==1):
                Fp=0
        self.Fp=Fp1
        self.Fq=Fp2
        temp=[]#存储q*Fp
        for i in range(len(self.Fp)):
            temp.append(self.Fp[i]*self.q)
        #q*Fp*g
        self.hx=self.Multiply2(temp,self.g,self.N)
        self.hx=self.MultiplyModm(self.hx,self.p)


    def key_gen_Thread(self):
        Fp=-1
        x1 = random.randint(1, int(self.N / 2))
        self.g = self.Rand_Poly(self.N, x1, x1 - 1)
        x1 = random.randint(1, int(self.N / 2))
        x2 = random.randint(1, self.N - x1)
        self.r = self.Rand_Poly(self.N, x1, x2)
        while(len(self.t)==0):
            for i in range(12):
                pool=ThreadPoolExecutor(max_workers=12)
                x=pool.submit(self.Threading)
                x.add_done_callback(self.ThreadCallBack)
        pool.shutdown()
        self.f=self.t[0][0]
        self.Fp=self.t[0][1]
        self.Fq=self.t[0][2]
        temp=[]#存储q*Fp
        for i in range(len(self.Fp)):
            temp.append(self.Fp[i]*self.q)
        #q*Fp*g
        self.hx=self.Multiply2(temp,self.g,self.N)
        self.hx=self.MultiplyModm(self.hx,self.p)
    #生成f和Fp,并且计算出hx
    def key_gen(self):
        Fp = -1
        x1 = random.randint(1, int(self.N / 2))
        self.g = self.Rand_Poly(self.N, x1, x1)
        x1 = random.randint(1, int(self.N / 2))
        # x2 = random.randint(1, self.N - x1)
        self.r = self.Rand_Poly(self.N, x1, x1)
        self.estore=[]
        while (Fp == -1):
            # index+=1
            # random.seed(time.time()+index)
            x1 = random.randint(1, int(self.N / 2))
            self.f = self.Rand_Poly(self.N, x1, x1 - 1)
            Fp2 = self.InversePoly(self.f, self.N, self.q)
            Fp1 = self.InversePoly(self.f, self.N, self.p)
            if (Fp1 != -1 and Fp2 != -1 and self.Multiply(Fp1, self.f, self.N, self.p)[0] == 1 and
                    self.Multiply(Fp2, self.f, self.N, self.q)[0] == 1):
                Fp = 0
        self.Fp = Fp1
        self.Fq = Fp2
        temp = []  # 存储q*Fp
        for i in range(len(self.Fp)):
            temp.append(self.Fp[i] * self.q)
        # q*Fp*g
        self.hx = self.Multiply2(temp, self.g, self.N)
        self.hx = self.MultiplyModm(self.hx, self.p)
    def encrypt_Weak(self,message):
        if(len(message)<self.N):
            for i in range(self.N-len(message)):
                message.append(0)
        x1 = random.randint(1, int(self.N / 2))
        x2 = random.randint(1, self.N - x1)
        self.r=self.Rand_Poly(self.N,5,4)
        temp2=self.Multiply2(self.r,self.hx,self.N)#r*h
        self.e=self.add(temp2,message)#r*h+m
        self.e=self.MultiplyModm(self.e,self.p)
        return self.e
    #加密过程
    def encrypt(self,message):
        if(len(message)<self.N):
            for i in range(self.N-len(message)):
                message.append(0)
        temp2=self.Multiply2(self.r,self.hx,self.N)#r*h
        self.e=self.add(temp2,message)#r*h+m
        self.e=self.MultiplyModm(self.e,self.p)
        self.estore.append(self.e)
        return self.estore
    def TranMessageBit(self,m):
        self.MessageBit = []
        for index1 in m:
            value = ord(index1)
            temp = []
            for index2 in range(32):
                if (value % 2 == 1):
                    value = value - 1
                    value = value / 2
                    temp.append(1)
                else:
                    value = value / 2
                    temp.append(0)
            self.MessageBit.append(temp)
        return self.MessageBit
    #解密过程
    def decrypt(self,e=[]):
        c=[]
        if(len(e)==0):
            pass
        else:
            self.estore=e
        for i in self.estore:
            temp=self.Multiply2(self.f,i,self.N)#f*e
            temp=self.MultiplyModm(temp,self.p)
            temp2=self.center_lift(temp,self.p)#temp2=a
            b=[]
            for i in temp2:
                b.append(i%self.q)
            #b=a%q
            temp3=self.Multiply2(self.Fq,b,self.N)
            c.append(self.MultiplyModm(temp3,self.q))
        return c
    #输出多项式
    def show_f(self,f):
        for i in range(len(f)):
            if(i==0):
                print(f"{f[i]}+",end="")
            elif(i==len(f)-1):
                print(f"{f[i]}x^{i}")
            else:
                print(f"{f[i]}x^{i}+",end="")

    #输出公钥
    def ReturnHx(self):
        return self.hx
    def EncryptMessage(self,m):
        self.MessageBit=[]
        for index1 in m:
            value=ord(index1)
            temp=[]
            for index2 in range(32):
                if(value%2==1):
                    value=value-1
                    value=value/2
                    temp.append(1)
                else:
                    value=value/2
                    temp.append(0)
            self.MessageBit.append(temp)
        for i in self.MessageBit:
            self.encrypt(i)
        self.MessageBit=[]
    def returnE(self):
        return self.estore
    def DecryptMessage(self,e):
        if(len(e)==0):
            pass
        else:
            self.estore=e
        #print("开始解密")
        result=""
        self.MessageBit=self.decrypt()
        for i in self.MessageBit:
            temp=0
            for index in range(32):
                if(i[index]==1):
                    temp+=2**index
            #print(chr(temp),end="")
            result+=chr(temp)
        return result
    #多项式求逆
    def InversePoly(self,a,N,p):
        k=0
        #定义b(x)=1,c(x)=0,f(x)
        b=[1]
        c=[]
        f=[]
        g=[-1]
        for i in range(N):
            if(i==0):
                c.append(0)
                f.append(a[i])
            elif(i==N-1):
                c.append(0)
                g.append(0)
                f.append(a[i])
                b.append(0)
            else:
                c.append(0)
                g.append(0)
                f.append(a[i])
                b.append(0)
        g.append(1)
        index=0
        index2=0
        while(1):
            index+=1
            if(index>10e2):
                #print("Error!!!")
                return -1
            while(f[0]==0 and self.deg(f)!=0):
                index2 += 1
                #f(x)=f(x)/x
                if (index2 > 10e2):
                    #print("Error!!!")
                    return -1
                for i in range(1,len(f),1):
                    f[i-1]=f[i]

                #多项式x
                # poly_x=[]
                # for i in range(N):
                #     if(i==1):
                #         poly_x.append(1)
                #     else:
                #         poly_x.append(0)
                # c=self.Multiply(c,poly_x,N,p)
                for i in range(N-1,0,-1):
                    c[i]=c[i-1]
                c[0]=0
                f[len(f)- 1] = 0;
                k=k+1
            if(self.deg(f)==0):
                #b(x)=b(x)*f0逆
                for index in range(len(b)):
                    b[index]=(b[index]*f[0])%p
                b1=[]
                for i in range(len(b)):
                    if(b[i]<0):
                        b1.append(b[i]+p)
                    else:
                        b1.append(b[i])
                k1=N-k
                if(k1<0):
                    k1=N+k1
                    for i in range(N):
                        b[(k1+i)%N]=b1[i]
                else:
                    for i in range(N):
                        b[(k1+i)%N] = b1[i]
                # temp=self.iv(a[0],p)
                # for i in range(len(b)):
                #     b[i]=b[i]*temp
                return b
            if(self.deg(f)<self.deg(g)):
                t=[]
                t=f
                f=g
                g=t
                t=b
                b=c
                c=t
            if(g[0]<0):
                t=0
                t=g[0]
                t=(t+p)%p
                INX=self.iv(t,p)
                u=(INX*f[0])%p
            else:
                INX=self.iv(g[0],p)
                u=(INX*f[0])%p
            for i in range(N):
                f[i] = (f[i] - u * g[i])%p
                b[i] = (b[i] - u * c[i])%p








