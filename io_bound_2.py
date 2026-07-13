import requests
import time
import logging

STATUS = [404, 503, 403]
TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='io_bound.log',
    encoding='utf-8',
    filemode='a',
)

logger = logging.getLogger('io_bound')


def get_url(url: str, num: int):
    try:
        logger.info('Запись началась')
        response = requests.get(url, timeout=TIMEOUT)
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
            f'Получена не известнная ошибка {error} на запросе №: {num}'
            )


def main():
    start = time.perf_counter()
    results = [get_url(f'https://httpbin.org/delay/{i}', i) for i in range(10)]

    count = 0
    for res in results:
        if res is not None and res not in STATUS:
            count += 1

    elapsed = time.perf_counter() - start
    print(
        f'Успешно обработано {count} синхронных запросов - за время {elapsed:.2f}'
        )


if __name__ == '__main__':
    main()
