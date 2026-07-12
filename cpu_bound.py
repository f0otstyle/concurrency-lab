from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
import time


def sumtwosquare(a: int, b: int):
    result = 0
    for i in range(1000000):
        result = (a ** 2 + b ** 2) * 2
    return result


def request_url(url: str):
    response = requests.get(url)
    return response.status_code


if __name__ == '__main__':
    print('CPU-bound задания')
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        a = [10**7, 20**7, 40**7, 50**7, 60**7]
        b = [11**7, 22**7, 33**7, 44**7, 55**7]
        results = executor.map(sumtwosquare, a, b)

    print('-Многопорточность-')
    for res in results:
        print(res)

    print(f'Время выполнения {time.time() - start_time}')

    print('-' * 100)

    start_time = time.time()
    with ProcessPoolExecutor(max_workers=5) as executor:
        a = [10**7, 20**7, 40**7, 50**7, 60**7]
        b = [11**7, 22**7, 33**7, 44**7, 55**7]
        results = executor.map(sumtwosquare, a, b)

    print('-Многопроцессорность-')
    for res in results:
        print(res)

    print(f'Время выполнения {time.time() - start_time}')

    print('=' * 100)

    print('I/O-bound задания')
    start_time = time.time()
    with ThreadPoolExecutor(max_workers=5) as executor:
        url = ['https://httpbin.org/delay/1',
               'https://httpbin.org/delay/2',
               'https://httpbin.org/delay/3']
        results = executor.map(request_url, url)

    print('-Многопорточность-')
    for res in results:
        print(res)

    print(f'Время выполнения {time.time() - start_time}')

    print('-' * 100)

    start_time = time.time()
    with ProcessPoolExecutor(max_workers=5) as executor:
        url = ['https://httpbin.org/delay/1',
               'https://httpbin.org/delay/2',
               'https://httpbin.org/delay/3']
        results = executor.map(request_url, url)

    print('-Многопроцессорность-')
    for res in results:
        print(res)

    print(f'Время выполнения {time.time() - start_time}')
