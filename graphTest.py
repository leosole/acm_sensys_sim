from scipy.stats import norm
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import matplotlib.lines as mlines

def loadData(file):
    readData = []
    with open("DATA/"+file, "r") as data:
        lines = data.readlines()
        for line in lines:
            if line != 'remove' and line != 'remove\n':
                readData.append(float(line))
    return readData

def avg(data):
    return sum(data)/len(data)

def countTotal(data, tot=False):
    if not tot:
        tot = len(data)
    counted = []
    for n in range(0, int(max(data))):
        if n == 0:
            counted.append(data.count(n)/tot)
        else:
            counted.append(data.count(n)/tot+counted[n-1])
    x = list(range(int(max(data))))
    x.insert(0,0)
    counted.insert(0,0)
    return x, counted

def findMax(l1, l2, l3):
    m1 = int(max(l1))
    m2 = int(max(l2))
    m3 = int(max(l3))
    all = [m1, m2, m3]
    return max(all)




hexs246 = '#ff8c39'
hexm246 = '#4075ff'
hexs500 = '#b65006'
hexm500 = '#002c9d'
hexs1000 = '#692c01'
hexm1000 = '#001857'

def plotAPReach():
    apReach246 = loadData("APReach_246.txt")
    apReach500 = loadData("APReach_500.txt")
    apReach1000 = loadData("APReach_1000.txt")
    plt.figure()
    tot = len(apReach246)
    x246, counted246 = countTotal(apReach246)
    x500, counted500 = countTotal(apReach500)
    x1000, counted1000 = countTotal(apReach1000)
    p246 = mpatches.Patch(color=hexs246, label='246 APs | average = {0:0.2f}'.format(len(apReach246)/260))
    p500 = mpatches.Patch(color=hexm500, label='500 APs | average = {0:0.2f}'.format(len(apReach500)/260))
    p1000 = mpatches.Patch(color=hexs1000, label='1000 APs | average = {0:0.2f}'.format(len(apReach1000)/260))
    plt.plot(x246, counted246, color=hexs246)
    plt.plot(x500, counted500, color=hexm500)
    plt.plot(x1000, counted1000, color=hexs1000)
    plt.legend(handles=[p246, p500, p1000])
    bound = findMax(apReach246, apReach500, apReach1000)
    plt.axis([-1, bound+1, 0, 1])
    plt.title('Average Reach Through Access Points')
    plt.xlabel('Time (seconds)')
    plt.ylabel('New Vehicles')
    plt.savefig('graphs/APReach.png')

def plotCarsReached():
    carsReached = loadData("carsReachSingle.txt")
    multiReach = loadData("carsReachMulti.txt")
    plt.figure()

    xmin=0
    xmax=5
    steps=5000
    stepsize=float(xmax-xmin)/float(steps)
    xpoints=[i*stepsize for i in range(int(xmin/stepsize),int(xmax/stepsize))]
    def countCars(data):
        tot = len(data)
        counted =[]
        last = 0
        for n in range(5000):
            if n == 0:
                last = data.count(n)/tot
                counted.append(last)
            else:
                for el in data:
                    temp = 0
                    if el > (n-1)/1000 and el < n/1000:
                        temp+=1
                    last += temp/tot
                counted.append(last)
        return counted
    countedCars = countCars(carsReached)
    multiCars = countCars(multiReach)
    plt.plot(xpoints, countedCars, color='#ff6b00')
    plt.plot(xpoints, multiCars, color='#0047ff')

    carsAvg = avg(carsReached)
    multiAvg = avg(multiReach)
    singleP = mpatches.Patch(color='#ff6b00', linewidth=1, label='single hop')
    multiP = mpatches.Patch(color='#0047ff', linewidth=1, label='double hop')
    singleAv = mlines.Line2D([], [], color='#ff6b00', linewidth=1, label='average: {0:0.2f}'.format(carsAvg), linestyle='--')
    multiAv = mlines.Line2D([], [], color='#0047ff', linewidth=1, label='average: {0:0.2f}'.format(multiAvg), linestyle='--')
    # sns.kdeplot(np.array(carsReached), bw=0.4, cut=0, color='#ff6b00')
    # sns.kdeplot(np.array(multiReach), bw=0.4, cut=0, color='#0047ff')
    plt.title('CDF of Cars Reached')
    plt.xlabel('% Cars Reached')
    plt.ylabel('Density')
    plt.axvline(x=carsAvg, color='#ff6b00', linestyle='--', linewidth=1)
    plt.axvline(x=multiAvg, color='#0047ff', linestyle='--', linewidth=1)
    plt.legend(handles=[singleP, singleAv, multiP, multiAv])
    plt.savefig('graphs/carsReachedT.png')

