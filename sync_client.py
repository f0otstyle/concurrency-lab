import requests
import time
import logging

TIMEOUT = 10

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='sync_client.log',
    encoding='utf-8',
    filemode='a',
)

logger = logging.getLogger('sync_client')


def get_url(url: str, num: int, session):
    try:
        logger.info(f'Запись запроса №:{num} началась')
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


def main():
    start = time.perf_counter()
    with requests.Session() as session:
        results = [get_url('http://localhost:8000/blocking/1', i, session) for i in range(50)]

    count = 0
    for res in results:
        if res is not None and res < 400:
            count += 1

    elapsed = time.perf_counter() - start
    print(
        f'Успешно обработано {count} синхронных запросов - за время {elapsed:.2f}'
        )


if __name__ == '__main__':
    main()
