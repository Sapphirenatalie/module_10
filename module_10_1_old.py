# Напишите программу, которая создает два потока.
# Первый поток должен выводить числа от 1 до 10 с интервалом в 1 секунду.
# Второй поток должен выводить буквы от 'a' до 'j' с тем же интервалом.
# Оба потока должны работать параллельно.
# Примечание:
# Используйте методы: start() для старта потока,
# join() для заморозки дальнейшей интерпретации, пока процессы не завершаться.
# Для установки интервала в 1 секунду используйте функцию sleep() из модуля time,
# предварительно импортировав его.

from threading import Thread
import threading
import time
from datetime import datetime

lock = threading.RLock()


def output_numbers():
    for number in range(1, 10 + 1):
        with lock:
            time.sleep(1)
        print(number)


def output_letters():
    for letter in ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']:
        with lock:
            time.sleep(1)
        print(letter)


time_start = datetime.now()

flow_1 = Thread(target=output_numbers)
flow_2 = Thread(target=output_letters)
flow_1.start()
flow_2.start()
flow_1.join()
flow_2.join()

time_end = datetime.now()

duration_time = time_end - time_start
print(duration_time)

# Выходные данные:
# 1
# a
# 2
# b
# 3
# c
# 4
# d
# 5
# e
# 6
# f
# 7
# g
# 8
# h
# 9
# i
# 10
# j
# 0:00:20.009822
