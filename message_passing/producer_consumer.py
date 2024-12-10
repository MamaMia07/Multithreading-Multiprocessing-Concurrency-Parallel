import time
from queue import Queue
from threading import Thread
i = 0
def consumer(q, i):
    while True:
        txt = q.get()
        i +=1
        print(i, "  ", txt)
        time.sleep(1)

j = 0
def producer(q, j):
    while True:
        j +=1
        q.put(str(j) + "  Hello there")
        print(str(j) + " Message sent")
        #time.sleep(1)

q = Queue(maxsize=10) #maxsize - capacity of queue
t1 = Thread(target= consumer, args = (q,i))
t2 = Thread(target= producer, args = (q,j))
t1.start()
t2.start()
