'''The shoelace formula, also known as Gauss's area formula and the surveyor's formula,
is a mathematical algorithm to determine the area of a simple polygon whose vertices are described
by their Cartesian coordinates in the plane.'''
import re
import time

# polygon coordinates format: (45,110), (44, 23), (36, 20)

# to extract the points from input
PTS_REGEX = "\((\d*),(\d*)\)" # inner brackets separate groups of digits, to extract the X and Y in separate groups

def find_area(points_str):
    points = []
    area = 0.0
    for xy in re.finditer(PTS_REGEX, points_str):
        points.append((int(xy.group(1)), int(xy.group(2))))  # xy.group(1) and (2) we extract the first and the second group.

    #after the loop we have list of points
    for i in range(len(points)):
        a, b = points[i], points[(i+1) % len(points)]
        '''% len(points)   -   when i+1 goes past the last index of our points list, we wrap around 
        and go back to the first one and now we can use points A and B to do our calculation.'''
        area += a[0]*b[1] - a[1]*b[0]

    area = abs(area)/2
    #print(area)


f = open("polygons.txt", "r")
lines = f.read().splitlines()

start = time.time()
for line in lines:
    find_area(line)
end = time.time()
print("Time taken: ", end-start)