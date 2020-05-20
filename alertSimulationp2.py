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

simuTime = 600

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
        if carDist < naka() and carDist > 0 and car.id not in carsReached:
            car.setDist(carDist)
            carsReached.append(car.id)
    carNum = len(carsReached)
    multiReach = carNum
    carsReachedM = carsReached
    for car in trace.cars: # second hop
        for carR in carsReached:
            eventCoord = [carR.x, carR.y]
            carDist = calcDist(eventCoord,[car.x, car.y])
            if carDist < naka() and carDist > 0 and car.id not in carsReachedM:
                multiReach += 1
                carsReachedM.append(car.id)
    carsReached.insert(0, trace.cars[event])
    return [100*carNum/total, carsReached, 100*multiReach/total]

def carsInTime2hop(event, traces, time1hop, time2hop):
    cars1hop = []
    carsReached1 = []
    carsReached2 = []
    for t in range(0, simuTime):
        tempList = []
        for car in traces[t].cars:
            tempCar = findIDInTrace(traces[0].cars[event].id, traces[t])
            if tempCar and car.id not in carsReached1 and car.id not in tempList:
                if car.id not in carsReached2:
                    carDist = calcDist([tempCar.x, tempCar.y],[car.x, car.y])
                    if carDist < 200:
                        if carDist < naka():
                            tempList.append(car.id)
                            time2hop.append(t)
                if car.id not in cars1hop:
                    carDist = calcDist([tempCar.x, tempCar.y],[car.x, car.y])
                    if carDist < 200:
                        if carDist < naka():
                            cars1hop.append(car.id)
                            time1hop.append(t)
            for sv in carsReached1:
                tempCar = findIDInTrace(sv, traces[t])
                if tempCar and car.id not in carsReached1 and car.id not in tempList and car.id not in carsReached2:
                    carDist = calcDist([tempCar.x, tempCar.y],[car.x, car.y])
                    if carDist < 200:
                        if carDist < naka():
                            carsReached2.append(car.id)
                            time2hop.append(t)
        for new in tempList:
            carsReached1.append(new)

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

def findNearest(traces, bs, car):
    for trace in traces:
        carInT = findCarInTrace(car, trace)
        if carInT:
            eventCoord = [carInT.x, carInT.y]
            for base in bs:
                dist = calcDist(eventCoord, [base.x,base.y])
                if dist < naka():
                    return base
    return False

def svRSUs(traces, bs, car):
    found = []
    rsusFound = []
    for t in range(simuTime):
        carInT = findCarInTrace(car, traces[t])
        if carInT:
            eventCoord = [carInT.x, carInT.y]
            for base in bs:
                dist = calcDist(eventCoord, [base.x,base.y])
                if dist < naka() and base not in rsusFound:
                    found.append([base, t])
                    rsusFound.append(base)
    return found

def radiusRSUs(traces, bs, car):
    nearRSU = False
    t = 0
    while not nearRSU and t < simuTime:
        carInT = findCarInTrace(car, traces[t])
        if carInT:
            eventCoord = [carInT.x, carInT.y]
            for base in bs:
                dist = calcDist(eventCoord, [base.x,base.y])
                if dist < naka():
                    nearRSU = base
        t += 1
    found = [nearRSU]
    if nearRSU:
        baseCoord = [nearRSU.x,nearRSU.y]
        for rsu in bs:
            dist = calcDist(baseCoord, [rsu.x,rsu.y])
            if dist < naka()*5:
                found.append(rsu)
    return found, t

def removeHighValues(vec):
    for el in vec:
        if el == 'remove' or el == 'remove\n':
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

def baseReachTime(bs, traces, start, carsReached):
    bsCoord = [bs.x, bs.y]
    time = []
    for t in range(start, simuTime):
        for car in traces[t].cars:
            carDist = calcDist(bsCoord,[car.x, car.y])
            if carDist < naka() and car.id not in carsReached:
                carsReached.append(car.id)
                time.append(t)
    return time

