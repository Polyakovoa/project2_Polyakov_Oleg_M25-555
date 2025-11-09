#!/usr/bin/env python3

import time


def handle_db_errors(func):
    """Декоратор для обработки ошибок базы данных."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError:
            print("Ошибка: Файл данных не найден. Возможно, база данных не инициализирована.")  # noqa: E501
        except KeyError as e:
            print(f"Ошибка: Таблица или столбец {e} не найден.")
        except ValueError as e:
            print(f"Ошибка валидации: {e}")
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")
    return wrapper

def confirm_action(action_name):
    """Декоратор для подтверждения опасных операций.
    
    Args:
        action_name: Название действия для отображения в запросе
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            response = input(f'Вы уверены, что хотите выполнить "{action_name}"? [y/n]: ').strip().lower()  # noqa: E501
            if response == 'y':
                return func(*args, **kwargs)
            else:
                print("Операция отменена.")
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