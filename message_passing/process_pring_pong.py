import time
from multiprocessing import Process, Pipe

def ping(pipe_conn):
    while True:
        pipe_conn.send(["ping", time.time()])
        pong = pipe_conn.recv()
        print(pong)
        time.sleep(1)

def pong(pipe_conn):
    while True:
        ping = pipe_conn.recv()
        print(ping)
        time.sleep(2)
        pipe_conn.send(["pong", time.time()])

if __name__ == '__main__':
    pipe_end_a, pipe_end_b = Pipe()
    Process(target= ping, args=(pipe_end_a,)).start()
    Process(target= pong, args=(pipe_end_b,)).start()
