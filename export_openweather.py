#!/usr/bin/env python3
# coding : utf-8

import csv
import json
import os
import sys
import shutil
import sqlite3
import pandas as pd
import requests


__author__ = 'Sergei Krasavin'

""" OpenWeatherMap (экспорт)
Сделать скрипт, экспортирующий данные из базы данных погоды, 
созданной скриптом openweather.py. Экспорт происходит в формате CSV или JSON.
Скрипт запускается из командной строки и получает на входе:
    export_openweather.py --csv filename [<город>]
    export_openweather.py --json filename [<город>]
    export_openweather.py --html filename [<город>]

При выгрузке в html можно по коду погоды (weather.id) подтянуть 
соответствующие картинки отсюда:  http://openweathermap.org/weather-conditions
Экспорт происходит в файл filename.
Опционально можно задать в командной строке город. В этом случае 
экспортируются только данные по указанному городу. Если города нет в базе -
выводится соответствующее сообщение.
"""

print('sys.argv = ', sys.argv)

def collect_data(city_name=None):
    global info
    global names
    database = "weather.db"
    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    if city_name == None:
        sql = "SELECT * FROM weather"
    else:
        sql = "SELECT * FROM weather WHERE city_name = '" + str(city_name) + "'"
    info = cursor.execute(sql)
    names = list(map(lambda x: x[0], cursor.description))


def csv_import(filename):
    file_path = os.path.join(os.getcwd(), filename + '.csv')
    with open(file_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(names)
        for x in info:
            writer.writerow(x)

def json_import(filename):
    file_path = os.path.join(os.getcwd(), filename + '.json')
    json_out = []
    for i in info:
        y = dict(zip(names, i))
        json_out.append(y)
    with open(file_path, 'w') as f:
        json.dump(json_out, f, indent=4)

def html_import(filename):
    file_path = os.path.join(os.getcwd(), filename + '.html')
    html_out = []
    for i in info:
        y = dict(zip(names, i))
        html_out.append(y)
    df = pd.DataFrame(html_out)
    df.to_html(file_path)

def main():
    do = {
        "--csv": csv_import,
        "--json": json_import,
        "--html": html_import
    }


    try:
        city_name = sys.argv[3]
    except IndexError:
        city_name = None

    collect_data(city_name=city_name)


    try:
        filename = sys.argv[2]
    except IndexError:
        filename = 'weather'


    try:
        key = sys.argv[1]
    except IndexError:
        key = None


    if key:
        if do.get(key):
            do[key](filename)
        else:
            print("Задан неверный ключ")


if __name__ == '__main__':
    main()

input("Press Enter")