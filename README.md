# Primitive Database

Простая база данных для управления таблицами с поддержкой основных операций.

## Установка

make install
или
poetry install

## Запуск

make project
или
poetry run project

## Управление таблицами

Доступные команды:

create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> ... - создать таблицу
list_tables - показать список всех таблиц
drop_table <имя_таблицы> - удалить таблицу
help - справочная информация
exit - выход из программы

Поддерживаемые типы данных:

int - целые числа
str - строки
bool - логические значения

## Демонстрация работы:

На сайте Asciinema: https://asciinema.org/a/4M5i8e6d30LfrY9P4fiaLK7zK

Демонстрация в текстовом формате:

admin@Ubuntu:~/Рабочий стол/project2_Polyakov_Oleg_M25-555/project2_Polyakov_Oleg_M25-555$ project
***База данных***

Функции:
<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу
<command> list_tables - показать список всех таблиц
<command> drop_table <имя_таблицы> - удалить таблицу
<command> exit - выход из программы
<command> help - справочная информация

>>>Введите команду: create_table users name:str age:int is_active:bool
Таблица "users" успешно создана со столбцами: ID:int, name:str, age:int, is_active:bool

>>>Введите команду: create_table products title:str price: int
Ошибка: Некорректный тип данных: . Допустимые типы: int, str, bool

>>>Введите команду: create_table products title:str price:int
Таблица "products" успешно создана со столбцами: ID:int, title:str, price:int

>>>Введите команду: list_tables
- users
- products

>>>Введите команду: drop_table products
Таблица "products" успешно удалена.

>>>Введите команду: list_tables
- users

>>>Введите команду: exit
Выход из программы.
admin@Ubuntu:~/Рабочий стол/project2_Polyakov_Oleg_M25-555/project2_Polyakov_Oleg_M25-555$
exit