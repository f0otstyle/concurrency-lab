import asyncio
import aiohttp
import time
import logging

TIMEOUT = 15
SEMAPHORE = 5

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='async_client.log',
    encoding='utf-8',
    filemode='a',
)

logger = logging.getLogger('async_client')


async def get_url(session, semaphore, url: str, num: int):
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


async def main():
    start = time.perf_counter()
    semaphore = asyncio.Semaphore(SEMAPHORE)
    async with aiohttp.ClientSession() as session:
        tasks = [
            get_url(
                session, semaphore,
                'http://localhost:8000/delay/1', i) for i in range(50)]
        results = await asyncio.gather(*tasks)

    count = 0
    for res in results:
        if res is not None and res < 400:
            count += 1

    elapsed = time.perf_counter() - start
    print(
        f'Успешно обработано {count} асинхронных запросов - за время {elapsed:.2f}'
        )

if __name__ == '__main__':
    asyncio.run(main())
