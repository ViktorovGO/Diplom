import random
import matplotlib.pyplot as plt
from statistics import mean,median
import pandas as pd
def out_table(N, M, mx):
    k_l,k_r=map(int,input("Введите пределы изменения длины серий через запятую (левый,правый) - ").split(','))
    shag=int(input("Введите шаг изменения длины серий (целое число) - "))
    lst=[[],[],[]]
    for k in range(k_l,k_r+1,shag):

        out_lst=razl(N, M, mx, k,0)   
        lst[0].append(out_lst[0])
        if (str(type(out_lst[1]))=="<class 'float'>"):
            lst[1].append(round(out_lst[1],2))
        else:
            lst[1].append(out_lst[1])     
        lst[2].append(out_lst[2])  
        

    df=pd.DataFrame(lst,columns=list(range(1,(len(lst[0])+1))),index=["K","Тлт","Tзап"])
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
        i=0
        for i in range(len(x)):    
            
            if x[i]>=med:
                k_p+=1
            elif x[i]<=med:
                k_p=0    
            if x[i]<=med:
                k_n+=1
            elif x[i]>=med:
                k_n=0 

            if k_p>=k:
                if i<N:
                    Tlt.append(i)
                elif i>=N:
                    break
                k_p=0
            elif k_n>=k:
                if i<N:
                    Tlt.append(i)
                elif i>=N:
                    break
                k_n=0
        return i
    
    
    random.seed(1)
    x=[]
    x=[random.gauss(0,1) for i in range(N)]
    med=median(x)
    x.extend([random.gauss(mx,1) for i in range(N,M)])

    lt=opr_razl(x, med, k, N)

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
        print(f'Время запаздывания - {lt-N}')
        
        plt.plot(range(len(x)),x)
        plt.axhline(med, color='y',label='Медиана до разладки')
        plt.legend()    
        plt.show()
    else:
        out_lst=[k,mean_razn,lt-N]
        return out_lst



st=input("Определение разладки / Построить таблицу зависимостей - 'y/n' ")
N=int(input("Введите момент времени разладки - "))
M=int(input("Введите общее число моментов времени - "))
mx=float(input("Введите мат ожидание разладки(исходное=0) - "))

if st=='y':
    k=int(input("Введите длину серий успехов - "))
    razl(N,M,mx,k)

elif st=='n':
    
    out_table(N, M, mx)






