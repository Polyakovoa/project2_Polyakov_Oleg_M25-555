#!/usr/bin/env python3

import time


def handle_db_errors(func):
    """Декоратор для обработки ошибок базы данных."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")  # noqa: E501
            raise  # Пробрасываем исключение дальше
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
            raise
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
            raise
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
            raise
    return wrapper


def confirm_action(action_name: str):
    """Декоратор для подтверждения опасных операций.
    
    Args:
        action_name: Название действия для отображения в запросе подтверждения
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()  # noqa: E501
            if response == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
                # Возвращаем исходные данные вместо None
                if len(args) > 0:
                    return args[0]  # Возвращаем первый аргумент (обычно metadata или table_data) # noqa: E501
                return None
        return wrapper
    return decorator


def log_time(func):
    """Декоратор для замера времени выполнения функции."""
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        print(f"Функция {func.__name__} выполнилась за {execution_time:.3f} секунд.")  # noqa: E501
        return result
    return wrapper


def create_cacher():
    """Фабрика для создания кэшера с замыканием."""
    cache = {}
    
    def cache_result(key, value_func):
        """Кэширует результат выполнения функции.
        
        Args:
            key: Ключ для кэша
            value_func: Функция для получения значения, если его нет в кэше
            
        Returns:
            Результат выполнения value_func или значение из кэша
        """
        if key in cache:
            return cache[key]
        else:
            result = value_func()
            cache[key] = result
            return result
    
    return cache_result

def parse_where_condition(where_str: str) -> dict:
    """Парсит условие WHERE в словарь.
    
    Args:
        where_str: Строка условия вида "age = 28" или "name = 'John'"
        
    Returns:
        dict: Словарь {столбец: значение}
        
    Raises:
        ValueError: Если формат условия некорректен
    """
    if not where_str:
        return {}
    
    # Разбиваем на части по оператору '='
    parts = where_str.split('=', 1)
    if len(parts) != 2:
        raise ValueError('Некорректный формат условия WHERE. '
                       'Используйте: столбец = значение')
    
    column = parts[0].strip()
    value = parts[1].strip()
    
    # Убираем кавычки для строковых значений
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    
    return {column: value}


def parse_set_clause(set_str: str) -> dict:
    """Парсит условие SET в словарь.
    
    Args:
        set_str: Строка условия вида "age = 29" или "name = 'John'"
        
    Returns:
        dict: Словарь {столбец: новое_значение}
        
    Raises:
        ValueError: Если формат условия некорректен
    """
    if not set_str:
        return {}
    
    # Разбиваем на части по оператору '='
    parts = set_str.split('=', 1)
    if len(parts) != 2:
        raise ValueError('Некорректный формат условия SET. '
                       'Используйте: столбец = значение')
    
    column = parts[0].strip()
    value = parts[1].strip()
    
    # Убираем кавычки для строковых значений
    if (value.startswith('"') and value.endswith('"')) or \
       (value.startswith("'") and value.endswith("'")):
        value = value[1:-1]
    
    return {column: value}