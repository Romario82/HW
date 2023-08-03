from datetime import datetime
from multiprocessing import Process

def factorize(number):
    start_time = datetime.now()
    res = []
    for i in range(1, (number // 2) + 1):
        if number % i == 0:
            res.append(i)
    res.append(number)
    end_time = datetime.now()
    print(res, '-> time: ', end_time - start_time)

#------------------------------
if __name__ == '__main__':
    numbers = [128, 255, 99999, 10651060]
    processing = []

    for index, number in enumerate(numbers):
        proc = Process(target=factorize, args=(number,))
        processing.append(proc)
        proc.start()

    for proc in processing:
        proc.join()

