from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import requests
import time

A = [10**7, 20**7, 40**7, 50**7, 60**7]
B = [11**7, 22**7, 33**7, 44**7, 55**7]
URL = ['https://httpbin.org/delay/1',
       'https://httpbin.org/delay/2',
       'https://httpbin.org/delay/3',
       'https://httpbin.org/delay/4',
       'https://httpbin.org/delay/5',
       'https://httpbin.org/delay/6',
       'https://httpbin.org/delay/7',
       'https://httpbin.org/delay/8',
       'https://httpbin.org/delay/9']


def benchmark(name, func):
    start = time.perf_counter()
    result = func()
    elapsed = time.perf_counter() - start
    print(f'{name:<20} {elapsed:.2f} с')
    return result


def benchmark_cpu(a: int, b: int):
    result = 0
    for i in range(100000000):
        result += (a ** 2 + b ** 2) * i
    return result


def benchmark_I_O(url: str):
    response = requests.get(url)
    return response.status_code


if __name__ == '__main__':
    print('CPU-bound задания')
    benchmark('-Однопоточность', lambda: list(map(benchmark_cpu, A, B)))

    with ThreadPoolExecutor(max_workers=5) as executor:
        benchmark('-Многопоточность', lambda: list(executor.map(benchmark_cpu, A, B)))

    with ProcessPoolExecutor(max_workers=5) as executor:
        benchmark('-Многопроцессорность', lambda: list(executor.map(benchmark_cpu, A, B)))


    print('=' * 100)

    print('I/O-bound задания')
    benchmark('-Однопоточность', lambda: list(map(benchmark_I_O, URL)))

    with ThreadPoolExecutor(max_workers=5) as executor:
        benchmark('-Многопоточность', lambda: list(executor.map(benchmark_I_O, URL)))

    with ProcessPoolExecutor(max_workers=5) as executor:
        benchmark('-Многопроцессорность', lambda: list(executor.map(benchmark_I_O, URL)))
