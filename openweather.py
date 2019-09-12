#!/usr/bin/env python3
# coding : utf-8

"""
== OpenWeatherMap ==
OpenWeatherMap — онлайн-сервис, который предоставляет бесплатный API
 для доступа к данным о текущей погоде, прогнозам, для web-сервисов
 и мобильных приложений. Архивные данные доступны только на коммерческой основе.
 В качестве источника данных используются официальные метеорологические службы
 данные из метеостанций аэропортов, и данные с частных метеостанций.
Необходимо решить следующие задачи:
== Получение APPID ==
    Чтобы получать данные о погоде необходимо получить бесплатный APPID.

    Предлагается 2 варианта (по желанию):
    - получить APPID вручную
    - автоматизировать процесс получения APPID,
    используя дополнительную библиотеку GRAB (pip install grab)
        Необходимо зарегистрироваться на сайте openweathermap.org:
        https://home.openweathermap.org/users/sign_up
        Войти на сайт по ссылке:
        https://home.openweathermap.org/users/sign_in
        Свой ключ "вытащить" со страницы отсюда:
        https://home.openweathermap.org/api_keys

        Ключ имеет смысл сохранить в локальный файл, например, "app.id"

== Получение списка городов ==
    Список городов может быть получен по ссылке:
    http://bulk.openweathermap.org/sample/city.list.json.gz

    Далее снова есть несколько вариантов (по желанию):
    - скачать и распаковать список вручную
    - автоматизировать скачивание (ulrlib) и распаковку списка
     (воспользоваться модулем gzip
      или распаковать внешним архиватором, воспользовавшись модулем subprocess)

    Список достаточно большой. Представляет собой JSON-строки:
{"_id":707860,"name":"Hurzuf","country":"UA","coord":{"lon":34.283333,"lat":44.549999}}
{"_id":519188,"name":"Novinki","country":"RU","coord":{"lon":37.666668,"lat":55.683334}}


== Получение погоды ==
    На основе списка городов можно делать запрос к сервису по id города. И тут как раз понадобится APPID.
        By city ID
        Examples of API calls:
        http://api.openweathermap.org/data/2.5/weather?id=2172797&appid=b1b15e88fa797225412429c1c50c122a
    Для получения температуры по Цельсию:
    http://api.openweathermap.org/data/2.5/weather?id=520068&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Для запроса по нескольким городам сразу:
    http://api.openweathermap.org/data/2.5/group?id=524901,703448,2643743&units=metric&appid=b1b15e88fa797225412429c1c50c122a
    Данные о погоде выдаются в JSON-формате
    {"coord":{"lon":38.44,"lat":55.87},
    "weather":[{"id":803,"main":"Clouds","description":"broken clouds","icon":"04n"}],
    "base":"cmc stations","main":{"temp":280.03,"pressure":1006,"humidity":83,
    "temp_min":273.15,"temp_max":284.55},"wind":{"speed":3.08,"deg":265,"gust":7.2},
    "rain":{"3h":0.015},"clouds":{"all":76},"dt":1465156452,
    "sys":{"type":3,"id":57233,"message":0.0024,"country":"RU","sunrise":1465087473,
    "sunset":1465149961},"id":520068,"name":"Noginsk","cod":200}
== Сохранение данных в локальную БД ==
Программа должна позволять:
1. Создавать файл базы данных SQLite со следующей структурой данных
   (если файла базы данных не существует):
    Погода
        id_города           INTEGER PRIMARY KEY
        Город               VARCHAR(255)
        Дата                DATE
        Температура         INTEGER
        id_погоды           INTEGER                 # weather.id из JSON-данных
2. Выводить список стран из файла и предлагать пользователю выбрать страну
(ввиду того, что список городов и стран весьма велик
 имеет смысл запрашивать у пользователя имя города или страны
 и искать данные в списке доступных городов/стран (регуляркой))
3. Скачивать JSON (XML) файлы погоды в городах выбранной страны
4. Парсить последовательно каждый из файлов и добавлять данные о погоде в базу
   данных. Если данные для данного города и данного дня есть в базе - обновить
   температуру в существующей записи.
При повторном запуске скрипта:
- используется уже скачанный файл с городами;
- используется созданная база данных, новые данные добавляются и обновляются.
При работе с XML-файлами:
Доступ к данным в XML-файлах происходит через пространство имен:
<forecast ... xmlns="http://weather.yandex.ru/forecast ...>
Чтобы работать с пространствами имен удобно пользоваться такими функциями:
    # Получим пространство имен из первого тега:
    def gen_ns(tag):
        if tag.startswith('{'):
            ns, tag = tag.split('}')
            return ns[1:]
        else:
            return ''
    tree = ET.parse(f)
    root = tree.getroot()
    # Определим словарь с namespace
    namespaces = {'ns': gen_ns(root.tag)}
    # Ищем по дереву тегов
    for day in root.iterfind('ns:day', namespaces=namespaces):
        ...
"""

