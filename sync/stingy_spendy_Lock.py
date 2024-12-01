import time
from threading import Thread, Lock

class StingySpendy:
    money = 100
    mutex = Lock()

    def stingy(self):
        for i in range(5000000):
            self.mutex.acquire() #lock the mutex
            self.money +=0.5
            self.mutex.release()
        print("Stingy done")

    def spendy(self):
        for i in range(5000000):
            self.mutex.acquire()
            self.money -= 0.5
            self.mutex.release()
        print("Spendy done")

ss= StingySpendy()
Thread(target=ss.stingy, args=()).start()
Thread(target=ss.spendy, args=()).start()

time.sleep(5)
print("Money in the end: ", ss.money)