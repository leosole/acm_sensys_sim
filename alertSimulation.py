# Leonardo Sole - GTA
#
print("importing libs..")
import math
import itertools
import random
from scipy.stats import nakagami
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import time
import numpy as np
import os
from multiprocessing import Process

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
    for t in range(0, simuTime):
        print("\t\t\t\t{0:.2f}/10 minutes".format(t/60), end='\r')
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
    events = []
    with open("DATA/{0}".format(file), "r") as data:
        temp = data.readlines()
        for event in temp:
            events.append(int(event))
        return events

def mapSim(traces, rsus, eoi, sufix):
    rt246 = []
    rt500 = []
    rt1000 = []
    rd246 = []
    rd500 = []
    rd1000 = []
    routex = []
    routey = []
    route = []
    t246=600
    t500=600
    t1000=600
    t=0
    event = traces[0].cars[eoi]
    for trace in traces:
        sv = findCarInTrace(traces[0].cars[eoi], trace)
        if sv:
            routex.append(sv.x)
            routey.append(sv.y)
            route.append(sv)
            r=0
            for rsu in rsus:
                dist = calcDist([rsu.x,rsu.y],[sv.x,sv.y])
                if dist < 200:
                    if r < 246 and rsu not in rt246:
                        if len(rt246) == 0:
                            t246=t
                        rt246.append(rsu)
                    elif r < 500 and rsu not in rt500 and rsu not in rt246:
                        if len(rt500) == 0:
                            t500=t
                        rt500.append(rsu)
                    elif rsu not in rt1000 and rsu not in rt500 and rsu not in rt246:
                        if len(rt1000) == 0:
                            t1000=t
                        rt1000.append(rsu)
                r+=1
        t+=1
    if len(rt246) > 0:
        plt.figure()
        ax = plt.subplot()
        ax.plot(routex, routey, color='blue', label='SV route', lw=1, zorder=0)
        ax.scatter(event.x, event.y, color='#eb9b00', label='EoI', s=20, zorder=100, marker='X')
        first246 = rt246[0]
        first500 = rt246[0]
        first1000 = rt246[0]
        if t246>t500:
            first500 = rt500[0]
        rd500.append(first500)
        if t246>t1000:
            first1000 = rt1000[0]
        rd1000.append(first1000)
        r=0
        rd246.append(first246)
        for rsu in rsus:
            if r < 246:
                dist = calcDist([rsu.x,rsu.y],[first246.x,first246.y])
                if dist < 1000:
                    rd246.append(rsu)
                if first246 != first500:
                    dist = calcDist([rsu.x,rsu.y],[first500.x,first500.y])
                if dist < 1000:
                    rd500.append(rsu)
                if first246 != first1000:
                    dist = calcDist([rsu.x,rsu.y],[first1000.x,first1000.y])
                if dist < 1000:
                    rd1000.append(rsu)
            elif r < 500:
                dist = calcDist([rsu.x,rsu.y],[first500.x,first500.y])
                if dist < 1000:
                    rd500.append(rsu)
                if first500 != first1000:
                    dist = calcDist([rsu.x,rsu.y],[first1000.x,first1000.y])
                if dist < 1000:
                    rd1000.append(rsu)
            else:
                dist = calcDist([rsu.x,rsu.y],[first1000.x,first1000.y])
                if dist < 1000:
                    rd1000.append(rsu)
            r+=1
        plotRSUS(ax, rd246, 4, '#64ff61', 16, 'RSUs in 1km radius|246', 3)
        plotRSUS(ax, rd500, 5, '#0baf07', 16, 'RSUs in 1km radius|500', 2)
        plotRSUS(ax, rd1000, 6, '#074606', 16, 'RSUs in 1km radius|1000')
        plotRSUS(ax, rt246, 7, '#f75252', 16, 'RSUs in route|246', 6)
        plotRSUS(ax, rt500, 7, '#aa0505', 16, 'RSUs in route|500', 5)
        plotRSUS(ax, rt1000, 7, '#410101', 16, 'RSUs in route|1000', 4)
        # plt.gca().set_aspect('equal', adjustable='box')
        plt.axis('scaled')
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0., framealpha=1, edgecolor='black', fancybox=False)
        # plt.tight_layout(True)
        plt.savefig(f"mapSim{sufix}.png", dpi=300, bbox_inches = "tight")

def plotRSUS(ax, rsus, marker, color, s=16, label=False, z=1):
    if len(rsus)>0:
        if label:
            ax.scatter(rsus[0].x, rsus[0].y, color=color, label=label, s=s, marker=marker)
        for rsu in rsus:
            ax.scatter(rsu.x, rsu.y, color=color, s=s, marker=marker)

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
    processes = []
    percent = 0
    for event in events:
        print("initializing event {}".format(event), end='\r')
        process = Process(target=carsInTime2hop, args=(event, traces, time1hop, time2hop))
        processes.append(process)
        process.start()
    for process in processes:
        print("{0:.2f}%completed".format(100*percent/len(processes)), end='\r')
        process.join()
        percent+=1
        print("{0:.2f}%completed".format(100*percent/len(processes)), end='\r')



def saveFile(filename, data):
    with open(filename, "w") as file:
        print("open "+filename)
        for el in data:
         file.write("{0}\n".format(el))

print("starting..")
start_time = time.process_time()
filenames = []
sufix = ["8am", "9am", "10am", "11am", "12am", "1pm", "2pm", "3pm", "4pm", "5pm", "6pm", "7pm", "8pm"]
for i in range(len(sufix)):
    filenames.append(sufix[i]+".txt")
radius = 200
propSpeed = 299792458
# print ("reading rsus")
rsus = []
rsufiles = ["bases/bs_246.txt", "bases/bs_500.txt", "bases/bs_1000.txt"]
for file in rsufiles:
    rsus.append(readBS(file))
time1hop = []
time2hop = []
rsuReachS = [[],[],[]]
rsuReachR = [[],[],[]]
n=0
cases = ["246", "500", "1000"]

for file in filenames:
    print(file)
    traces = readTraces(file)
    eoi = random.randint(0,traces[0].countCars() - 1)
    mapSim(traces, rsus[2], eoi, sufix[n])
    n+=1
exit()

for file in filenames:
    print ("\nreading "+file)
    traces = []
    traces = readTraces(file)
    events = loadEvents("events{0}.txt".format(sufix[n]))
    n+=1
    simNum = 20
    # events = []
    # for event in range(simNum):
    #     events.append(random.randint(0,traces[0].countCars() - 1))
    # saveFile("events{0}".format(file), events)
    print("simulating")
    # runSimulations(simNum, traces, rsus, events, rsuReachS, rsuReachR)
    runSimulations2(traces, events, time1hop, time2hop)
    print("end of simulation from "+file)
id=0
saveFile("carsTime10m1hop.txt", time1hop)
saveFile("carsTime10m2hop.txt", time2hop)
# for case in cases:
#     saveFile("multipleRSUsTimeSV-{0}.txt".format(case), rsuReachS[id])
#     id+=1

print("end of simulations")
print ("simulation time: {:.2f} minutes".format((time.process_time() - start_time)/60))
