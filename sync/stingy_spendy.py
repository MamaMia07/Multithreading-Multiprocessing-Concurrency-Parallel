import time
from threading import Thread

class StingySpendy:
    money = 100

    def stingy(self):
        for i in range(5000000):
            self.money +=0.5
        print("Stingy done")

    def spendy(self):
        for i in range(5000000):
            self.money -= 0.5
        print("Spendy done")

ss= StingySpendy()
Thread(target=ss.stingy, args=()).start()
Thread(target=ss.spendy, args=()).start()

time.sleep(5)
print("Money in the end: ", ss.money)