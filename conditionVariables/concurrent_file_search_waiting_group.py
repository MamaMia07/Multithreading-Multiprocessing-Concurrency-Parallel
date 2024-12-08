import os
from threading import Lock, Thread
from os.path import isdir, join

from wait_group import WaitGroup

mutex = Lock()
matches = []

def file_search(root, filename, wait_group):
    print("Searching in: ", root)
    for file in os.listdir(root):
        full_path = join(root, file)
        if filename in file:
            mutex.acquire() #before global variable, all threads modify matches[]
            matches.append(full_path)
            mutex.release()

        if isdir(full_path):
            wait_group.add(1)
            t = Thread(target=file_search, args=([full_path, filename,wait_group]))
            t.start()
    wait_group.done()


def main():
    wait_group = WaitGroup()
    wait_group.add(1) #adding first thread 9created below)
    t = Thread(target = file_search, args=(["C:/Users/UPWr/MAGDA/IGiG", "fdgggr.txt", wait_group]))
    t.start()
    wait_group.wait() #main thread will be waiting on this function and it's only once this function returns that we are sure that this search operation has finished.
    for m in matches:
        print("Matched: ", m)

main()