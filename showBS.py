import math
import itertools
import random
import xml.etree.ElementTree as ET
from scipy.stats import nakagami
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import time
import numpy as np

class BS:
    def __init__(self):
        self.x = []
        self.y = []


def calcDist(pointA, pointB): # calculates de distance between two points
    aX, aY, bX, bY = pointA[0], pointA[1], pointB[0], pointB[1]

    xDiff = abs(aX - bX)
    yDiff = abs(aY - bY)

    return math.sqrt(xDiff**2 + yDiff**2)

def readBS(file):
    bs = BS()
    with open(file, "r") as bsFile:
        bsLines = bsFile.readlines()
        for i in range(0, len(bsLines)):
            temp = bsLines[i].split()
            bs.x.append(float(temp[1]))
            bs.y.append(float(temp[2]))
    return bs

def newPoint(bs):
    maxX = 26000
    minX = int(min(bs.x))
    minY = int(min(bs.y))
    maxY = 30000
    x1 = random.randint(minX, maxX)
    y1 = random.randint(minY, maxY)
    for x0, y0 in zip(bs.x, bs.y):
        while calcDist([x0, y0],[x1,y1]) < 700:
            x1 = random.randint(minX, maxX)
            y1 = random.randint(minY, maxY)
    bs.x.append(x1)
    bs.y.append(y1)

def readTraces(txtFile):
    traces = BS()
    count = 0
    t = 0
    with open(txtFile, "r") as trFile:
        trLines = trFile.readlines()
        for line in trLines:
            temp = line.split()
            if count == 0:
                t = temp[0]
                traces.x.append(float(temp[2]))
                traces.y.append(float(temp[3]))
                count = 1
            elif temp[0] == t:
                count+=1
                traces.x.append(float(temp[2]))
                traces.y.append(float(temp[3]))
            else:
                print(count)
                return traces
    return traces
def addPoints(bs, n):
    for i in range(0,n):
        newPoint(bs)
    id = 0
    with open("bs_"+str(n+246)+".txt", "w") as bsFile:
        for x, y in zip(bs.x, bs.y):
         bsFile.write("{0} {1} {2}\n".format(id, x, y))
         id += 1

def showAPs():
    bs246 = readBS("bases/bs_246.txt")
    bs500 = readBS("bs_500.txt")
    bs1000 = readBS("bs_1000.txt")
    tr = readTraces("9am.txt")
    plt.figure()
    plt.scatter(x=bs1000.x, y=bs1000.y, color='#00ff4e', s=1)
    plt.scatter(x=bs500.x, y=bs500.y, color='#0038ff', s=1)
    plt.scatter(x=bs246.x, y=bs246.y, color='#e300ff', s=1)
    plt.scatter(x=tr.x, y=tr.y, color='#000000', s=0.2)
    plt.savefig("APs2.png")

bs = readBS("bases/bs_246.txt")
# addPoints(bs, 500-246)
# addPoints(bs, 1000-246)
# showAPs()
print("min({0}|{1})".format(int(min(bs.x)), int(min(bs.y))))
