import time


def move_train(train, distance, crossings):  #crossings represent the positions of different intersections that we have along train's journey
    while train.front < distance:
        #While the train's position is less than the distance we need to travel, we move the train forward.
        train.front += 1
        # check that we are not in front of a crossing
        for crossing in crossings:
            if train.front == crossing.position:
                # if the front of the train is at the crossing that position,
                # we to try to acquire an exclusive look on that intersection.
                crossing.intersection.mutex.acquire()
                crossing.intersection.locked_by = train.uid # mark that that intersection is blocked by this particular train
            back = train.front - train.train_length #find the back position of our train.
            if back == crossing.position:
                # if that back position is equal to a particular crossing position, this means that we have moved past that intersection.
                crossing.intersection.locked_by = -1 #-1 to mark that this intersection is not being used anymore by this train.
                crossing.intersection.mutex.release()
        time.sleep(0.01) #to slow movement on the screen





