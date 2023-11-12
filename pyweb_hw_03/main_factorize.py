import time
from multiprocessing import Process, Queue, Pool, current_process, cpu_count
import sys


def measure_time(func):

    def inner(*args, **kwargs):

        start_time = time.perf_counter()  
        result = func(*args, **kwargs)
        stop_time = time.perf_counter()
        delta_time = stop_time - start_time
        print(f'Total time: {func.__name__} - {round(delta_time, 4)} s')

        return result
    
    return inner


def factorize(number):
    result = list()
    for i in range(1, number+1):
        if number % i == 0:
            result.append(i)

    return result


@measure_time
def sync_test(*numbers):
    total_result= list()
    for number in numbers:
        result = factorize(number)
        total_result.append(result)

    return total_result


def process_factorize(q_rcv: Queue, q_snd: Queue):
    number = q_rcv.get()
    result = list()
    for i in range(1, number+1):
        if number % i == 0:
            result.append(i)
    
    q_snd.put(result)


@measure_time
def process_test(*numbers):
    total_result = list()

    q_snd = Queue()
    q_rcv = Queue()

    processes = []

    for number in numbers:
        
        pr = Process(target=process_factorize, args=(q_snd, q_rcv))
        processes.append(pr)

        pr.start()
        q_snd.put(number)

    [pr.join() for pr in processes]
    total_result = [q_rcv.get() for _ in processes]

    return total_result


@measure_time
def pool_process_test(*numbers):
    print(f"Count CPU: {cpu_count()}; numbers: {numbers}")

    with Pool(cpu_count()) as pool:
        result = pool.map(factorize, numbers)

    return result


def check_answers(a, b, c, d):
    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]


if __name__ == '__main__':
    print('Start compare sync work and process work')

    list_numbers = [128, 255, 99_999, 10_651_060]
    print(f"Compute next numbers: {list_numbers}")

    print('---- Sync test ----')
    a, b, c, d = sync_test(*list_numbers)
    check_answers(a, b, c, d)

    print('---- Process test ----')
    a, b, c, d = process_test(*list_numbers)
    check_answers(a, b, c, d)

    print('---- Pool process test ----')
    a, b, c, d  = pool_process_test(*list_numbers)
    check_answers(a, b, c, d)

    # Start compare sync work and process work
    # Compute next numbers: [128, 255, 99999, 10651060]
    # ---- Sync test ----
    # Total time: sync_test - 0.8198 s
    # ---- Process test ----
    # Total time: process_test - 0.8582 s
    # ---- Pool process test ----
    # Count CPU: 6; numbers: (128, 255, 99999, 10651060)
    # Total time: pool_process_test - 0.8514 s

    print('Test with very long numbers')
    long_numbers = [100_000_000, 200_000_000, 400_000_000, 300_000_000, 150_000_000, 50_000, 135_000_000]


    print('Very long numbers test: sync test')
    sync_test(*long_numbers)

    print('Very long numbers test: process test')
    process_test(*long_numbers)

    print('Very long numbers test: pool process test')
    pool_process_test(*long_numbers)

    # Result:
    # Test with very long numbers
    # Very long numbers test: sync test
    # Total time: sync_test - 92.3915 s
    # Very long numbers test: process test
    # Total time: process_test - 58.9367 s
    # Very long numbers test: pool process test
    # Count CPU: 6; numbers: (100000000, 200000000, 400000000, 300000000, 150000000, 50000, 135000000)
    # Total time: pool_process_test - 36.8177 s


    


