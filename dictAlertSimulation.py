# Leonardo Sole - GTA
#
import math
import itertools
import random
from scipy.stats import nakagami
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import datetime
import numpy as np
import os
from multiprocessing import Process

simuTime = 100
radius = 200
propSpeed = 299792458

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
        self.cars = {}
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

def carsInTime1hop(event, traces):
    carsReached = []
    time = []
    for t in range(0, simuTime):
        tempCar = findCarInTrace(traces[0].cars[event], traces[t])
        if tempCar:
            eventCoord = [tempCar.x, tempCar.y]
            for car in traces[t].cars:
                carDist = calcDist(eventCoord,[car.x, car.y])
                if carDist < naka() and car.id not in carsReached:
                    carsReached.append(car.id)
                    time.append(t)
    return time

def carsInTime2hop(event, traces, time1hop, time2hop):
    cars1hop = []
    carsReached1 = []
    carsReached2 = []
    for i, key in enumerate(traces[0].cars.keys()):
        if i == event:
            eoi = key
    for t in range(0, simuTime):
        print("\t\t\t\t{0:.2f}/{1:d} minutes".format(t/60, simuTime/60), end='\r')
        tempList = []
        for car in traces[t].cars.values():
            if eoi in traces[t].cars:
                tempCar = traces[t].cars[eoi]
                if car.id not in carsReached1 and car.id not in tempList:
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
                if sv in traces[t].cars:
                    tempCar = traces[t].cars[sv]
                    if car.id not in carsReached1 and car.id not in tempList and car.id not in carsReached2:
                        carDist = calcDist([tempCar.x, tempCar.y],[car.x, car.y])
                        if carDist < 200:
                            if carDist < naka():
                                carsReached2.append(car.id)
                                time2hop.append(t)
        for new in tempList:
            carsReached1.append(new)
    print("\t\t\t\tdone                      ", end='\r')

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
    time = []
    carsReached = []
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

def findIDInTrace(wantedID, trace):
    for car in trace.cars:
        if car.id == wantedID:
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
            car = Car(temp[1], float(temp[2]), float(temp[3]))
            if count == 0:
                traces.append(Time(temp[0]))
                traces[0].cars[car.id]=car
                count = 1
            elif temp[0] == traces[-1].sec:
                traces[-1].cars[car.id]=car
            else:
                traces.append(Time(temp[0]))
                traces[-1].cars[car.id]=car
    return traces

def loadEvents(file):
    events = []
    with open("DATA/{0}".format(file), "r") as data:
        temp = data.readlines()
        for event in temp:
            events.append(int(event))
        return events

def runSimulations(simNum, traces, rsus, events, rsuReachS, rsuReachR):
    global percent
    global all
    case = [246, 500, 1000]
    all*=2
    for n in range(simNum):
        for rsu, a in zip(rsus, range(3)):
            print("{0:.2f}% | {1}                  ".format(100*percent/all, case[a]), end='\r')

            basesR, start = radiusRSUs(traces, rsu, traces[0].cars[events[n]])
            print("{0:.2f} | {1}: {2} found     ".format(100*percent/all, case[a], len(basesR)), end='\r')
            if len(basesR) > 0:
                rsuReachR[a] += baseTimeRadius(basesR, traces, start)
            percent+=1

            basesS = svRSUs(traces, rsu, traces[0].cars[events[n]])
            print("{0:.2f}% | {1}: {2} found     ".format(100*percent/all, case[a], len(basesS)), end='\r')
            if len(basesS) > 0:
                rsuReachS[a] += baseTimeSV(basesS, traces)
            percent+=1

def runSimulations2(traces, events, time1hop, time2hop):
    for event in events:
        carsInTime2hop(event, traces, time1hop, time2hop)
    appendFile("carsTime10m1hop.txt", time1hop)
    appendFile("carsTime10m2hop.txt", time2hop)


def saveFile(filename, data):
    with open(filename, "w") as file:
        print("writing "+filename)
        for el in data:
         file.write("{0}\n".format(el))

def appendFile(filename, data):
    with open(filename, "a") as file:
        print("appending "+filename)
        for el in data:
         file.write("{0}\n".format(el))

if __name__ == '__main__':
    print("starting..")
    now = datetime.datetime.now()
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
    filenames = []
    sufix = ["8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm"]
    for suf in sufix:
        filenames.append(suf+".txt")
    radius = 200
    propSpeed = 299792458
    # print ("reading rsus")
    # rsus = []
    # rsufiles = ["bases/bs_246.txt", "bases/bs_500.txt", "bases/bs_1000.txt"]
    # for file in rsufiles:
    #     rsus.append(readBS(file))
    time1hop = []
    time2hop = []
    # cases = ["246", "500", "1000"]
    processes = []
    percent = 0
    totalCars = []
    for file, suf in zip(filenames,sufix):
        print ("\nreading "+file)
        traces = []
        traces = readTraces(file)
        total = traces[0].countCars()
        print(total)
        totalCars.append(total)
        # events = loadEvents("event8am.txt")
        # events = loadEvents("events{0}.txt".format(sufix))
        # simNum = 20
        # events = []
        # for event in range(simNum):
        #     events.append(random.randint(0,traces[0].countCars() - 1))
        # saveFile("events{0}".format(file), events)
        # runSimulations(simNum, traces, rsus, events, rsuReachS, rsuReachR)
        # runSimulations2(traces, events, time1hop, time2hop, sufix[n])
        # process = Process(target=runSimulations2, args=(traces, events, time1hop, time2hop))
        # processes.append(process)
        # process.start()
        # print("initialized events: {}".format(filenames.index(file)+1), end='\r')
    # for process in processes:
    #     process.join()
    #     percent+=1
    #     print("{0:.1f}% completed simulations          ".format(100*percent/len(processes)), end='\r')
    # for case in cases:
    #     saveFile("multipleRSUsTimeSV-{0}.txt".format(case), rsuReachS[id])
    #     id+=1
    print(f"average = {sum(totalCars)/len(totalCars)}")
    print("end of simulations")
    now = datetime.datetime.now()
    print (now.strftime("%Y-%m-%d %H:%M:%S"))
