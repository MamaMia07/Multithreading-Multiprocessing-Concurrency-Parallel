import time
#from queue import Queue #
# !! because we use queue to communicate between processes, CAN NOT use normal Queue, must import it from multoprocessing
from multiprocessing import Process, Queue

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

if __name__ == "__main__":
    q = Queue(maxsize=10) #maxsize - capacity of queue
    p1 = Process(target= consumer, args = (q,i))
    p2 = Process(target= producer, args = (q,j))
    p1.start()
    p2.start()
