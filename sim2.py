# Leonardo Sole - GTA
#
print("importing libs..")
import math
import itertools
import random
from scipy.stats import nakagami
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import time
import numpy as np



class Car:
    def __init__(self, id, x, y):
        self.id = id
        self.x = x
        self.y = y
    def setDist(self, d):
        self.dist = d
class Time:
    def __init__(self, sec):
        self.sec = sec
        self.cars = []
    def countCars(self):
        return len(self.cars)
class Graphs:
    def __init__(self, carNum, cars):
        self.carNum = carNum
        self.cars = cars

def naka():
    a = nakagami.rvs(2)*radius
    if a > radius:
        return radius
    return a
def calcDist(pointA, pointB): # calculates de distance between two points
    aX, aY, bX, bY = pointA[0], pointA[1], pointB[0], pointB[1]

    xDiff = abs(aX - bX)
    yDiff = abs(aY - bY)

    return math.sqrt(xDiff**2 + yDiff**2)

def simulateCarsInReach(trace, bs, event, carsReached):
    total = trace.countCars()
    eventCoord = [trace.cars[event].x, trace.cars[event].y]
    for car in trace.cars: # first hop
        carDist = calcDist(eventCoord,[car.x, car.y])
        if carDist < naka() and carDist > 0 and car not in carsReached:
            car.setDist(carDist)
            carsReached.append(car)
    carNum = len(carsReached)
    multiReach = carNum
    carsReachedM = carsReached
    for car in trace.cars: # second hop
        for carR in carsReached:
            eventCoord = [carR.x, carR.y]
            carDist = calcDist(eventCoord,[car.x, car.y])
            if carDist < naka() and carDist > 0 and car not in carsReachedM:
                multiReach += 1
                carsReachedM.append(car)
    carsReached.insert(0, trace.cars[event])
    return [100*carNum/total, carsReached, 100*multiReach/total]

def simulateBSDelay(traces, bs, event):
    bsFound = False
    t = -1
    nearestBs = False
    while not bsFound:
        t += 1
        tempCar = findCarInTrace(traces[0].cars[event], traces[t])
        if tempCar:
            eventCoord = [tempCar.x, tempCar.y]
            for base in bs:
                currDist = calcDist(eventCoord, [base.x, base.y])
                if currDist < naka():
                    bsFound = True
                    nearestBS = base.id
        if t > 588:
            print("no base stations found in the time period [single]")
            return ['remove', False]
    return [t, nearestBS]

def findNearest(trace, bs, event):
    eventCoord = [trace.cars[event].x, trace.cars[event].y]
    nearDist = False
    nearest = None
    for base in bs:
        dist = calcDist(eventCoord, [base.x,base.y])
        if not nearDist or dist < nearDist:
            nearDist = dist
            nearest = base
    return nearest

def removeHighValues(vec):
    for el in vec:
        if el == 'remove':
            vec.remove(el)
    return vec

def carsInTime(event, traces):
    carsReached = []
    time = []
    for t in range(0, 120):
        tempCar = findCarInTrace(traces[0].cars[event], traces[t])
        if tempCar:
            eventCoord = [tempCar.x, tempCar.y]
            for car in traces[t].cars:
                carDist = calcDist(eventCoord,[car.x, car.y])
                if carDist < naka() and car.id not in carsReached:
                    carsReached.append(car.id)
                    time.append(t)
    return time

def baseReachTime(bs, traces):
    bsCoord = [bs.x, bs.y]
    carsReached = []
    time = []
    for t in range(0, 120):
        for car in traces[t].cars:
            carDist = calcDist(bsCoord,[car.x, car.y])
            if carDist < naka() and car.id not in carsReached:
                carsReached.append(car.id)
                time.append(t)
    return time

def baseReach(bs, trace):
    total = trace.countCars()
    bsCoord = [bs.x, bs.y]
    reach = 0
    for car in trace.cars:
        carDist = calcDist(bsCoord,[car.x, car.y])
        if carDist < naka():
            reach += 1
    return 100*reach/total

def simulateMultiBSDelay(traces, bs, cars):
    bsFound = False
    t = -1
    nearestBS = False
    while not bsFound:
        t += 1
        for car in cars:
            tempCar = findCarInTrace(car, traces[t])
            if tempCar and not bsFound:
                eventCoord = [tempCar.x, tempCar.y]
                for base in bs:
                    currDist = calcDist(eventCoord, [base.x, base.y])
                    if currDist < naka():
                        bsFound = True
                        nearestBS = base.id
            if t > 588:
                print("no base stations found in the time period [multi]")
                return ['remove', False]
    return [t, nearestBS]

def findCarInTrace(wantedCar, trace):
    for car in trace.cars:
        if car.id == wantedCar.id:
            return car
    return False

def readBS(file):
    bs = [] # list with base stations coordinates
    with open(file, "r") as bsFile:
        bsLines = bsFile.readlines()
        for i in range(0, len(bsLines)):
            temp = bsLines[i].split()
            base = Car(int(temp[0]), float(temp[1]), float(temp[2]))
            bs.append(base)
    return bs