def plotAPDelayDens():
    multi_246 = loadData("delayMulti_246.txt")
    single_246 = loadData("delaySingle_246.txt")
    multi_500 = loadData("delayMulti_500.txt")
    single_500 = loadData("delaySingle_500.txt")
    multi_1000 = loadData("delayMulti_1000.txt")
    single_1000 = loadData("delaySingle_1000.txt")
    sPatch246 = mpatches.Patch(color=hexs246, label='single hop | 246 AP')
    mPatch246 = mpatches.Patch(color=hexm246, label='double hop | 246 AP')
    sPatch500 = mpatches.Patch(color=hexs500, label='single hop | 500 AP')
    mPatch500 = mpatches.Patch(color=hexm500, label='double hop | 500 AP')
    sPatch1000 = mpatches.Patch(color=hexs1000, label='single hop | 1000 AP')
    mPatch1000 = mpatches.Patch(color=hexm1000, label='double hop | 1000 AP')

    plt.figure()
    sns.kdeplot(np.array(single_246), bw=0.5, cut=0, color=hexs246)
    sns.kdeplot(np.array(multi_246), bw=0.5, cut=0, color=hexm246)
    sns.kdeplot(np.array(single_500), bw=0.5, cut=0, color=hexs500)
    sns.kdeplot(np.array(multi_500), bw=0.5, cut=0, color=hexm500)
    sns.kdeplot(np.array(single_1000), bw=0.5, cut=0, color=hexs1000)
    sns.kdeplot(np.array(multi_1000), bw=0.5, cut=0, color=hexm1000)
    plt.legend(handles=[sPatch246, sPatch500, sPatch1000, mPatch246, mPatch500, mPatch1000])
    plt.title('Density AP Delay')
    plt.xlabel('Delay (seconds)')
    plt.ylabel('Density')
    plt.savefig('graphs/APDelayDens.png')

def plotAPDelay():
    multi_246 = loadData("delayMulti_246.txt")
    single_246 = loadData("delaySingle_246.txt")
    multi_500 = loadData("delayMulti_500.txt")
    single_500 = loadData("delaySingle_500.txt")
    multi_1000 = loadData("delayMulti_1000.txt")
    single_1000 = loadData("delaySingle_1000.txt")
    sPatch246 = mpatches.Patch(color=hexs246, label='single hop | 246 AP')
    mPatch246 = mpatches.Patch(color=hexm246, label='double hop | 246 AP')
    sPatch500 = mpatches.Patch(color=hexs500, label='single hop | 500 AP')
    mPatch500 = mpatches.Patch(color=hexm500, label='double hop | 500 AP')
    sPatch1000 = mpatches.Patch(color=hexs1000, label='single hop | 1000 AP')
    mPatch1000 = mpatches.Patch(color=hexm1000, label='double hop | 1000 AP')
    sAv246 = mlines.Line2D([], [], color=hexs246, linewidth=1, label='average: {0:0.0f}'.format(avg(single_246)), linestyle='--')
    sAv500 = mlines.Line2D([], [], color=hexs500, linewidth=1, label='average: {0:0.0f}'.format(avg(single_500)), linestyle='--')
    sAv1000 = mlines.Line2D([], [], color=hexs1000, linewidth=1, label='average: {0:0.0f}'.format(avg(single_1000)), linestyle='--')
    mAv246 = mlines.Line2D([], [], color=hexm246, linewidth=1, label='average: {0:0.0f}'.format(avg(multi_246)), linestyle='--')
    mAv500 = mlines.Line2D([], [], color=hexm500, linewidth=1, label='average: {0:0.0f}'.format(avg(multi_500)), linestyle='--')
    mAv1000 = mlines.Line2D([], [], color=hexm1000, linewidth=1, label='average: {0:0.0f}'.format(avg(multi_1000)), linestyle='--')
    plt.figure()
    plt.axvline(x=avg(single_246), color=hexs246, linestyle='--', linewidth=1)
    plt.axvline(x=avg(single_500), color=hexs500, linestyle='--', linewidth=1)
    plt.axvline(x=avg(single_1000), color=hexs1000, linestyle='--', linewidth=1)
    plt.axvline(x=avg(multi_246), color=hexm246, linestyle='--', linewidth=1)
    plt.axvline(x=avg(multi_500), color=hexm500, linestyle='--', linewidth=1)
    plt.axvline(x=avg(multi_1000), color=hexm1000, linestyle='--', linewidth=1)
    s246, cs246 = countTotal(single_246)
    plt.plot(s246, cs246, color=hexs246)
    s500, cs500 = countTotal(single_500)
    plt.plot(s500, cs500, color=hexs500)
    s1000, cs1000 = countTotal(single_1000)
    plt.plot(s1000, cs1000, color=hexs1000)
    m246, cm246 = countTotal(multi_246)
    plt.plot(m246, cm246, color=hexm246)
    m500, cm500 = countTotal(multi_500)
    plt.plot(m500, cm500, color=hexm500)
    m1000, cm1000 = countTotal(multi_1000)
    plt.plot(m1000, cm1000, color=hexm1000)
    plt.axis([-1, 600, 0, 1])
    plt.legend(handles=[sPatch246, sAv246, sPatch500, sAv500, sPatch1000, sAv1000, mPatch246, mAv246, mPatch500, mAv500, mPatch1000, mAv1000])
    plt.title('CDF AP Delay')
    plt.xlabel('Delay (seconds)')
    plt.savefig('graphs/APdelay.png')

def plotCarsInTime():
    plt.figure()
    carsTime = loadData("carsInTime.txt")
    x, counted = countTotal(carsTime)
    plt.plot(x, counted, color=hexs246)
    plt.title('Average Reach Through V2V in Time')
    plt.xlabel('Time (seconds)')
    plt.ylabel('New Vehicles')
    plt.savefig('graphs/TimeReach.png')

plotAPDelay()
