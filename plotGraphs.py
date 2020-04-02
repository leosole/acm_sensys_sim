from scipy.stats import norm
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import matplotlib.lines as mlines
matplotlib.use('Agg')
from matplotlib import rc
from matplotlib import rcParams

# Graph settings
# rcParams['text.usetex'] = True
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
# rc('text', usetex=True)
plt.rcParams.update()
sns.set_context("paper")
# sns.set(font_scale=1.5, rc={'text.usetex' : True})
sns.set(font_scale=1.5)
sns.set_style('white', {'font.family':'serif', 'font.serif':'Times New Roman', 'background':'white'})
sns.despine()

def loadData(file, const=1):
    readData = []
    with open("DATA/"+file, "r") as data:
        lines = data.readlines()
        for line in lines:
            if line != 'remove' and line != 'remove\n':
                readData.append(float(line)*const)
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


def plotAPReach():
    apReach246 = loadData("APReachT_246.txt")
    apReach500 = loadData("APReachT_500.txt")
    apReach1000 = loadData("APReachT_1000.txt")
    plt.figure()
    tot = len(apReach246)
    x246, counted246 = countTotal(apReach246)
    x500, counted500 = countTotal(apReach500)
    x1000, counted1000 = countTotal(apReach1000)
    p246 = mpatches.Patch(label='246 APs | average = {0:0.2f}'.format(len(apReach246)/260))
    p500 = mpatches.Patch(label='500 APs | average = {0:0.2f}'.format(len(apReach500)/260))
    p1000 = mpatches.Patch(label='1000 APs | average = {0:0.2f}'.format(len(apReach1000)/260))
    plt.plot(x246, counted246)
    plt.plot(x500, counted500)
    plt.plot(x1000, counted1000)
    plt.legend(handles=[p246, p500, p1000])
    bound = findMax(apReach246, apReach500, apReach1000)
    plt.axis([-1, bound+1, 0, 1])
    plt.xlabel('Time (seconds)')
    plt.ylabel('New Vehicles')
    plt.tight_layout(True)
    plt.savefig('graphs/RSUTimeReach.png', dpi=300)

def plotCarsReached():
    carsReached = loadData("carsReachSingle.txt")
    multiReach = loadData("carsReachMulti.txt")
    plt.figure()
    # xmin=0
    # xmax=5
    # steps=5000
    # stepsize=float(xmax-xmin)/float(steps)
    # xpoints=[i*stepsize for i in range(int(xmin/stepsize),int(xmax/stepsize))]
    # def countCars(data):
    #     tot = len(data)
    #     counted =[]
    #     last = 0
    #     for n in range(5000):
    #         if n == 0:
    #             last = data.count(n)/tot
    #             counted.append(last)
    #         else:
    #             for el in data:
    #                 temp = 0
    #                 if el > (n-1)/1000 and el < n/1000:
    #                     temp+=1
    #                 last += temp/tot
    #             counted.append(last)
    #     return counted
    # countedCars = countCars(carsReached)
    # multiCars = countCars(multiReach)
    # plt.plot(xpoints, countedCars)
    # plt.plot(xpoints, multiCars)

    # singleP = mpatches.Patch(linewidth=1, label='single hop')
    # multiP = mpatches.Patch(linewidth=1, label='double hop')
    # sns.kdeplot(np.array(carsReached), bw=0.4, cut=0)
    # sns.kdeplot(np.array(multiReach), bw=0.4, cut=0)
    sns.distplot(np.array(carsReached), kde_kws={"bw":0.3, "cut":0}, hist=False, label='single hop')
    sns.distplot(np.array(multiReach), kde_kws={"bw":0.3, "cut":0}, hist=False, label='double hop')
    # sns.distplot(np.array(carsReached), hist=False)
    # sns.distplot(np.array(multiReach), hist=False)
    plt.xlabel('% Cars Reached')
    plt.ylabel('Density')
    plt.legend()
    plt.tight_layout(True)
    plt.savefig('graphs/V2VReachPDF.png', dpi=300)

