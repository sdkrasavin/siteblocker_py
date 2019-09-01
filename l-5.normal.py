#!/usr/bin/env python3
# coding : utf-8

import math
import random
from math import sqrt


__author__ = 'Sergei Krasavin'

# Задача-1:
# Напишите небольшую консольную утилиту,
# позволяющую работать с папками текущей директории.
# Утилита должна иметь меню выбора действия, в котором будут пункты:
# 1. Перейти в папку
# 2. Просмотреть содержимое текущей папки
# 3. Удалить папку
# 4. Создать папку
# При выборе пунктов 1, 3, 4 программа запрашивает название папки
# и выводит результат действия: "Успешно создано/удалено/перешел",
# "Невозможно создать/удалить/перейти"

# Для решения данной задачи используйте алгоритмы из задания easy,
# оформленные в виде соответствующих функций,
# и импортированные в данный файл из easy.py

from lesson5.easy import chdir, makedir, removedir, os, nowdir
print('Ваша текущая директория {}'.format(os.getcwd()))
menu = 0
try:
    while(menu < 1 or menu > 4):
        menu = int(input('Выберите один из пунктов\n1. Перейти в папку\n2. Просмотреть содержимое текущей папки\n3. Удалить папку\n4. Создать папку\nВаш выбор: '))
        if (menu < 1 or menu > 4):
            print('Попробуйте снова')
    print('Ваша текущая директория {}'.format(os.getcwd()))
    if menu == 1:
        folder = str(input('В какую папку вы хотите перейти: '))
        chdir(folder)
    elif menu == 2:
        nowdir();
    elif menu == 3:
        folder = str(input('Какую папку вы хотите удалить: '))
        removedir(folder)
    elif menu == 4:
        folder = str(input('Какую папку вы хотите создать: '))
        makedir(folder)
except ValueError:
    print('Невозможно создать/удалить/прейти\nValueError')
except FileNotFoundError:
    print('Невозможно создать/удалить/прейти\nFileNotFoundError')
else:
    print('Успешно создано/удалено/перешел')
print('Ваша текущая директория {}'.format(os.getcwd()))
