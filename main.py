import random
import matplotlib.pyplot as plt
from statistics import mean, median, stdev
from gen_of_corr import get_corr_row
import pandas as pd
import numpy as np
import math 

def transform_signal(uniform_signal, N, m=None):
    """ 
    Преобразование равномерного сигнала в гауссовский
    """

    gaussian_signal = []
    for i in range(0, N, 2):
        
        u1 = uniform_signal[i]
        u2 = uniform_signal[i+1]
        
        r = math.sqrt(-2 * math.log(u1))
        theta = 2 * math.pi * u2
        z1 = r * math.cos(theta)
        z2 = r * math.sin(theta)

        # # добавляем математическое ожидание (разладка)
        # if m is not None:
        #     if i >= m:
        #         z1 += 1 
        #         z2 += 1

        gaussian_signal.append(z1)
        gaussian_signal.append(z2)
        
    return gaussian_signal

def get_correlation(gaussian_signal, b1, b2):
    """
    Введение корреляции в гауссовский сигнал
    """
    corr_gaussian_signal = []
    x1 = b1 * 0 + b2 * 0 + gaussian_signal[0]
    x2 = b1 * x1 + b2 * 0 + gaussian_signal[1]
    corr_gaussian_signal.append(x1)
    corr_gaussian_signal.append(x2)

    for i in range(2, len(gaussian_signal)):
        
        e = gaussian_signal[i]
        x = b1 * corr_gaussian_signal[i-1] + b2 * corr_gaussian_signal[i-2] + e
        corr_gaussian_signal.append(x)

    # corr_gaussian_signal = corr_gaussian_signal[2:]
    
    # нормализация
    mn = mean(corr_gaussian_signal)
    std = stdev(corr_gaussian_signal)
    corr_gaussian_signal = ((np.array(corr_gaussian_signal) - mn) / std).tolist()

    return corr_gaussian_signal

def get_auto_corr(timeSeries,k):
    '''
    Descr:输入：时间序列timeSeries，滞后阶数k
            输出：时间序列timeSeries的k阶自相关系数
        l：序列timeSeries的长度
        timeSeries1，timeSeries2:拆分序列1，拆分序列2
        timeSeries_mean:序列timeSeries的均值
        timeSeries_var:序列timeSeries的每一项减去均值的平方的和

    '''
    l = len(timeSeries)
    #取出要计算的两个数组
    timeSeries1 = timeSeries[0:l-k]
    timeSeries2 = timeSeries[k:]
    timeSeries_mean = timeSeries.mean()
    timeSeries_var = np.array([i**2 for i in timeSeries-timeSeries_mean]).sum()
    auto_corr = 0
    for i in range(l-k):
        temp = (timeSeries1[i]-timeSeries_mean)*(timeSeries2[i]-timeSeries_mean)/timeSeries_var
        auto_corr = auto_corr + temp
    return auto_corr

def plot_auto_corr(timeSeries,k):
    '''
    Descr:需要计算自相关函数get_auto_corr(timeSeries,k)
            输入时间序列timeSeries和想绘制的阶数k，k不能超过timeSeries的长度
            输出：k阶自相关系数图，用于判断平稳性
    '''
    timeSeriestimeSeries = pd.DataFrame(range(k))
    for i in range(1,k+1):
        timeSeriestimeSeries.loc[i-1] =get_auto_corr(timeSeries,i)
    for i,v in enumerate(list(timeSeriestimeSeries[0])):
        if v<=0.05 and v>=-0.05:
            Tay = i
            print(f'Тау mk = {i}')
            print(f'Тау к = {abs(sum(list(timeSeriestimeSeries[0][:Tay])))}')
            break
    plt.subplot(1, 2, 1)
    lst = plt.bar(range(1,len(timeSeriestimeSeries)+1),timeSeriestimeSeries[0])
    lst[Tay].set_color('r')
    plt.title("Корреляционная функция")
    
    



def mean_of_razl(m, N, L, k, mx = 0):
    """
    Усреднение по m значениям
    """
    lst = [[], [], [], []]
    res_list = [[], [], [], []]
    for i in range(m):
        out_lst = razl(N, L, k, mx = mx, out = 0)
        res_list[0] = out_lst[0]
        res_list[1].append(out_lst[1])
        res_list[2].append(out_lst[2])
        res_list[3].append(out_lst[3])

    if res_list[1].count("-") <= (len(res_list[1])-res_list[1].count("-")):
        buf = []
        for i in range(len(res_list[1])):
            if str(type(res_list[1][i])) != "<class 'str'>":
                buf.append(res_list[1][i])
        res_list[1] = buf
        res_list[1] = mean(res_list[1])
    else:
        res_list[1] = "-"

    res_list[2] = int(mean(res_list[2]))
    res_list[3] = int(mean(res_list[3]))

    lst[0].append(res_list[0])
    if (str(type(res_list[1])) == "<class 'float'>"):
        lst[1].append(round(res_list[1], 2))
    else:
        lst[1].append(res_list[1])
    lst[2].append(res_list[2])
    lst[3].append(res_list[3])
    res_list.clear()
    return lst


