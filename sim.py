# Leonardo Sole - GTA
#
import utm
import math
import itertools
import random

def calcDist(pointA, pointB): # calculates de distance between two points
    aX, aY, bX, bY = pointA[0], pointA[1], pointB[0], pointB[1]

    xDiff = abs(aX - bX)
    yDiff = abs(aY - bY)

    return math.sqrt(xDiff**2 + yDiff**2)

def createSmallFile(firstLine, lastLine): # 99239748, 99260777 -> lines to create 8am file with 2 seconds
    with open("koln_traces.tr", "r") as traceFile:
        with open("koln_traces8am.txt", "w") as smallTrace:
            for line in itertools.islice(traceFile, firstLine, lastLine):
                smallTrace.write(line)

class Car:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y

class Time:
    def __init__(self, sec):
        self.sec = sec
    cars = []
    def countCars(self):
        return len(self.cars)

def simulateEvent(traces, bs):
    event = random.randint(0,traces.countCars())
    eventCoord = [traces.cars[event].x, traces.cars[event].y]
    carsReached = -1
    bsReached = 0
    for car in traces.cars:
        if calcDist(eventCoord,[car.x, car.y]) < radius:
            carsReached += 1
    for base in bs:
        if calcDist(eventCoord, base) < radius:
            bsReached += 1
    # print("cars: ",carsReached)
    # print("bs: ",bsReached)
    return [carsReached, bsReached]

radius = 100

# BASE STATIONS
bs = [] # list with base stations coordinates
with open("koln_bs.txt", "r") as bsFile:
    bsLines = bsFile.readlines()
    for i in range(0, len(bsLines)):
        temp = bsLines[i].split()
        del temp[0]
        temp[0] = float(temp[0])
        temp[1] = float(temp[1])
        bs.append(temp)

# TRACES
traces = [] # list with traces
count = 0
with open("koln_traces8am.txt", "r") as trFile:
    trLines = trFile.readlines()
    for line in trLines:
        temp = line.split()
        if count == 0:
            traces.append(Time(temp[0]))
            traces[0].cars.append(Car(temp[1], float(temp[2]), float(temp[3])))
            count = 1
        elif temp[0] == traces[count - 1].sec:
            traces[0].cars.append(Car(temp[1], float(temp[2]), float(temp[3])))
        elif count == 1:
            traces.append(Time(temp[0]))
            traces[1].cars.append(Car(temp[1], float(temp[2]), float(temp[3])))
            count = 2
sums = [0, 0]
for i in range(1, 1000):
    temp = simulateEvent(traces[1], bs)
    sums[0] += temp[0]
    sums[1] += temp[1]
print("cars mean: ",sums[0]/1000)
print("bs mean: ",sums[1]/1000)