def plotRSUReach():
    reach246 = loadData("APReach_246.txt", 100)
    reach500 = loadData("APReach_500.txt", 100)
    reach1000 = loadData("APReach_1000.txt", 100)
    plt.figure()
    # p246 = mpatches.Patch(linewidth=1, label='246 RSU')
    # p500 = mpatches.Patch(linewidth=1, label='500 RSU')
    # p1000 = mpatches.Patch(linewidth=1, label='1000 RSU')
    sns.distplot(np.array(reach246), kde_kws={"bw":0.3, "cut":0}, hist=False, label='246 RSU')
    sns.distplot(np.array(reach500), kde_kws={"bw":0.3, "cut":0}, hist=False, label='500 RSU')
    sns.distplot(np.array(reach1000), kde_kws={"bw":0.3, "cut":0}, hist=False, label='1000 RSU')
    plt.xlabel('% Cars Reached')
    plt.ylabel('Density')
    plt.legend()
    plt.tight_layout(True)
    plt.savefig('graphs/RSUReachPDF.png', dpi=300)

def plotAPDelayDens():
    multi_246 = loadData("delayMulti_246.txt")
    single_246 = loadData("delaySingle_246.txt")
    multi_500 = loadData("delayMulti_500.txt")
    single_500 = loadData("delaySingle_500.txt")
    multi_1000 = loadData("delayMulti_1000.txt")
    single_1000 = loadData("delaySingle_1000.txt")
    sPatch246 = mpatches.Patch(label='single hop | 246 AP')
    mPatch246 = mpatches.Patch(label='double hop | 246 AP')
    sPatch500 = mpatches.Patch(label='single hop | 500 AP')
    mPatch500 = mpatches.Patch(label='double hop | 500 AP')
    sPatch1000 = mpatches.Patch(label='single hop | 1000 AP')
    mPatch1000 = mpatches.Patch(label='double hop | 1000 AP')

    plt.figure()
    sns.kdeplot(np.array(single_246), bw=0.5, cut=0)
    sns.kdeplot(np.array(multi_246), bw=0.5, cut=0)
    sns.kdeplot(np.array(single_500), bw=0.5, cut=0)
    sns.kdeplot(np.array(multi_500), bw=0.5, cut=0)
    sns.kdeplot(np.array(single_1000), bw=0.5, cut=0)
    sns.kdeplot(np.array(multi_1000), bw=0.5, cut=0)
    plt.legend(handles=[sPatch246, sPatch500, sPatch1000, mPatch246, mPatch500, mPatch1000])
    plt.title('Density AP Delay')
    plt.xlabel('Delay (seconds)')
    plt.ylabel('Density')
    # plt.tight_layout(True)
    plt.savefig('graphs/RSUDelayPDF.png', dpi=300)

def plotAPDelay():
    multi_246 = loadData("delayMulti_246.txt")
    single_246 = loadData("delaySingle_246.txt")
    multi_500 = loadData("delayMulti_500.txt")
    single_500 = loadData("delaySingle_500.txt")
    multi_1000 = loadData("delayMulti_1000.txt")
    single_1000 = loadData("delaySingle_1000.txt")
    plt.figure()
    s246, cs246 = countTotal(single_246)
    plt.plot(s246, cs246, label='single hop : 246 AP')
    s500, cs500 = countTotal(single_500)
    plt.plot(s500, cs500, label='single hop : 500 AP')
    s1000, cs1000 = countTotal(single_1000)
    plt.plot(s1000, cs1000, label='single hop : 1000 AP')
    m246, cm246 = countTotal(multi_246)
    plt.plot(m246, cm246, label='double hop : 246 AP')
    m500, cm500 = countTotal(multi_500)
    plt.plot(m500, cm500, label='double hop : 500 AP')
    m1000, cm1000 = countTotal(multi_1000)
    plt.plot(m1000, cm1000, label='double hop : 1000 AP')
    plt.axis([-1, 600, 0, 1])
    plt.legend()
    plt.xlabel('Delay (seconds)')
    plt.tight_layout(True)
    plt.savefig('graphs/RSUdelayCDF.png', dpi=300)

def plotCarsInTime():
    plt.figure()
    carsTime = loadData("carsInTime.txt")
    x, counted = countTotal(carsTime)
    plt.plot(x, counted)
    plt.xlabel('Time (seconds)')
    plt.ylabel('New Vehicles')
    plt.tight_layout(True)
    plt.savefig('graphs/V2VTimeReach.png', dpi=300)

# plotAPDelay()
# plotCarsReached()
# plotRSUReach()
