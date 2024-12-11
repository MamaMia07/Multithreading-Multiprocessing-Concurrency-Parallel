import re
import time
from multiprocessing import Process,Queue
#from queue import Queue !!DO NOT use normal Queue for multiprocessisng!!!!


# polygon coordinates format: (45,110), (44, 23), (36, 20)

# to extract the points from input
PTS_REGEX = "\((\d*),(\d*)\)" # inner brackets separate groups of digits, to extract the X and Y in separate groups
TOTAL_PROCESSES = 4 # number of all processes, eual to nmb. of cores in computer


'''area function will accept a list of points from the queue, 
the cube between the master and the worker threads'''
def find_area(points_queue):
    points_str = points_queue.get()
    while points_str is not None:
        points = []
        area = 0.0
        for xy in re.finditer(PTS_REGEX, points_str):
            points.append((int(xy.group(1)), int(xy.group(2))))  # xy.group(1) and (2) we extract the first and the second group.
        #after the loop we have list of points
        for i in range(len(points)):
            a, b = points[i], points[(i+1) % len(points)]
            '''% len(points)   -   when i+1 goes past the last index of our points list, we wrap around 
            and go back to the first one and now we can use points A and B to do our calculation.'''
            area += a[0]*b[1] - a[1]*b[0]
        area = abs(area)/2
        points_str = points_queue.get()


if __name__ == "__main__":
    queue = Queue(maxsize=1000)
    processes = []  # list which will contain all of our processes.
    for i in range(TOTAL_PROCESSES):
        p = Process(target=find_area, args = (queue,))
        processes.append(p)
        p.start()
    f = open("polygons.txt", "r")
    lines = f.read().splitlines()
    start = time.time()
    for line in lines:
        queue.put(line) # put the line containing the list of points.
    for _ in range(TOTAL_PROCESSES): queue.put(None) # to signal all our worker processes that we have finished the work
    for p in processes: p.join()  # to know when the process terminates
    #use the join() function to know whether a trade has terminated or not.This will return once the process has terminated.
    end = time.time()
    print("Time taken: ", end-start)