#!/usr/bin/env python3

import shlex
from prettytable import PrettyTable
from .utils import load_metadata, save_metadata, load_table_data, save_table_data
from .core import create_table, drop_table, insert, select, update, delete
from .decorators import parse_where_condition, parse_set_clause


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


def display_table(data: list, columns: list) -> None:
    """Отображает данные в виде красивой таблицы.
    
    Args:
        data: Данные для отображения
        columns: Список столбцов в формате ['ID:int', 'name:str', ...]
    """
    if not data:
        print("Нет данных для отображения")
        return
    
    # Создаем таблицу
    table = PrettyTable()
    
    # Извлекаем названия столбцов (без типов)
    field_names = []
    for column in columns:
        col_name = column.split(':')[0]
        field_names.append(col_name)
    
    table.field_names = field_names
    
    # Добавляем данные
    for record in data:
        row = []
        for col_name in field_names:
            row.append(record.get(col_name, ''))
        table.add_row(row)
    
    print(table)


def run():
    """Главная функция с основным циклом программы"""
    metadata_file = "db_meta.json"
    
    print("***Операции с данными***\n")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")  # noqa: E501
    print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")  # noqa: E501
    print("<command> select from <имя_таблицы> - прочитать все записи.")
    print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")  # noqa: E501
    print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")  # noqa: E501
    print("<command> info <имя_таблицы> - вывести информацию о таблице.")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация")
    
    while True:
        try:
            user_input = input("\n>>> Введите команду: ").strip()
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
                print("***Операции с данными***")
                print("Функции:")
                print("<command> create_table <имя_таблицы> <столбец1:тип> <столбец2:тип> .. - создать таблицу")  # noqa: E501
                print("<command> list_tables - показать список всех таблиц")
                print("<command> drop_table <имя_таблицы> - удалить таблицу")
                print("<command> insert into <имя_таблицы> values (<значение1>, <значение2>, ...) - создать запись.")  # noqa: E501
                print("<command> select from <имя_таблицы> where <столбец> = <значение> - прочитать записи по условию.")  # noqa: E501
                print("<command> select from <имя_таблицы> - прочитать все записи.")
                print("<command> update <имя_таблицы> set <столбец1> = <новое_значение1> where <столбец_условия> = <значение_условия> - обновить запись.")  # noqa: E501
                print("<command> delete from <имя_таблицы> where <столбец> = <значение> - удалить запись.")  # noqa: E501
                print("<command> info <имя_таблицы> - вывести информацию о таблице.")
                print("<command> exit - выход из программы")
                print("<command> help - справочная информация")
                
            elif command == "create_table":
                if len(args) < 3:
                    print("Ошибка: Недостаточно аргументов для create_table")
                    continue
                table_name = args[1]
                if ':' in table_name:
                    print(f'Ошибка: Некорректное имя таблицы "{table_name}". '
                          'Имя таблицы не должно содержать двоеточие.')
                    continue
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
                
            elif command == "insert":
                if len(args) < 4 or args[1].lower() != "into" or args[3].lower() != "values":  # noqa: E501
                    print("Ошибка: Неверный формат команды insert. Используйте: insert into <таблица> values (<значения>)")  # noqa: E501
                    continue
                
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                
                # Извлекаем значения из скобок
                values_str = ' '.join(args[4:])
                if not values_str.startswith('(') or not values_str.endswith(')'):  # noqa: E501
                    print("Ошибка: Значения должны быть в скобках")
                    continue
                
                values_str = values_str[1:-1]  # Убираем скобки
                values = [v.strip().strip('"\'') for v in values_str.split(',')]
                
                # Загружаем данные таблицы
                table_data = load_table_data(table_name)
                
                validated_values = insert(metadata, table_name, values)
                
                # Генерируем новый ID
                if table_data:
                    max_id = max(record.get('ID', 0) for record in table_data)  # noqa: E501
                    new_id = max_id + 1
                else:
                    new_id = 1
                
                # Создаем новую запись
                columns = metadata[table_name]
                new_record = {'ID': new_id}
                
                # Добавляем остальные значения
                for i, column in enumerate(columns[1:]):  # Пропускаем ID
                    col_name = column.split(':')[0]
                    new_record[col_name] = validated_values[i]
                
                table_data.append(new_record)
                save_table_data(table_name, table_data)
                print(f'Запись с ID={new_id} успешно добавлена в таблицу "{table_name}".')  # noqa: E501
                    
            elif command == "select":
                if len(args) < 3 or args[1].lower() != "from":
                    print("Ошибка: Неверный формат команды select. Используйте: select from <таблица> [where условие]")  # noqa: E501
                    continue
                
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                
                # Загружаем данные таблицы
                table_data = load_table_data(table_name)
                
                # Проверяем наличие условия WHERE
                where_clause = {}
                if len(args) > 4 and args[3].lower() == "where":
                    where_str = ' '.join(args[4:])
                    where_clause = parse_where_condition(where_str)
                
                # Выполняем выборку
                result_data = select(table_data, where_clause)
                display_table(result_data, metadata[table_name])
                
            elif command == "update":
                if len(args) < 6:
                    print("Ошибка: Неверный формат команды update. Используйте: update <таблица> set <столбец>=<значение> where <условие>")  # noqa: E501
                    continue
                
                table_name = args[1]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                
                if args[2].lower() != "set":
                    print("Ошибка: Отсутствует ключевое слово SET")
                    continue
                
                # Парсим SET условие
                set_parts = []
                i = 3
                while i < len(args) and args[i].lower() != "where":
                    set_parts.append(args[i])
                    i += 1
                
                set_str = ' '.join(set_parts)
                set_clause = parse_set_clause(set_str)
                
                # Парсим WHERE условие
                where_clause = {}
                if i < len(args) and args[i].lower() == "where":
                    where_str = ' '.join(args[i+1:])
                    where_clause = parse_where_condition(where_str)
                
                # Загружаем данные таблицы
                table_data = load_table_data(table_name)
                
                # Выполняем обновление
                updated_data = update(table_data, set_clause, where_clause)
                save_table_data(table_name, updated_data)
                
                # Подсчитываем количество обновленных записей
                original_count = len(table_data)
                updated_count = len([r for r in updated_data if r not in table_data])  # noqa: E501
                print(f'Обновлено {updated_count} записей в таблице "{table_name}".')  # noqa: E501
                
            elif command == "delete":
                if len(args) < 4 or args[1].lower() != "from":
                    print("Ошибка: Неверный формат команды delete. Используйте: delete from <таблица> where <условие>")  # noqa: E501
                    continue
                
                table_name = args[2]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                
                if args[3].lower() != "where":
                    print("Ошибка: Отсутствует ключевое слово WHERE")
                    continue
                
                # Парсим WHERE условие
                where_str = ' '.join(args[4:])
                where_clause = parse_where_condition(where_str)
                
                # Загружаем данные таблицы
                table_data = load_table_data(table_name)
                
                # Выполняем удаление
                original_count = len(table_data)
                updated_data = delete(table_data, where_clause)
                save_table_data(table_name, updated_data)
                
                deleted_count = original_count - len(updated_data)
                print(f'Удалено {deleted_count} записей из таблицы "{table_name}".')  # noqa: E501
                
            elif command == "info":
                if len(args) < 2:
                    print("Ошибка: Недостаточно аргументов для info")
                    continue
                
                table_name = args[1]
                if table_name not in metadata:
                    print(f'Ошибка: Таблица "{table_name}" не существует.')
                    continue
                
                # Загружаем данные таблицы
                table_data = load_table_data(table_name)
                
                columns = metadata[table_name]
                column_list = ", ".join(columns)
                record_count = len(table_data)
                
                print(f"Таблица: {table_name}")
                print(f"Столбцы: {column_list}")
                print(f"Количество записей: {record_count}")
                
            else:
                print(f'Функции "{command}" нет. Попробуйте снова.')
                
        except Exception as e:
            print(f"Ошибка: {e}")