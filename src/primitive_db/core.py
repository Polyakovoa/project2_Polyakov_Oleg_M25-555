#!/usr/bin/env python3

import os

from .decorators import confirm_action, create_cacher, handle_db_errors, log_time

# Создаем кэшер для запросов select
select_cacher = create_cacher()


@handle_db_errors
def create_table(metadata: dict, table_name: str, columns: list) -> dict:
    """Создает новую таблицу в метаданных.
    
    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя создаваемой таблицы
        columns: Список столбцов в формате ['name:str', 'age:int']
        
    Returns:
        dict: Обновленные метаданные
        
    Raises:
        ValueError: Если таблица уже существует или неверный тип данных
    """
    # Проверяем, существует ли таблица
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')
    
    # Добавляем автоматический столбец ID:int в начало
    table_columns = ['ID:int']
    
    # Проверяем и добавляем остальные столбцы
    for column in columns:
        if ':' not in column:
            raise ValueError(f'Некорректный формат столбца: {column}')
        
        col_name, col_type = column.split(':', 1)
        col_type = col_type.lower()
        
        # Проверяем корректность типа данных
        if col_type not in ('int', 'str', 'bool'):
            raise ValueError(f'Некорректный тип данных: {col_type}. '
                           'Допустимые типы: int, str, bool')
        
        table_columns.append(f'{col_name}:{col_type}')
    
    # Сохраняем таблицу в метаданные
    metadata[table_name] = table_columns
    return metadata


@handle_db_errors
@confirm_action("удаление таблицы")
def drop_table(metadata: dict, table_name: str) -> dict:
    """Удаляет таблицу из метаданных и удаляет файл с данными.
    
    Args:
        metadata: Текущие метаданные базы данных
        table_name: Имя удаляемой таблицы
        
    Returns:
        dict: Обновленные метаданные
        
    Raises:
        ValueError: Если таблица не существует
    """
    # Проверяем, существует ли таблица
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')
    
    # Удаляем таблицу из метаданных
    del metadata[table_name]
    
    # Удаляем файл с данными таблицы
    data_file = f"data/{table_name}.json"
    if os.path.exists(data_file):
        os.remove(data_file)
    
    return metadata


@handle_db_errors
@log_time
def insert(metadata: dict, table_name: str, values: list) -> tuple:
    """Добавляет новую запись в таблицу.
    
    Args:
        metadata: Метаданные базы данных
        table_name: Имя таблицы
        values: Список значений для вставки
        
    Returns:
        tuple: (новый ID, обновленные данные таблицы)
        
    Raises:
        ValueError: Если таблица не существует или неверные данные
    """
    if table_name not in metadata:
        raise ValueError(f'Таблица "{table_name}" не существует.')
    
    # Получаем схему таблицы (без ID столбца для проверки количества)
    table_columns = metadata[table_name][1:]  # Пропускаем ID:int
    expected_count = len(table_columns)
    
    if len(values) != expected_count:
        raise ValueError(f'Ожидается {expected_count} значений, '
                       f'получено {len(values)}')
    
    # Валидируем типы данных
    validated_values = []
    for i, (column, value) in enumerate(zip(table_columns, values)):
        col_name, col_type = column.split(':')
        
        try:
            if col_type == 'int':
                validated_value = int(value)
            elif col_type == 'bool':
                # Преобразуем строки в bool
                if value.lower() in ('true', '1', 'yes'):
                    validated_value = True
                elif value.lower() in ('false', '0', 'no'):
                    validated_value = False
                else:
                    raise ValueError(f'Некорректное булево значение: {value}')
            else:  # str
                # Убираем кавычки если они есть
                validated_value = str(value).strip('"\'')
            
            validated_values.append(validated_value)
        except (ValueError, TypeError) as e:
            raise ValueError(f'Неверный тип для столбца {col_name}: {e}')
    
    return validated_values


