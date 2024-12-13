import threading
import time

'''use a conditional variable to implement arbitrator - 
   controller is the conditional variable '''
controller = threading.Condition()

# function that checks if the intersection that we want to use are free or not
def all_free(intersections_to_lock):
        #accepting a list of intersections to lock
    for it in intersections_to_lock:
        if it.locked_by >0: # it.locked_by > 0 means thah this intersection is beeing used
            return False
    return True #this function returns True, if all those intersections are free to be used

def lock_intersections_in_distance(id, reserve_start, reserve_end, crossings):
    # accepted parameters: id of train locking intersections,
        #reserve_starts the position along the tracks where we want to start reserving all the crossings
        # and the reserve_end - the position on the tracks where we want to stop reserving these intersections.

    intersections_to_lock = [] #list with all the intersections that are in that reserve_start and reserve_end.
    for crossing in crossings:
        if reserve_end >= crossing.position >= reserve_start and crossing.intersection.locked_by != id:
            intersections_to_lock.append(crossing.intersection)
    #after we exit this loop, we have a list of intersections that we need to acquire.

    controller.acquire()  # so that no other trade enters this part of the code while we are trying to lock all of these intersections together.
    while not all_free(intersections_to_lock):
        controller.wait() #as long as there is at least one intersection that we want to lock that is not free,
                             # we have to wait for it to become free.
        #when a thread enters this wait state, it releases this controller mutex,
        # this will allow another track to acquire this mutex and possibly broadcast that intersection has become available.

    for intersection in intersections_to_lock:
        intersection.locked_by = id
        time.sleep(0.01) # it's ONLY to increase the chances of the deadlock happening
    controller.release()


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
                controller.acquire()
                crossing.intersection.locked_by = -1 #-1 to mark that this intersection is not being used anymore by this train.
                controller.notify_all()
                controller.release()
        time.sleep(0.01) #to slow movement on the screen





