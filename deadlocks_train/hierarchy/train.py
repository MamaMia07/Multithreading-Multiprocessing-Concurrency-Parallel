import time
'''Use orderings on locks and resources to avoid deadlocks.
   In Hierarchy, you need to know in advance which locks you are going to use.'''


'''-use ordering on how we can lock the different intersections in our launcher
   -lock the different intersections in advance according to train length.
'''
def lock_intersections_in_distance(id, reserve_start, reserve_end, crossings):
    # accepted parameters: id of train locking intersections,
        #reserve_starts the position along the tracks where we want to start reserving all the crossings
        # and the reserve_end - the position on the tracks where we want to stop reserving these intersections.

    intersections_to_lock = [] #list with all the intersections that are in that reserve_start and reserve_end.
    for crossing in crossings:
        if reserve_end >= crossing.position >= reserve_start and crossing.intersection.locked_by != id:
            intersections_to_lock.append(crossing.intersection)
    #after we exit this loop, we have a list of intersections that we need to acquire.

    # sort these intersections
    #this will cause the intersections to lock list to be sorted by the intersection id.
    intersections_to_lock = sorted(intersections_to_lock, key=lambda it: it.uid)


    # in implementation without ordering these intersections, the deadlock will still occur.
    for intersection in intersections_to_lock:
        intersection.mutex.acquire()
        intersection.locked_by = id
        time.sleep(0.01) # it's ONLY to increase the chances of the deadlock happening

def move_train(train, distance, crossings):  #crossings represent the positions of different intersections that we have along train's journey
    while train.front < distance:
        #While the train's position is less than the distance we need to travel, we move the train forward.
        train.front += 1
        # check that we are not in front of a crossing
        for crossing in crossings:
            if train.front == crossing.position:
                # if the front of the train is at the crossing that position,
                lock_intersections_in_distance(train.uid, crossing.position,
                                               crossing.position+train.train_length, crossings)
            back = train.front - train.train_length #find the back position of our train.
            if back == crossing.position:
                # if that back position is equal to a particular crossing position, this means that we have moved past that intersection.
                crossing.intersection.locked_by = -1 #-1 to mark that this intersection is not being used anymore by this train.
                crossing.intersection.mutex.release()
        time.sleep(0.01) #to slow movement on the screen