def readTraces(txtFile):
    traces = [] # list with traces
    count = 0
    with open(txtFile, "r") as trFile:
        trLines = trFile.readlines()
        for line in trLines:
            temp = line.split()
            if count == 0:
                traces.append(Time(temp[0]))
                traces[0].cars.append(Car(temp[1], float(temp[2]), float(temp[3])))
                count = 1
            elif temp[0] == traces[-1].sec:
                traces[-1].cars.append(Car(temp[1], float(temp[2]), float(temp[3])))
            else:
                traces.append(Time(temp[0]))
                traces[-1].cars.append(Car(temp[1], float(temp[2]), float(temp[3])))
    return traces

def runSimulations(simNum, traces, bs, carsReached, timeSingle, timeMulti, multiReach, bsReach, carsList, multiList, carsinT, apReach):
    for n in range(0, simNum):
        print("{0}/{1}".format(n+1, simNum))
        event = random.randint(0,traces[n].countCars() - 1)
        base = findNearest(traces[n], bs, event)
        # apReach.append(baseReach(base, traces[n]))
        # carsinT += carsInTime(event, traces)
        # cars = []
        # temp = simulateCarsInReach(traces[0], bs, event, cars)
        # bsSingle = simulateBSDelay(traces, bs, event)
        # timeSingle.append(bsSingle[0])
        # bsMulti = simulateMultiBSDelay(traces, bs, temp[1])
        # timeMulti.append(bsMulti[0])
        # carsReached.append(temp[0])
        # multiReach.append(temp[2])
        # event2 = random.randint(0,len(bs) - 1)
        bsReach += baseReachTime(base, traces)
        # carsReachTime = []
        # for t in range(0, len(carsList)):
        #     print("{0}/{1}".format(t, len(carsList)))
        #     temp2 = simulateCarsInReach(traces[t], bs, event, carsReachTime)
        #     carsList[t] += temp2[0]/len(carsList)
        #     multiList[t] += temp2[2]/len(multiList)
def saveFile(filename, data):
    with open(filename, "w") as file:
        print("open "+filename)
        for el in data:
         file.write("{0}\n".format(el))

print("starting..")
start_time = time.process_time()
filenames = []
sufix = ["8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm"]
for i in range(0, len(sufix)):
    filenames.append(sufix[i]+".txt")
radius = 200
propSpeed = 299792458
print ("reading base stations")
bases = []
bases.append(readBS("bases/bs_246.txt"))
bases.append(readBS("bases/bs_500.txt"))
bases.append(readBS("bases/bs_1000.txt"))

carsList = [0] * 120
multiList = [0] * 120
id = [246, 500, 1000]
# id = [1000]
for bs, i in zip(bases, id):
    print("APs: {0}".format(i))
    timeSingle = []
    carsReached = []
    timeMulti = []
    multiReach = []
    bsReach = []
    carsinT = []
    apReach = []
    for file in filenames:
        print ("\nreading "+file)
        traces = []
        traces = readTraces(file)
        print("simulating")
        runSimulations(20, traces, bs, carsReached, timeSingle, timeMulti, multiReach, bsReach, carsList, multiList, carsinT, apReach)
        print("end of simulation from "+file)
    print("end simulation from AP: {0}".format(i))
    saveFile("APReachT_"+str(i)+".txt", bsReach)


print("end of simulations")

# carsReached = removeHighValues(carsReached)
# carsAvg = sum(carsReached)/len(carsReached)
# multiAvg = sum(multiReach)/len(multiReach)
# with open("carsReachSingle.txt", "w") as file:
#     print("open carsReachSingle.txt")
#     for el in carsReached:
#      file.write("{0}\n".format(el))
#
# with open("carsReachMulti.txt", "w") as file:
#     print("open carsReachMulti.txt")
#     for el in multiReach:
#      file.write("{0}\n".format(el))
#
# print("average reached cars: %.2f" % carsAvg)
# print("average reached cars [multi]: %.2f" % multiAvg)
#
# timeSingle = removeHighValues(timeSingle)
# timeMulti = removeHighValues(timeMulti)
# saveFile("delaySingle_"+str(i)+".txt", timeSingle)
# saveFile("delayMulti_"+str(i)+".txt", timeMulti)


# sAvg = sum(timeSingle)/len(timeSingle)
# mAvg = sum(timeMulti)/len(timeMulti)
# print("average delay: %.2f" % sAvg)
# print("average multi delay: %.2f" % mAvg)

# with open("reachInTime.txt", "w") as file:
#     print("open reachInTime.txt")
#     for el in carsList:
#      file.write("{0}\n".format(el))
#
# with open("reachMultiInTime.txt", "w") as file:
#     print("open reachMultiInTime.txt")
#     for el in multiList:
#      file.write("{0}\n".format(el))
#
# bsReach.sort()
# with open("bsReach.txt", "w") as bsFile:
#     print("open")
#     for el in bsReach:
#      bsFile.write("{0}\n".format(el))


print ("simulation time: {0} minutes".format((time.process_time() - start_time)/60))
