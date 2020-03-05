# Leonardo Sole - GTA
#
import utm
import math

radius = 100

bsFile = open("koln_bs.txt", "r")
bsLines = bsFile.readlines()
bsFile.close()
bs = [] # list with base stations coordinates
for i in range(0, len(bsLines)):
    temp = bsLines[i].split()
    del temp[0]
    temp[0] = float(temp[0])
    temp[1] = float(temp[1])
    bs.append(temp)

def calcDist(pointA, pointB): # calculates de distance between two points
    aX, aY, bX, bY = pointA[0], pointA[1], pointB[0], pointB[1]

    xDiff = abs(aX - bX)
    yDiff = abs(aY - bY)

    return math.sqrt(xDiff**2 + yDiff**2)