@handle_db_errors
@log_time
def _select_impl(table_data: list, where_clause: dict = None) -> list:
    """Внутренняя реализация select без кэширования."""
    if where_clause is None:
        return table_data
    
    filtered_data = []
    for record in table_data:
        match = True
        for column, value in where_clause.items():
            record_value = record.get(column)
            
            # Преобразуем значение для сравнения
            if isinstance(record_value, bool):
                # Для bool преобразуем строки в булевы значения
                if isinstance(value, str):
                    if value.lower() in ('true', '1', 'yes', 'false', '0', 'no'):  # noqa: E501
                        if value.lower() in ('true', '1', 'yes'):
                            compare_value = True
                        else:
                            compare_value = False
                    else:
                        # Если это не булева строка, сравниваем как строки
                        compare_value = value
                else:
                    compare_value = value
            else:
                compare_value = value
            
            # Сравниваем значения
            if isinstance(record_value, bool) and isinstance(compare_value, bool):  # noqa: E501
                if record_value != compare_value:
                    match = False
                    break
            else:
                if str(record_value) != str(compare_value):
                    match = False
                    break
        
        if match:
            filtered_data.append(record)
    
    return filtered_data


def select(table_data: list, where_clause: dict = None) -> list:
    """Выбирает записи из данных таблицы с кэшированием.
    
    Args:
        table_data: Данные таблицы
        where_clause: Условие фильтрации {столбец: значение}
        
    Returns:
        list: Отфильтрованные данные
    """
    # Создаем ключ для кэша на основе данных и условия
    cache_key = f"select_{id(table_data)}_{str(where_clause)}"
    
    def get_data():
        return _select_impl(table_data, where_clause)
    
    return select_cacher(cache_key, get_data)


@handle_db_errors
def update(table_data: list, set_clause: dict, where_clause: dict) -> list:
    """Обновляет записи в данных таблицы.
    
    Args:
        table_data: Данные таблицы
        set_clause: Поля для обновления {столбец: новое_значение}
        where_clause: Условие фильтрации {столбец: значение}
        
    Returns:
        list: Обновленные данные
    """
    updated_data = []
    updated_count = 0
    
    for record in table_data:
        match = True
        for column, value in where_clause.items():
            if str(record.get(column)) != str(value):
                match = False
                break
        
        if match:
            # Обновляем запись
            updated_record = record.copy()
            for column, new_value in set_clause.items():
                if column in updated_record:
                    # Преобразуем тип если нужно
                    if isinstance(updated_record[column], bool):
                        if new_value.lower() in ('true', '1', 'yes'):
                            updated_record[column] = True
                        elif new_value.lower() in ('false', '0', 'no'):
                            updated_record[column] = False
                    elif isinstance(updated_record[column], int):
                        updated_record[column] = int(new_value)
                    else:
                        updated_record[column] = str(new_value).strip('"\'')
            updated_data.append(updated_record)
            updated_count += 1
        else:
            updated_data.append(record)
    
    return updated_data


@handle_db_errors
@confirm_action("удаление записей")
def delete(table_data: list, where_clause: dict) -> list:
    """Удаляет записи из данных таблицы.
    
    Args:
        table_data: Данные таблицы
        where_clause: Условие фильтрации {столбец: значение}
        
    Returns:
        list: Данные после удаления
    """
    if where_clause is None:
        return []
    
    filtered_data = []
    
    for record in table_data:
        match = True
        for column, value in where_clause.items():
            record_value = record.get(column)
            
            # Преобразуем значение для сравнения
            if isinstance(record_value, bool):
                # Для bool преобразуем строки в булевы значения
                if isinstance(value, str):
                    if value.lower() in ('true', '1', 'yes', 'false', '0', 'no'):  # noqa: E501
                        if value.lower() in ('true', '1', 'yes'):
                            compare_value = True
                        else:
                            compare_value = False
                    else:
                        # Если это не булева строка, сравниваем как строки
                        compare_value = value
                else:
                    compare_value = value
            else:
                compare_value = value
            
            # Сравниваем значения
            if isinstance(record_value, bool) and isinstance(compare_value, bool):  # noqa: E501
                if record_value != compare_value:
                    match = False
                    break
            else:
                if str(record_value) != str(compare_value):
                    match = False
                    break
        
        if not match:
            filtered_data.append(record)
    
    return filtered_data