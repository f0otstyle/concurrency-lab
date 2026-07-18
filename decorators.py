from time import perf_counter, sleep
from typing import Callable, Coroutine
from functools import wraps, lru_cache
import random
import asyncio
import logging
import pickle


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger('decorate')

# ===================================
#           Декораторы
# ===================================


# № 1 Написать декоратор timer:
def timer(func: Callable | Coroutine):
    '''Синхроный и асинхронный декоратор для подсчета времени'''
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = perf_counter()
        res = func(*args, **kwargs)
        elapsed = perf_counter() - start
        logger.info(f'Время выполнения фунцкции {elapsed:.5f}')
        return res

    @wraps(func)
    async def async_wrapper(*args, **kwargs):
        start = perf_counter()
        res = await func(*args, **kwargs)
        elapsed = perf_counter() - start
        logger.info(f'Время выполнения фунцкции {elapsed:.5f}')
        return res

    return async_wrapper if asyncio.iscoroutinefunction(func) else wrapper


# № 2 Написать декоратор retry:
def retry(times=3, delay=1):
    '''Декаратор для повторного выполнения функции если запрос упал'''
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(times):
                try:
                    result = func(*args, **kwargs)
                    logger.info(f'Функция обработала ответ за {i} попытку')
                    return result
                except Exception:
                    if i == times - 1:
                        logger.error(f'Все {times} попыток провалились')
                        raise
                    sleep(delay)
            return None
        return wrapper
    return decorator


# № 3 Написать декоратор cache_result:
def cache_result(func: Callable):
    '''Декоратор для проверки кеша'''
    cache: dict = {}

    @wraps(func)
    def wrapper(*args, **kwargs):
        key = pickle.dumps((args, sorted(kwargs.items())))
        if key in cache:
            return cache[key]
        result = func(*args, **kwargs)
        cache[key] = result
        return result
    return wrapper


# ===================================
#           Тесты декораторов
# ===================================
# № 1

@timer
def func_sleep():
    sleep(2)


@timer
async def async_func_sleep():
    await asyncio.sleep(2)


@retry(times=3, delay=1)
def func_requst():
    sleep(1)
    if random.random() < 0.7:
        raise ValueError("Случайная ошибка!")
    return "Успешно!"


@timer
@cache_result
def get_element_list(lst, index):
    print(f'Идёт вычисление: список {lst}, индекс {index}')
    return lst[index]


@timer
@lru_cache
def get_element_tuple(tuple, index):
    print(f'Идёт вычисление: кортеж {tuple}, индекс {index}')
    return tuple[index]


if __name__ == '__main__':
    func_sleep()
    asyncio.run(async_func_sleep())
    func_requst()

    my_tuple: tuple = (10, 20, 30, 40, 50)
    print(get_element_tuple(my_tuple, 2))

    my_list: list[int] = [10, 20, 30, 40, 50]
    print(get_element_list(my_list, 2))
