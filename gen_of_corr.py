import numpy as np
import matplotlib.pylab as plt
import pandas as pd  # 引入pandas包
# data=pd.read_table('/content/qtdbSel100MLII.txt',sep='\t',header=None)     #读入txt文件，分隔符为\t
import random


def get_corr_row(N, lamida1 = -0.2, lamida2 = 0.5):


    i = 1
    data = []
    data1 = []
    data2 = []
    data3 = []
    data4 = []
    while i <= N:
        y = random.random()  # 0-1之间抽样随机数
        data1.append(y)
        y = random.random()  # 0-1之间抽样随机数
        data2.append(y)
        y = random.random()  # 0-1之间抽样随机数
        data3.append(y)
        y = random.random()  # 0-1之间抽样随机数
        data4.append(y)
        i = i+1
    data.append(data1)
    data.append(data2)
    data.append(data3)
    data.append(data4)
    
    
    a = (lamida1+lamida2+1)/(2)
    b = (lamida1+lamida2+1)/(2)-lamida2
    # a=0.75 #(lamida1+lamida2+1)/(2)
    # b=0.75 #(lamida1+lamida2+1)/(2)-lamida2
    # lamida1=a+b-1
    # lamida2=a-b
    # print(a, b)
    # if a>=1 or b>=1:
    #  print('cant do it！')
    s1 = []
    s2 = []
    x = []
    # print('B1=', lamida1, ', B2=', lamida2)
    # print('a=', a, ', b=', b)
    for i in range(N):
        if i == 0:
            if data[0][0] > 0.5:
                s1.append(0)

            else:
                s1.append(1)

            if float(data[1][0]) > 0.5:
                s2.append(0)

            else:
                s2.append(1)

        else:
            if s1[i-1] == 0 and s2[i-1] == 0 and data[0][i] > a:  # 1
                s1.append(0)
                s2.append(0)
                x.append(0)
                continue
            elif s1[i-1] == 0 and s2[i-1] == 0 and data[0][i] <= a:  # 2
                s1.append(1)
                s2.append(0)
                x.append(1)
                continue
            if s1[i-1] == 0 and s2[i-1] == 1 and data[1][i] <= b:  # 3
                s1.append(0)
                s2.append(0)
                x.append(0)
                continue
            elif s1[i-1] == 0 and s2[i-1] == 1 and data[1][i] > b:  # 4
                s1.append(1)
                s2.append(0)
                x.append(1)
                continue
            if s1[i-1] == 1 and s2[i-1] == 0 and data[2][i] > b:  # 5 >
                s1.append(0)
                s2.append(1)
                x.append(1)
                continue
            elif s1[i-1] == 1 and s2[i-1] == 0 and data[2][i] <= b:  # 6 <=
                s1.append(1)
                s2.append(1)
                x.append(0)
                continue
            if s1[i-1] == 1 and s2[i-1] == 1 and data[3][i] > a:  # 7 <=
                s1.append(0)
                s2.append(1)
                x.append(1)
                continue
            elif s1[i-1] == 1 and s2[i-1] == 1 and data[3][i] <= a:  # 8 >
                s1.append(1)
                s2.append(1)
                x.append(0)
                continue
    return x
# print(x)
# xx=np.array(x)
# def RF(lamida3,lamida4):
#   R=[]
#   #lamida3=((a+b-1)/2)+(((a+b-1)/2)**2+(a-b))** 0.5
#   #lamida4=((a+b-1)/2)-(((a+b-1)/2)**2+(a-b))** 0.5
#   print(lamida3,lamida4)
#   if lamida3 == lamida4 == 0:

#     for i in range(21):
#       if i==1:
#         R.append(1)
#       if i>1:
#         r=0
#         R.append(r)
#   else:
#     #A1=(lamida3*(1-lamida4**2))/((lamida3-lamida4)*(1+lamida3*lamida4))
#     #A2=(-lamida4*(1-lamida3**2))/((lamida3-lamida4)*(1+lamida3*lamida4))
#     #b1=lamida3+lamida4
#     b1=lamida3
#     #b2=-lamida3*lamida4
#     b2=lamida4
#     print(b1,b2)


#     for i in range(21):
#       if i==0:
#         R.append(1)
#       if i==1:
#         R1=b1/(1-b2)
#         R.append(R1)
#       if i>1:
#         r=b1*R[i-1]+b2*R[i-2]
#         R.append(r)
#     print(R)


#   return R
# def get_auto_corr(timeSeries,k):
#     '''
#     Descr:输入：时间序列timeSeries，滞后阶数k
#             输出：时间序列timeSeries的k阶自相关系数
#         l：序列timeSeries的长度
#         timeSeries1，timeSeries2:拆分序列1，拆分序列2
#         timeSeries_mean:序列timeSeries的均值
#         timeSeries_var:序列timeSeries的每一项减去均值的平方的和

#     '''
#     l = len(timeSeries)
#     #取出要计算的两个数组
#     timeSeries1 = timeSeries[0:l-k]
#     timeSeries2 = timeSeries[k:]
#     timeSeries_mean = timeSeries.mean()
#     timeSeries_var = np.array([i**2 for i in timeSeries-timeSeries_mean]).sum()
#     auto_corr = 0
#     for i in range(l-k):
#         temp = (timeSeries1[i]-timeSeries_mean)*(timeSeries2[i]-timeSeries_mean)/timeSeries_var
#         auto_corr = auto_corr + temp
#     return auto_corr
# def plot_auto_corr(timeSeries,k):
#     '''
#     Descr:需要计算自相关函数get_auto_corr(timeSeries,k)
#             输入时间序列timeSeries和想绘制的阶数k，k不能超过timeSeries的长度
#             输出：k阶自相关系数图，用于判断平稳性
#     '''
#     timeSeriestimeSeries = pd.DataFrame(range(k))
#     for i in range(1,k+1):
#         timeSeriestimeSeries.loc[i-1] =get_auto_corr(timeSeries,i)
#     plt.subplot(1, 2, 1)
#     plt.bar(range(1,len(timeSeriestimeSeries)+1),timeSeriestimeSeries[0])
#     plt.title("Автокорреляции x")
# plot_auto_corr(xx,20)
# R=RF(lamida1,lamida2)
# plt.subplot(1, 2, 2)
# plt.bar(range(1,len(R)+1),R)
# plt.title("Автокорреляции AP(2)")
