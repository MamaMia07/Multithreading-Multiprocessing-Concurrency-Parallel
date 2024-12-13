from threading import Thread, Lock

#
from arbitrator.train import *
from draw_trains import *
from model import *



train_length = 200

def main():
    win = GraphWin('Train in a box', 800, 800) #title and dimensions
    win.setBackground('black')
    train_anim = TrainAnim(win, train_length)


    trains = []
    intersections = []
    for i in range(4):
        trains.append(Train(i, train_length, 0))

    for i in range(4):
        intersections.append(Intersection(i, Lock(), -1))

    t1 = Thread(target=move_train,
                   args=(trains[0], 700, [Crossing(320, intersections[0]), Crossing(460, intersections[1])]))

    t2 = Thread(target=move_train,
                args=(trains[1], 700, [Crossing(320, intersections[1]), Crossing(460, intersections[2])]))

    t3 = Thread(target=move_train,
                args=(trains[2], 700, [Crossing(320, intersections[2]), Crossing(460, intersections[3])]))

    t4 = Thread(target=move_train,
                args=(trains[3], 700, [Crossing(320, intersections[3]), Crossing(460, intersections[0])]))

    t1.start()
    t2.start()
    t3.start()
    t4.start()

    while True:
        train_anim.update_trains(trains, intersections)
        time.sleep(0.01)

main()