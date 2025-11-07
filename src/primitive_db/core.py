#!/usr/bin/env python3

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

def drop_table(metadata: dict, table_name: str) -> dict:
    """Удаляет таблицу из метаданных.
    
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
    return metadata