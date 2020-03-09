# Leonardo Sole - GTA
#
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
    carsReached = []
    farthestCar = -1
    for car in traces.cars:
        carDist = calcDist(eventCoord,[car.x, car.y])
        if carDist < radius:
            carsReached.append(car)
            if farthestCar < 0 or carDist > farthestCar:
                farthestCar = carDist
    bsDist = -1
    nearestBase = Car(0,0,0)
    for base in bs:
        currDist = calcDist(eventCoord, [base.x, base.y])
        if bsDist < 0 or currDist < bsDist:
            bsDist = currDist
            nearestBase = base
    bsFarthestCarDist = 0
    for car in carsReached:
        carDist = calcDist([nearestBase.x, nearestBase.y],[car.x, car.y])
        if carDist > bsFarthestCarDist:
            bsFarthestCarDist = carDist

    return [len(carsReached), bsDist, farthestCar, bsFarthestCarDist]

def readBS():
    bs = [] # list with base stations coordinates
    with open("koln_bs.txt", "r") as bsFile:
        bsLines = bsFile.readlines()
        for i in range(0, len(bsLines)):
            temp = bsLines[i].split()
            base = Car(temp[0], float(temp[1]), float(temp[2]))
            bs.append(base)
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
    cars, bsCarDist, bsDist, carDist = 0, 0, 0, 0
    for i in range(1, simNum):
        temp = simulateEvent(traces, bs)
        cars += temp[0]
        bsDist += temp[1]
        carDist += temp[2]
        bsCarDist += temp[3]
    avgCars = cars/simNum
    avgBSDist = bsDist/simNum
    avgCarDist = carDist/simNum
    avgBSCarDist = bsCarDist/simNum
    avgBSDelay = (avgBSDist+avgBSCarDist)/propSpeed
    avgDirectDelay = avgCarDist/propSpeed
    print("[averages after %i simulations]" % simNum)
    print("cars reached:\t\t\t %.2f" % avgCars)
    print("nearest base station distance:\t %.2f" % avgBSDist)
    print("direct communication delay:\t", "{:.2e}".format(avgDirectDelay))
    print("internet communication delay:\t", "{:.2e}".format(avgBSDelay))
    print("delay ratio:\t\t\t %.2f" % (avgBSDelay/avgDirectDelay))

radius = 200
propSpeed = 299792458
bs = readBS()
traces = readTraces()
runSimulations(traces[0], bs, 1000)
