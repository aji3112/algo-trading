import time
import threading

list_args = [1,2,3,4,5,6,7,8,9,10]

def countdown(n):
    a = n
    while n > 0:
        print('{} T-minus {} current thread name {}'.format(a, n, threading.current_thread().name))
        n -= 1
        time.sleep(5)


# Create and launch a thread
threads = []
for arg in list_args:
    t = threading.Thread(target=countdown, args=(arg,))
    t.start()
    threads.append(t)

for thread in threads:
    thread.join()

exit()