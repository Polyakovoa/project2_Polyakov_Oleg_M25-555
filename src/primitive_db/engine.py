#!/usr/bin/env python3

import shlex
from .utils import load_metadata, save_metadata
from .core import create_table, drop_table


def welcome():
    """Функция приветствия и игрового цикла"""
    print("Первая попытка запустить проект!\n")
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")
    
    while True:
        command = input("Введите команду: ").strip().lower()
        
        if command == "exit":
            print("Выход из программы.")
            break
        elif command == "help":
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {command}")


def run():
    """Главная функция с основным циклом программы"""
    metadata_file = "db_meta.json"
    
    print("***База данных***\n")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")
    
    while True:
        try:
            user_input = input("\n>>>Введите команду: ").strip()
            if not user_input:
                continue
                
            args = shlex.split(user_input)
            command = args[0].lower()
            
            # Загружаем актуальные метаданные
            metadata = load_metadata(metadata_file)
            
            if command == "exit":
                print("Выход из программы.")
                break
                
            elif command == "help":
                print("***Процесс работы с таблицей***")
                print("Функции:")
                print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
                print("<command> list_tables - показать список всех таблиц")
                print("<command> drop_table <имя_таблицы> - удалить таблицу")
                print("<command> exit - выход из программы")
                print("<command> help - справочная информация")
                
            elif command == "create_table":
                if len(args) < 3:
                    print("Ошибка: Недостаточно аргументов для create_table")
                    continue
                table_name = args[1]
                columns = args[2:]
                metadata = create_table(metadata, table_name, columns)
                save_metadata(metadata_file, metadata)
                column_list = ", ".join(metadata[table_name])
                print(f'Таблица "{table_name}" успешно создана со столбцами: {column_list}')  # noqa: E501
                
            elif command == "list_tables":
                if not metadata:
                    print("Нет созданных таблиц")
                else:
                    for table_name in metadata:
                        print(f"- {table_name}")
                        
            elif command == "drop_table":
                if len(args) < 2:
                    print("Ошибка: Недостаточно аргументов для drop_table")
                    continue
                table_name = args[1]
                metadata = drop_table(metadata, table_name)
                save_metadata(metadata_file, metadata)
                print(f'Таблица "{table_name}" успешно удалена.')
                
            else:
                print(f'Функции "{command}" нет. Попробуйте снова.')
                
        except ValueError as e:
            print(f"Ошибка: {e}")
        except Exception as e:
            print(f"Некорректное значение: {e}. Попробуйте снова.")