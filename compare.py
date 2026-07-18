import asyncio
from concurrent.futures import ThreadPoolExecutor
import aiohttp
import time
import logging
import requests

TIMEOUT = 15
SEMAPHORE = 5
URL = 'http://localhost:8000/delay/1'

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='compare.log',
    encoding='utf-8',
    filemode='w',
)

logger = logging.getLogger('compare')

# Запуск асинхронного метода
async def get_url_async(session, semaphore, url: str, num: int):
    try:
        async with semaphore:
            logger.info(f'Запись запроса №: {num} началась')
            async with session.get(
                    url,
                    timeout=aiohttp.ClientTimeout(total=TIMEOUT)
                    ) as response:
                status = response.status
                logger.info(
                    f'Запрос №: {num} выполнился со статус кодом {status}'
                    )
                return status
    except aiohttp.ClientError as error:
        logger.error(f"Error received {error}")
        return None
    except asyncio.TimeoutError:
        logger.error(f"Запрос №: {num} превышено время запроса")
        return None
    except Exception as error:
        logger.error(
            f'Получена неизвестнная ошибка {error} на запросе №: {num}'
            )


async def main_async():
    start = time.perf_counter()
    semaphore = asyncio.Semaphore(SEMAPHORE)
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_url_async(
                session, semaphore,
                URL, i) for i in range(100)]
        results = await asyncio.gather(*tasks)

    count = 0
    for res in results:
        if res is not None and res < 400:
            count += 1

    elapsed = time.perf_counter() - start
    print(
        f'Успешно обработано {count} асинхронных запросов - за время {elapsed:.2f}'
        )

# Запуск синхроного метода
def get_url_sync(url: str, num: int, session):
    try:
        logger.info(f'Запись запроса №: {num} началась')
        response = session.get(url, timeout=TIMEOUT)
        status = response.status_code
        logger.info(f'Запрос № {num} - статус {status}')
        return status
    except requests.exceptions.ConnectionError:
        logger.error("Error received")
        return None
    except requests.exceptions.Timeout:
        logger.error(f"Запрос №: {num} превышено время запроса")
        return None
    except Exception as error:
        logger.error(
            f'Получена неизвестнная ошибка {error} на запросе №: {num}'
            )


def main_sync():
    start = time.perf_counter()
    with requests.Session() as session:
        results = [get_url_sync(URL, i, session) for i in range(100)]

    count = 0
    for res in results:
        if res is not None and res < 400:
            count += 1

    elapsed = time.perf_counter() - start
    print(
        f'Успешно обработано {count} синхронных запросов - за время {elapsed:.2f}'
        )

# Использование многопоточности
def get_url_threadpool(url: str, num: int):
    try:
        logger.info(f'Запись №:{num} началась')
        with requests.Session() as session:
            response = session.get(url, timeout=TIMEOUT)
        status = response.status_code
        logger.info(f'Запрос №{num} выполнен, статус: {status}')
        return status
    except requests.exceptions.ConnectionError:
        logger.error(f'Запрос №:{num} ошибка соединения')
        return None
    except requests.exceptions.Timeout:
        logger.error("Превышен время запроса №:{num}")
        return None
    except Exception as error:
        logger.error(
            f'Получена неизвестнная ошибка {error} на запросе №: {num}'
            )


def main_threadpool():
    start = time.perf_counter()

    urls = [(URL, i) for i in range(100)]

    with ThreadPoolExecutor(max_workers=SEMAPHORE) as executor:
        results = list(executor.map(
            lambda args: get_url_threadpool(*args),
            urls
        ))

    count = 0
    for res in results:
        if res is not None and res < 400:
            count += 1
    elapsed = time.perf_counter() - start

    print(
        f'Успешно обработано {count} синхронных запросов - за время {elapsed:.2f}'
        )


if __name__ == '__main__':
    main_sync()
    asyncio.run(main_async())
    main_threadpool()
