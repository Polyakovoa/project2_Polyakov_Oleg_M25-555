#!/usr/bin/env python3

import json
import os


def load_metadata(filepath: str) -> dict:
    """Загружает данные из JSON-файла.
    
    Args:
        filepath: Путь к JSON-файлу
        
    Returns:
        dict: Загруженные данные или пустой словарь, если файл не найден
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_metadata(filepath: str, data: dict) -> None:
    """Сохраняет данные в JSON-файл.
    
    Args:
        filepath: Путь к JSON-файлу
        data: Данные для сохранения
    """
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)

def load_table_data(table_name: str) -> list:
    """Загружает данные таблицы из JSON-файла.
    
    Args:
        table_name: Имя таблицы
        
    Returns:
        list: Данные таблицы или пустой список, если файл не найден
    """
    data_dir = "data"
    filepath = os.path.join(data_dir, f"{table_name}.json")
    
    # Создаем директорию data если не существует
    os.makedirs(data_dir, exist_ok=True)
    
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_table_data(table_name: str, data: list) -> None:
    """Сохраняет данные таблицы в JSON-файл.
    
    Args:
        table_name: Имя таблицы
        data: Данные для сохранения
    """
    data_dir = "data"
    filepath = os.path.join(data_dir, f"{table_name}.json")
    
    # Создаем директорию data если не существует
    os.makedirs(data_dir, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=2)