def baseTimeRadius(rsus, traces, start):
    time = []ocarsReached = []
    for t in range(start, simuTime):
        for car in traces[t].cars:
            for rsu in rsus:
                coord = [rsu.x, rsu.y]
                carDist = calcDist(coord,[car.x, car.y])
                if carDist < naka() and car.id not in carsReached:
                    carsReached.append(car.id)
                    time.append(t)
    return time

def baseTimeSV(rsus, traces):
    time = []
    rsusFound = []
    carsReached = []
    for t in range(simuTime):
        for rsu in rsus:
            if rsu[1] == t:
                rsusFound.append(rsu[0])
        if len(rsusFound) > 0:
            for car in traces[t].cars:
                for rsu in rsusFound:
                    coord = [rsu.x, rsu.y]
                    carDist = calcDist(coord,[car.x, car.y])
                    if carDist < naka() and car.id not in carsReached:
                        carsReached.append(car.id)
                        time.append(t)
    return time

def baseReach(bs, trace, carsReached):
    total = trace.countCars()
    bsCoord = [bs.x, bs.y]
    reach = 0
    for car in trace.cars:
        carDist = calcDist(bsCoord,[car.x, car.y])
        if carDist < naka() and car.id not in carsReached:
            reach += 1
            carsReached.append(car.id)
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

def loadEvents(file):
    with open("DATA/{0}".format(file), "r") as data:
        events = data.readlines()
        for event in events:
            event = int(event)
        return events

def runSimulations(simNum, traces, rsus, events, rsuReachS, rsuReachR):
    case = [246, 500, 1000]
    for n in range(simNum):
        for rsu, a in zip(rsus, range(3)):
            print("{0}/{1}".format(n+1, simNum))

            basesR, start = radiusRSUs(traces, rsu, traces[0].cars[events[n]])
            if len(basesR) > 0:
                rsuReachR[a] += baseTimeRadius(basesR, traces, start)

            basesS = svRSUs(traces, rsu, traces[0].cars[events[n]])
            if len(basesS) > 0:
                rsuReachS[a] += baseTimeSV(basesS, traces)

def runSimulations2(traces, events, time1hop, time2hop):
    n = 1
    for event in events:
        print("{0:.2f}%".format(n/len(events)))
        carsInTime2hop(event, traces, time1hop, time2hop)
        n+=1

def saveFile(filename, data):
    with open(filename, "w") as file:
        print("open "+filename)
        for el in data:
         file.write("{0}\n".format(el))

print("starting..")
start_time = time.time()
filenames = []
sufix = ["8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm"]
for i in range(len(sufix)):
    filenames.append(sufix[i]+".txt")
radius = 200
propSpeed = 299792458
print ("reading rsus")
rsus = []
rsufiles = ["bases/bs_246.txt", "bases/bs_500.txt", "bases/bs_1000.txt"]
for file in rsufiles:
    rsus.append(readBS(file))
carsList = [0] * 120
multiList = [0] * 120
rsuReachS = [[],[],[]]
rsuReachR = [[],[],[]]
time1hop = []
time2hop = []
totalCars = []
for file in filenames:
    print ("\nreading "+file)
    traces = []
    traces = readTraces(file)
    totalCars.append(traces[0].countCars())
    # events = loadEvents("events{0}".format(file))
    # for event in range(simNum):
    #     events.append(random.randint(0,traces[0].countCars() - 1))
    # saveFile("events{0}".format(file), events)
    # print("simulating")
    # runSimulations(simNum, traces, rsus, events, rsuReachS, rsuReachR)
    # runSimulations2(traces, events, time1hop, time2hop)
    print("end of simulation from "+file)
# cases = ["246", "500", "1000"]
# id=0
# for case in cases:
#     saveFile("multipleRSUsTimeSV-{0}.txt".format(case), rsuReach[id])
#     id+=1
# saveFile("carsTime1hop.txt", time1hop)
# saveFile("carsTime2hop.txt", time2hop)
print(sum(totalCars)/len(totalCars))
print("end of simulations")
print ("simulation time: {:.2f} minutes".format((time.time() - start_time)/60))
