import time
from threading import Thread


def do_work():
    print("starting work")
    time.sleep(1)
    print("Finished work")

def do_work2(): #CPU bound function
    print("starting work")
    i=0
    for _ in range(20000000):
        i+=1
    print("Finished work")

for _ in range(5):
    t = Thread(target=do_work2, args=())
    t.start()