def out_table(N, L, mx = 0):

    k_l, k_r = map(int, input("Введите пределы изменения длины серий через запятую (левый,правый) - ").split(','))
    shag = int(input("Введите шаг изменения длины серий (целое число) - "))
    m = int(input("Введите по скольким значениям проводить усреднение - "))
    lst = [[], [], [], []]

    for i in range(k_l, k_r+1, shag):
        out_lst = mean_of_razl(m, N, L, i, mx = mx)
        lst[0].append(out_lst[0][0])
        lst[1].append(out_lst[1][0])
        lst[2].append(out_lst[2][0])
        lst[3].append(out_lst[3][0])

    print("Исходные данные:")
    print(f"Медиана ряда с разладкой - {mx}")
    print(f"Количество повторений для одного k - {m}")
    print(f"Номер такта номинальной разладки - {N}")
    print(f"Длина сигнала - {L}")
    df = pd.DataFrame(lst, columns=list(range(1, (len(lst[0])+1))), index=[
                      "Длина серии", "Среднее время между ложными тревогами", "Среднее время запаздывания", "Номер такта обнаружения разладки"])
    what = ""
    while what not in ["Y", "y", "N", "n"]:
        what = input(
            "Вывести таблицу в excel / Вывести таблицу в консоль 'y/n' ")
    if what == 'y':
        df.to_excel("table.xlsx", sheet_name="sheet_1", header=False)
    elif what == 'n':
        print(df)


def razl(N, L, k, mx = 0, out=1):
    '''
    Определение разладки сигнала
    '''
    def opr_razl(x, med, k, N):
        '''
        Определение разладки сигнала
        '''
        global Tlt
        k_p = 0  # Число положительных серий
        Tlt = []  # Моменты времени ложных тревог
        Tr = []  # Моменты реальных тревог
        for i in range(len(x)):
            if not corr:
                if x[i] >= med:
                    k_p += 1
                elif x[i] < med:
                    k_p = 0
            elif corr and bin:
                if x[i] == 1:
                    k_p += 1
                elif x[i] == 0:
                    k_p = 0
            else:
                if x[i] >= med:
                    k_p += 1
                elif x[i] < med:
                    k_p = 0
            if i == N:
                k_p = 0
            if k_p >= k:
                if i < N:
                    Tlt.append(i)
                elif i >= N:
                    Tr.append(i)
                k_p = 0
        
        return Tr
    if not corr:
        x = []
        x = [(random.uniform(0,1))*1 for i in range(N)]
        med = median(x)
        x.extend([(random.uniform(0,1)+mx-0.5)*1 for i in range(N, L)])
    
    else:
        
        if bin:
            x = get_corr_row(N+1, lamida1 = b1, lamida2 = b2)
            med = median(x)
            x.extend(get_corr_row(L-N+1, lamida1 = b1, lamida2 = b2))
        else:
            x_all = get_correlation(transform_signal([(random.uniform(0,1))*1 for i in range(L)], L), b1 = b1, b2 = b2)
            x = [i+0.5 for i in x_all[:N]]
            med = median(x)
            x.extend([i+mx for i in x_all[N:]])
    Tr = []
    Tr = opr_razl(x, med, k, N)

    razn = []  # Список разностей между ложными тревогами

    # Определение среднего времени между ложными тревогами
    mean_Tlt = 0  # Среднее время между ложными тревогами
    if len(Tlt) != 0:
        if len(Tlt) == 2:
            mean_Tlt = Tlt[1]-Tlt[0]
        elif len(Tlt) == 1:
            mean_Tlt = "-"
        else:
            for i in range(len(Tlt)-1):
                razn.append(Tlt[i+1]-Tlt[i])
            mean_Tlt = mean(razn)
    else:
        if len(Tlt) == 0:
            mean_Tlt = "-"

    if out == 1:
        # Вывод результатов
        print("Результаты моделирования:")
        if len(Tlt) != 0:
            print(f'Моменты времени ложных тревог - {Tlt}')
        else:
            print("Ложные тревоги отсутствуют")
        print(f'Среднее время между ложными тревогами - {mean_Tlt}')
        if len(Tr)!=0:
            print(f'Время запаздывания - {Tr[0]-N}')
        else:
            print("Реальные тревоги отсутствуют")

        x_dot = []      # Значения ряда в моменты реальных тревог
        for i in Tlt:
            x_dot.append(x[i])

        x_dot_real = []  # Значения ряда в моменты реальных тревог
        for i in Tr:
            x_dot_real.append(x[i])
        
        
        if not bin:
            if corr:
                plot_auto_corr(np.array(x[:N]), 20)  
            fig, axs = plt.subplots(1,3)
            axs[1].hist(x[:N], bins = 10)
            axs[1].set_title('Гистограмма исходного сигнала', fontsize=15)
            axs[1].set_ylabel('Число наблюдений', fontsize=10)
            axs[2].hist(x[N:L], bins = 10)
            axs[2].set_title('Гистограмма сигнала с разладкой', fontsize=15)
            axs[2].set_ylabel('Число наблюдений', fontsize=10)

        else:
            if corr:
                plot_auto_corr(np.array(x),20)
            fig, axs = plt.subplots(1,3)
            axs[1].hist(x[:N], bins = 20)
            axs[1].set_title('Гистограмма исходного сигнала', fontsize=15)
            axs[1].set_ylabel('Число наблюдений', fontsize=10)
            axs[2].hist(x[N:L], bins = 20)
            axs[2].set_title('Гистограмма сигнала с разладкой', fontsize=15)
            axs[2].set_ylabel('Число наблюдений', fontsize=10)
        axs[0].plot(range(len(x)), x)
        axs[0].plot(Tlt, x_dot, '.', label="Ложная тревога",
                 color="r", markersize=10)
        axs[0].plot(Tr, x_dot_real, ".", label="Реальная тревога",
                    markersize=10, color="0")
        axs[0].axhline(med, color='y', label='Медиана до разладки')
        axs[0].legend()
        plt.show()
        
    else:
        if not bin:
            out_lst = [k, mean_Tlt, Tr[0]-N, Tr[0]]
        else:
            out_lst = [k, mean_Tlt, 0, 0]
        return out_lst


