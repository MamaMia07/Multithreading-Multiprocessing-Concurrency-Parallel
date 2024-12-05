import json
import urllib.request
import time
from threading import Thread, Lock
'''
fixed multithreaded program 'counting_letters' and made use of tred synchronization.
using mutex locks to solve all of our race conditions.
'''
finished_count=0

def count_letters(url, frequency, mutex):
    response = urllib.request.urlopen(url)
    txt = str(response.read())
    mutex.acquire() # before loop, not before a letter
    for l in txt:
        letter = l.lower()
        if letter in frequency:
            frequency[letter] += 1
    global finished_count
    finished_count += 1
    mutex.release() # protect global counter (used by all threads)


def with_threading():
    frequency = {}
    mutex = Lock()
    for c in "abcdefghijklmnoprqstuwxyz":
        frequency[c] = 0
    start = time.time()
    for i in range(1000, 1050):
        Thread(target=count_letters, args=(f"https://www.rfc-editor.org/rfc/rfc{i}.txt", frequency, mutex)).start()

    while True:
        mutex.acquire()  # reading shared variable - protect finished_count with lock()
        if finished_count == 50:
            break
        mutex.release()
        time.sleep(0.5)

    end = time.time()
    print(json.dumps(frequency, indent=4))
    print("Done, time taken: ", end - start)
    print(finished_count)


def main():
    with_threading()


main()