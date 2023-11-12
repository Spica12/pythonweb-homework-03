import time
from multiprocessing import Process, Pipe
import sys

def measure_time(func):

    def inner(*args, **kwargs):
        times = []

        for _ in range(10):
            start_time = time.perf_counter()       
            result= func(*args, **kwargs)
            stop_time = time.perf_counter()
            delta_time = stop_time - start_time
            times.append(delta_time)

            
        avg_time = sum(times) / len(times)
        print(f'Total average time:{func.__name__} - {round(avg_time, 4)} s')

        return result
    
    return inner



def factorize(*numbers):
    total_result= list()
    for number in numbers:
        result = list()

        for i in range(1, number+1):

            if number % i == 0:
                result.append(i)
        
        total_result.append(result)

    return total_result


def sync_test(numbers, test=10):
    times = []

    for i in range(test):
        start_time = time.perf_counter()       
        result = factorize(*numbers)
        stop_time = time.perf_counter()
        delta_time = stop_time - start_time
        times.append(delta_time)
        # print(f'Test_{i} -  Sync time: {round(delta_time, 4)} s')

    avg_time = sum(times) / len(times)
    print(f'Average -  Sync time: {round(avg_time, 4)} s')
    return result


def process_test(*numbers):
    total_result = list()

    process = []
    for number in numbers:
        
        pr = Process(target=factorize, args=(numbers, ))





def check_answers(a, b, c, d):
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    list_numbers = [128, 255, 99999, 10651060]

    a, b, c, d  = sync_test(list_numbers)
    check_answers(a, b, c, d)