import requests
import json
import sqlite3
import os
import gzip
from datetime import date


class WeatherBase():
    def __init__(self, name):
        self.database = name
        self.conn = sqlite3.connect(self.database)
        self.cursor = self.conn.cursor()

        try:
            self.cursor.execute("""CREATE TABLE weather
                              (city_id INTEGER PRIMARY KEY, city_name VARCHAR(255), info_date DATE,
                               temperature INTEGER, weather_id INTEGER)
                           """)
        except sqlite3.OperationalError:
            pass

    def add_data(self, city_id, name, info_date, temp, wet_id):
        try:
            self.cursor.execute("""INSERT INTO weather
                      VALUES ('""" + str(city_id) + "', '" + str(name) + "', '" + str(info_date) + "', '"
                                + str(temp) + "', '" + str(wet_id) + "')"
                                )
            self.conn.commit()
        except sqlite3.IntegrityError:
            sql = """
            UPDATE weather 
            SET info_date = '""" + str(info_date) + "', temperature = '" + str(temp) + "' " + """
            WHERE city_id = '""" + str(city_id) + "'"
            self.cursor.execute(sql)
            self.conn.commit()

    def show_cities(self):
        sql = "SELECT city_name FROM weather"
        for x in self.cursor.execute(sql):
            print(x[0])

    def show_data(self, city_name):
        try:
            sql = "SELECT * FROM weather WHERE city_name = '" + str(city_name) + "'"
            self.cursor.execute(sql)
            info = self.cursor.fetchall()[0]
            print(f"{info[2]} Температура в городе {info[1]} составляет {info[3]} \xB0C")
        except IndexError:
            print('Нет такого города в базе. Необходимо запросить данные у службы либо введите название корректно.')


class CityWeather(dict):
    with open('app.id', 'r') as f:
        APP_ID = f.read().strip()

    API_URL = 'http://api.openweathermap.org/data/2.5/weather'

    def __init__(self, city_name, base, save='no'):
        self.city_name = city_name
        self.base = base
        self.today = date.today().strftime("%d/%m/%Y")

        for i in city_data:
            if i['name'] == city_name:
                self.city_id = i['id']

        self.params = {
            'id': self.city_id,
            'APPID': self.APP_ID,
            'units': 'metric'
        }
        self.res = requests.get(self.API_URL, params=self.params)
        self.weather_info = self.res.json()

        self.base.add_data(self.city_id, self.city_name, self.today, self.weather_info['main']['temp'],
                           self.weather_info['weather'][0]['id'])

        if save == 'yes':
            file_name = self.city_name + '.json'
            file_path = os.path.join(os.getcwd(), file_name)
            with open(file_path, 'w') as f:
                json.dump(self.weather_info, f)

    def __str__(self):
        return f"Temperature in {self.city_name} is {self.weather_info['main']['temp']} \xB0C"


def city_list():
    global city_data
    list_name = 'city.list.json'
    list_path = os.path.join(os.getcwd(), list_name)
    if os.path.exists(list_path):
        with open(list_path, 'r', encoding='utf8') as f:
            city_data = json.load(f)
    else:
        list_url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
        list_req = requests.get(list_url)
        gz_name = 'city.list.json.gz'
        gz_path = os.path.join(os.getcwd(), gz_name)
        with open(gz_path, 'wb') as f:
            f.write(list_req.content)
        with gzip.open(gz_path, 'rb') as zf:
            with open(list_path, 'wb') as jf:
                jf.write(zf.read())
        os.remove(gz_path)
        with open(list_path, 'r', encoding='utf8') as f:
            city_data = json.load(f)


def main():
    city_list()
    print('Weather Report\n')
    print('Здравствуйте!')
    answers = ['1', '2', '3', '4', '5']
    answer = ''
    while answer is not '5':
        print()
        print('1. Вывести список городов из базы данных.')
        print('2. Показать информацию о погоде в городе из базы данных.')
        print('3. Запросить свежие данные о погоде в городе из метеослужбы.')
        print('4. Скачать JSON-файл с данными о погоде в городе.')
        print('5. Выйти из программы.')
        print()

        answer = input('Ваш выбор? ').lower()

        if answer == '1':
            new_base.show_cities()
        elif answer == '2':
            city = input('Введите название города. ')
            print()
            new_base.show_data(city)
        elif answer == '3':
            city = input('Введите название города. ')
            new_request = CityWeather(city, new_base)
            print(new_request)
        elif answer == '4':
            city = input('Введите название города. ')
            new_request = CityWeather(city, new_base, save='yes')
        elif answer == '5':
            break
        else:
            print('Такого пути нет. Выберите другой.')


new_base = WeatherBase("weather.db")

if __name__ == '__main__':
    main()

input("Press Enter")