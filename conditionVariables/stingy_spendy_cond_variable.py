import time
from threading import Thread, Condition


class StingySpendy:
    money = 100
    cond_var = Condition() #condition variable.

    def stingy(self):
        for i in range(100000):
            self.cond_var.acquire() #lock the mutex
            self.money +=10
            self.cond_var.notify() # the signal function when we have more money. we are simply notifying that there is more money in the bank account.
                                   # when it puts more money in our bank account, we need to call and notify on the condition variable
                                     # then if I will signal any waiting thread that their condition might not be valid anymore.
                                    #thread with Spendy should check if the condition holds or not anymore.
            self.cond_var.release()
        print("Stingy done")

    def spendy(self):
        for i in range(50000):
            self.cond_var.acquire()
            while self.money < 20:
                self.cond_var.wait() # wait if there isn't enough money on the bank account.
                                    #it will wait Until someone signals that the condition might not hold anymore.
            self.money -= 20
            if self.money < 0 :
                print("Money in the bank: ", self.money)
            self.cond_var.release()
        print("Spendy done")

ss= StingySpendy()
Thread(target=ss.stingy, args=()).start()
Thread(target=ss.spendy, args=()).start()

time.sleep(5)
print("Money in the end: ", ss.money)