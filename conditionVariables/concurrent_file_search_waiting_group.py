import os
from threading import Lock, Thread
from os.path import isdir, join

from wait_group import WaitGroup

mutex = Lock()
matches = []

def file_search(root, filename):
    print("Searching in: ", root)
    child_threads = []
    for file in os.listdir(root):
        full_path = join(root, file)
        if filename in file:
            mutex.acquire() #before global variable, alll threads modify matches[]
            matches.append(full_path)
            mutex.release()

        if isdir(full_path):
            t = Thread(target=file_search, args=([full_path, filename]))
            t.start()
            # here without t.join() because we do not want to wait for wait for each directory  to complete
                # its search before we search through another one, meaning that our search would not really be parallel.
            child_threads.append(t) #put all threads on the list and then ...
    for t in child_threads: # ... wait for all threads to complete
            t.join()


def main():
    wait_group = WaitGroup()
    wait_group.add(1)
    t = Thread(target = file_search, args=(["C:/Users/UPWr/MAGDA/IGiG", "fdgggr.txt"]))
    t.start()
    t.join()
    for m in matches:
        print("Matched: ", m)

main()