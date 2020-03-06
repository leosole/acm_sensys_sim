# Leonardo Sole - GTA
#
import utm
import math
import itertools
import random

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

def simulateEvent(traces, bs):
    event = random.randint(0,traces.countCars())
    eventCoord = [traces.cars[event].x, traces.cars[event].y]
    carsReached = -1
    avgCarDist = 0
    for car in traces.cars:
        carDist = calcDist(eventCoord,[car.x, car.y])
        if carDist < radius:
            carsReached += 1
            avgCarDist += carDist
    avgCarDist = avgCarDist/carsReached
    bsReached = 0
    bsDist = -1
    for base in bs:
        currDist = calcDist(eventCoord, base)
        if currDist < radius:
            bsReached += 1
        if bsDist < 0 or currDist < bsDist:
            bsDist = currDist
    return [carsReached, bsReached, bsDist, avgCarDist]

def readBS():
    bs = [] # list with base stations coordinates
    with open("koln_bs.txt", "r") as bsFile:
        bsLines = bsFile.readlines()
        for i in range(0, len(bsLines)):
            temp = bsLines[i].split()
            del temp[0]
            temp[0] = float(temp[0])
            temp[1] = float(temp[1])
            bs.append(temp)
    return bs

def readTraces():
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
    return traces

def runSimulations(traces, bs, simNum):
    cars, bases, bsDist, carDist = 0, 0, 0, 0
    for i in range(1, simNum):
        temp = simulateEvent(traces, bs)
        cars += temp[0]
        bases += temp[1]
        bsDist += temp[2]
        carDist += temp[3]
    avgCars = cars/simNum
    avgBases = bases/simNum
    avgBSDist = bsDist/simNum
    avgBSDelay = avgBSDist*2/propSpeed
    avgCarDist = carDist/simNum
    avgDirectDelay = avgCarDist/propSpeed
    print("cars avg: ", avgCars)
    print("bs avg: ", avgBases)
    print("bs distance avg: ", avgBSDist)
    print("direct delay avg: ", avgDirectDelay)
    print("bs delay avg: ", avgBSDelay)

radius = 200
propSpeed = 300000000
bs = readBS()
traces = readTraces()
runSimulations(traces[0], bs, 100)
