import multiprocessing
from multiprocessing import Process


def do_work(n): #CPU bound function
    print("starting work  ",n)
    i=0
    for _ in range(200000000):
        i+=1
    print("Finished work  ", n)


if __name__ == '__main__':
    '''multiprocessing rozdziela procesy na procesowy.
    if - ten warunek jest bo przu multiprocesach kazdy z procesow dziala w oddzielnym
    interpreterze, kazdy bedzie wykonywql kod, ktory pozostawimy
    poza funkcja'''
    multiprocessing.set_start_method('spawn') #metoda spawn jest domyslna
    for n in range(5):
        p = Process(target = do_work, args=(n,))
        p.start()