def opt_k_for_Tlt(N, L, Tlt, mx = 0):
    """
    Нахождение k, удовлетворяющего заданному Tlt
    """
    m = int(input("Введите по скольким значениям проводить усреднение - "))
    k = 1
    out_lst = mean_of_razl(m, N, L, k, mx = mx)
    delta = abs(Tlt-out_lst[1][0])
    while (1):
        k += 1
        out_lst = mean_of_razl(m, N, L, k, mx = mx)

        if str(type(out_lst[1][0])) != "<class 'str'>":
            print
            delta_next = abs(Tlt-out_lst[1][0])
            if delta_next > delta:
                k -= 1
                break
        else:
            break
        delta = delta_next
    print("Исходные данные")
    print(f"Заданное среднее время между ложными тревогами - {Tlt}")
    print(f"Медиана ряда с разладкой - {mx}")
    print(f"Количество повторений для одного k - {m}")
    print(f"Номер такта номинальной разладки - {N}")
    print(f"Длина сигнала - {L}")
    print(f"Оптимальное значение k - {k}")

    st = ""
    while st not in ["y", "Y", "n", "N"]:
        st = input("Вывести результаты исследования для данного k? 'y/n'")
    if st in ["Y", "y"]:
        razl(N, L, k , mx = mx)


def main():
    global corr
    st = ""
    while st not in ["y", "Y", "n", "N"]:
        st = input("Исследовать коррелированный сигнал? 'y/n' ")
    if st in ['Y','y']:
        corr = True
    else:
        corr = False  
    if not corr:    
        st = 0    
        while st not in [1, 2, 3]:
            st = int(input("""
            1-Определение разладки  
            2-Построить таблицу зависимостей 
            3-Определение оптимального k для заданного Tlt' 
            """))
        
        N = int(input("Введите с какого отсчёта пойдёт разладка - "))
        L = int(input("Введите общее число отсчётов - "))
        mx = float(input(
        "Введите медиану процесса начиная с момента заданной разладки(исходная=0.5) - "))

        if st == 1:
            k = int(input("Введите длину серий успехов - "))
            razl(N, L, k , mx = mx)

        elif st == 2:
            out_table(N, L, mx = mx)
        elif st == 3:
            Tlt = float(input("Введите необходимое значение Tlt - "))
            opt_k_for_Tlt(N, L, Tlt, mx = mx)
    else:
        global bin
        bin = False
        st = 0    
        while st not in [1, 2, 3]:
            st = int(input("""
            1-Определение разладки  
            2-Построить таблицу зависимостей 
            3-Определение оптимального k для заданного Tlt' 
            """))
        global b1, b2
        b1, b2 = map(float, input("Введите коэффициенты для рекуррентного соотношения через запятую (b1,b2) - ").split(','))
        if not bin:
            N = int(input("Введите с какого отсчёта пойдёт разладка - "))
            mx = float(input(
            "Введите медиану процесса начиная с момента заданной разладки(исходная=0.5) - "))
        L = int(input("Введите общее число отсчётов - "))
        if st == 1:
            k = int(input("Введите длину серий успехов - "))
            print(f'B1={b1}, B2={b2}')
            razl(N, L, k , mx = mx)

        elif st == 2:
            print(f'B1={b1}, B2={b2}')
            # razl(N, L, 1000, mx = mx)
            out_table(N, L, mx = mx)
        elif st == 3:
            Tlt = float(input("Введите необходимое значение Tlt - "))
            opt_k_for_Tlt(N, L, Tlt, mx = mx)


if __name__ == "__main__":
    main()
