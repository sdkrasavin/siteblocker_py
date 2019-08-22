#!/usr/bin/env python3
# coding : utf-8

import math
import random
from math import sqrt


__author__ = 'Sergei Krasavin'


# Задача-1:
# Дан список фруктов.
# Напишите программу, выводящую фрукты в виде нумерованного списка,
# выровненного по правой стороне.

# Пример:
# Дано: ["яблоко", "банан", "киви", "арбуз"]
# Вывод:
# 1. яблоко
# 2.  банан
# 3.   киви
# 4.  арбуз

fruits = ['яблоко', 'банан', 'киви', 'арбуз']
name = len(fruits)
for i in range(name):
    print(str(i+1) + '.' + '{}'.format(fruits[i]))

# Задача-2:
# Даны два произвольные списка.
# Удалите из первого списка элементы, присутствующие во втором списке.

first_list = [1,2,3,4,5]
second_list = [4,3,6,5,7]
first_list = [x for x in first_list if x not in second_list]
print (first_list)



# Задача-3:
# Дан произвольный список из целых чисел.
# Получите НОВЫЙ список из элементов исходного, выполнив следующие условия:
# если элемент кратен двум, то разделить его на 4, если не кратен, то умножить на два.
list = [1,2,3,4,5,6,7]
print ("initial list: ", list)
new_list = []
for i in list:
    if i % 2 == 0:
        new_list.append(i/4)
    else:
        new_list.append(2*i)
        print ("Result: ", new_list)

