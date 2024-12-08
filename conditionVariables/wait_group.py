from threading import Condition


class WaitGroup():
    wait_count = 0 # count the number of active threats( number of threads we wait for them to finish)
    cv = Condition()


    def add(self, count):
        self.cv.acquire() #protected so that multiple threads that are accessing the same variable do not overwrite each other.
        self.wait_count += count
        self.cv.release()

    # This will be called by threads once they're finished with the work.
    # done operation  signals that a threat is done from its work.
    def done(self):
        self.cv.acquire()
        if self.wait_count > 0:
            self.wait_count -= 1
        if self.wait_count == 0: #if there is no working thread
            self.cv.notify_all() # notify all, notifies all the threads that are currently waiting on that condition variable
        self.cv.release()

    # wait()  - the main threat will call to wait on all the other threads to finish their work.
    # wait operation will block the calling thread until all of the work is done
    def wait(self):
        self.cv.acquire()
        # in while loop because we need to check again every time we are awaken from the condition variable.
        #in case that just before our tread is woken up, another thread comes in and adds more work to the wait group.
        while self.wait_count > 0: # we need to wait for more threads to finish what they're doing, we need to do a conditional variable that wait.
            self.cv.wait() #blocks the execution of the current thread and releases the associated lock
        self.cv.release()