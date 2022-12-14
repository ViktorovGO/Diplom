import random
import matplotlib.pyplot as plt
from statistics import mean,median
import pandas as pd
def out_table(N, M, mx):
    k_l,k_r=map(int,input("Введите пределы изменения длины серий через запятую (левый,правый) - ").split(','))
    shag=int(input("Введите шаг изменения длины серий (целое число) - "))
    m=int(input("Введите по скольким значениям проводить усреднение - "))
    lst=[[],[],[],[]]
    
    for k in range(k_l,k_r+1,shag):
        res_list=[[],[],[],[]]
        for i in range(m):
            out_lst=razl(N, M, mx, k,0)
            res_list[0]=out_lst[0]
            res_list[1].append(out_lst[1])
            res_list[2].append(out_lst[2])
            res_list[3].append(out_lst[3])

        if res_list[1].count("-")<=(len(res_list[1])-res_list[1].count("-")):
            buf=[]
            for i in range(len(res_list[1])):
                if str(type(res_list[1][i]))!="<class 'str'>":
                    buf.append(res_list[1][i])
            res_list[1]=buf     
            res_list[1]=mean(res_list[1])
        else:
            res_list[1]="-"    

        res_list[2]=int(mean(res_list[2]))
        res_list[3]=int(mean(res_list[3]))
               
        lst[0].append(res_list[0])
        if (str(type(res_list[1]))=="<class 'float'>"):
            lst[1].append(round(res_list[1],2))
        else:
            lst[1].append(res_list[1])     
        lst[2].append(res_list[2])  
        lst[3].append(res_list[3])
        res_list.clear()

    df=pd.DataFrame(lst,columns=list(range(1,(len(lst[0])+1))),index=["Число серий","Тлт","Tзап","Время обнаружения ЛТ"])
    what=""
    while what not in ["Y","y","N","n"]:    
        what=input("Вывести таблицу в excel / Вывести таблицу в консоль 'y/n' ")
    if what=='y':
        df.to_excel("table.xlsx",sheet_name="sheet_1", header=False)
    elif what=='n':
        print(df)
  

def razl(N,M,mx,k,out=1):  
    '''
    Определение разладки сигнала
    '''
    def opr_razl(x,med,k,N):
        global Tlt
        k_p=0  # Число положительных серий
        k_n=0  # Число положительных серий
        Tlt=[] # Моменты времени ложных тревог
        Tr=[] # Моменты леальных тревог
        j=0
        for i in range(len(x)):    
            
            if x[i]>=med:
                k_p+=1
                k_n=0
            elif x[i]<med:
                k_p=0
                k_p+=1    
            
            if i==N:
                k_n=0
                k_p=0
            if k_p>=k:
                if i<N:
                    Tlt.append(i)
                elif i>=N:
                    Tr.append(i)
                k_p=0
            elif k_n>=k:
                if i<N:
                    Tlt.append(i)
                elif i>=N:
                    Tr.append(i)
                k_n=0
        return Tr
    
    
    
    x=[]
    x=[(random.random()-0.5)*1 for i in range(N)]
    med=median(x)
    x.extend([(random.random()+mx-0.5)*1 for i in range(N,M)])

    Tr=opr_razl(x, med, k, N)

    razn=[] # Список разностей между ложными тревогами

    # Определение среднего времени между ложными тревогами
    mean_razn = 0 # Среднее время между ложными тревогами
    if len(Tlt)!=0:
        if len(Tlt)==2:
            mean_razn=Tlt[1]-Tlt[0]    
        elif len(Tlt)==1:
            mean_razn="-"
        else:
            for i in range(len(Tlt)-1):      
                razn.append(Tlt[i+1]-Tlt[i])
            mean_razn=mean(razn)    
    else:
        if len(Tlt)==0:
            mean_razn="-"

    if out==1:  
        # Вывод результатов
        print(f'\n\nМедиана - {med}')
        if len(Tlt)!=0:
            print(f'Моменты времени ложных тревог - {Tlt}')
        else:
            print("Ложные тревоги отсутствуют")    
        print(f'Среднее время между ложными тревогами - {mean_razn}')
        print(f'Время запаздывания - {Tr[0]-N}')

        x_dot=[]      # Значения ряда в моменты реальных тревог
        for i in Tlt:
            x_dot.append(x[i])

        x_dot_real=[] # Значения ряда в моменты реальных тревог
        for i in Tr:
            x_dot_real.append(x[i])

        plt.plot(range(len(x)),x)
        plt.plot(Tlt,x_dot,'.',label="Ложная тревога",color="r",markersize=10)
        plt.plot(Tr,x_dot_real,".",label="Реальная тревога",markersize=10,color="0")
        plt.axhline(med, color='y',label='Медиана до разладки')
        plt.legend()    
        plt.show()
    else:
        out_lst=[k,mean_razn,Tr[0]-N,Tr[0]]
        return out_lst
st=""
while st not in ["Y","y","N","n"]:
    st=input("Определение разладки / Построить таблицу зависимостей - 'y/n' ")
N=int(input("Введите с какого отсчёта пойдёт разладка - "))
M=int(input("Введите общее число отсчётов - "))
mx=float(input("Введите медиану процесса начиная с момента заданной разладки(исходная=0) - "))

if st=='y':
    k=int(input("Введите длину серий успехов - "))
    razl(N,M,mx,k)

elif st=='n':
    
    out_table(N, M, mx)






