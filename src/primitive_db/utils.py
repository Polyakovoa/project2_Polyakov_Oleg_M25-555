#!/usr/bin/env python3

import json


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