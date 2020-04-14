import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import rc
from matplotlib import rcParams
# from matplotlib.ticker import PercentFormatter
# from scipy.stats import expon
# from scipy.interpolate import interp1d


# Graph settings
rcParams['text.usetex'] = True
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
plt.rcParams.update()
sns.set_context("paper")
sns.set(font_scale=1.5)
sns.set(font_scale=1.5, rc={'text.usetex' : True})
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

def median(data):
    data.sort()
    middle = int(len(data)/2)
    return data[middle]

def setMarkerPlace(x, y):
    mid = (x[1]-x[0])/2
    newX = []
    newY = []
    for elx, ely in zip(x, y):
        if ely:
            newX.append(elx+mid)
            newY.append(ely)
    return newX, newY

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

def countFloat(data, steps=1000, maxi=False):
    if not maxi:
        maxi = max(data)
    tot = len(data)
    counted = []
    step = maxi/steps
    # temp = 0
    for n in range(0, steps+1):
        temp = 0
        for el in data:
            if el >= n*step and el < (n+1)*step:
                temp +=1
        counted.append(temp/tot)
        # counted.append(temp)
    x = np.arange(0, maxi, maxi/(steps+1))
    return x, counted

def countFloat2(data, steps=1000, maxi=False):
    if not maxi:
        maxi = max(data)
    tot = len(data)
    counted = []
    step = maxi/steps
    # temp = 0
    for n in range(0, steps+1):
        temp = 0
        for el in data:
            if n == 0:
                if el == 0:
                    temp +=1
            elif el > (n-1)*step and el < n*step:
                temp +=1
        counted.append(temp/tot)
        # counted.append(temp)
    x = np.arange(0, maxi, maxi/(steps+1))
    return x, counted

def findMax(l1, l2, l3, l4):
    m1 = int(max(l1))
    m2 = int(max(l2))
    m3 = int(max(l3))
    m4 = int(max(l4))
    all = [m1, m2, m3, m4]
    return max(all)

def plotTimeReach():
    apReach246 = loadData("APReachT_246.txt")
    apReach500 = loadData("APReachT_500.txt")
    apReach1000 = loadData("APReachT_1000.txt")
    carsTime = loadData("carsInTime.txt")
    x, counted = countTotal(carsTime)
    plt.figure()
    x246, counted246 = countTotal(apReach246)
    x500, counted500 = countTotal(apReach500)
    x1000, counted1000 = countTotal(apReach1000)
    # plt.plot(x246, counted246, linestyle='--', marker='o', label='246 RSUs : average = {0:0.1f}'.format(len(apReach246)/260))
    # plt.plot(x500, counted500, linestyle='-.', marker='v', label='500 RSUs : average = {0:0.1f}'.format(len(apReach500)/260))
    # plt.plot(x1000, counted1000, linestyle=':', marker='1', label='1000 RSUs : average = {0:0.1f}'.format(len(apReach1000)/260))
    # plt.plot(x, counted, linestyle='-', marker='x', label='V2V : average = {0:0.1f}'.format(len(apReach1000)/260))
    plt.plot(x246, counted246, linestyle='--', marker='o', label='246 RSUs', markevery=0.1)
    plt.plot(x500, counted500, linestyle='-.', marker='v', label='500 RSUs', markevery=0.1)
    plt.plot(x1000, counted1000, linestyle=':', marker='1', label='1000 RSUs', markevery=0.1)
    plt.plot(x, counted, linestyle='-', marker='x', label='V2V', markevery=0.1)
    plt.legend()
    bound = findMax(apReach246, apReach500, apReach1000, carsTime)
    plt.axis([-1, bound+1, 0, 1])
    plt.xlabel('Time (seconds)')
    plt.ylabel('New Vehicles')
    plt.tight_layout(True)
    plt.savefig('graphs/TimeReach.png', dpi=300)

def plotV2VPDF():
    carsReached = loadData("carsReachSingle.txt")
    multiReach = loadData("carsReachMulti.txt")
    plt.figure()
    binarray = np.arange(0, 5, 0.1)
    sns.distplot(np.array(carsReached), norm_hist=True, fit=expon, fit_kws={"color":"red", "cut":0, "linestyle":'--', "marker":'o', "markevery":0.1}, kde=False, label='single hop', hist=False, color='red')
    sns.distplot(np.array(multiReach), norm_hist=True, fit=expon, fit_kws={"color":"green", "cut":0, "linestyle":'-.', "marker":'v', "markevery":0.1}, kde=False, label='double hop', hist=False, color='blue')
    # plt.hist(carsReached, weights=np.ones(len(carsReached))/len(carsReached), alpha=0.4, bins = binarray, density=False, color='red', rwidth=1, histtype='step', linewidth=2)
    # plt.hist(multiReach, weights=np.ones(len(multiReach))/len(multiReach), alpha=0.4, bins = binarray, density=False, color='green', rwidth=1, histtype='step', linewidth=2)
    plt.hist(carsReached, alpha=0.4, bins = binarray, density=True, color='red', rwidth=1, histtype='step', linewidth=2)
    plt.hist(multiReach, alpha=0.4, bins = binarray, density=True, color='green', rwidth=1, histtype='step', linewidth=2)

    # plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
    plt.xlabel('% Cars Reached')
    plt.ylabel('Density')
    plt.legend()
    plt.tight_layout(True)
    plt.savefig('graphs/V2VReachPDF.png', dpi=300)
#
# def plotV2VHIST():
#     carsReached = loadData("carsReachSingle.txt")
#     multiReach = loadData("carsReachMulti.txt")
#     plt.figure()
#
#     # plt.hist(carsReached, bins = 200, label = 'single hop', histtype='bar', stacked=True, fill=False, linewidth=3)
#     # plt.hist(multiReach, bins = 200, label = 'double hop', histtype='bar', stacked=True, fill=False, linewidth=3)
#
#     plt.hist([carsReached, multiReach], weights=[np.ones(len(carsReached)) / len(carsReached), np.ones(len(multiReach)) / len(multiReach)], bins = 50, label = ['single hop','double hop'])
#     plt.xlabel('% Cars Reached')
#     plt.ylabel('Count')
#     plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
#     plt.legend()
#     plt.tight_layout(True)
#     plt.savefig('graphs/V2VReachHIST.png', dpi=300)

def plotRSUPDF():
    reach246 = loadData("APReachNew_246.txt")
    reach500 = loadData("APReachNew_500.txt")
    reach1000 = loadData("APReachNew_1000.txt")
    plt.figure()
    binarray = np.arange(0, 5, 0.1)
    sns.distplot(np.array(reach246), fit=expon, fit_kws={"color":"red", "cut":0, "linestyle":'--', "marker":'o', "markevery":0.1}, kde=False, label='246 RSUs', hist=False)
    sns.distplot(np.array(reach500), fit=expon, fit_kws={"color":"blue", "cut":0, "linestyle":'-.', "marker":'v', "markevery":0.1}, kde=False, label='500 RSUs', hist=False)
    sns.distplot(np.array(reach1000), fit=expon, fit_kws={"color":"green", "cut":0, "linestyle":':', "marker":'s', "markevery":0.1}, kde=False, label='1000 RSUs', hist=False)
    plt.hist(reach246, fill=False, alpha=0.3, bins = binarray, density=True, color='red', rwidth=1, histtype='step')
    plt.hist(reach500, fill=False, alpha=0.3, bins = binarray, density=True, color='blue', rwidth=1, histtype='step')
    plt.hist(reach1000, fill=False, alpha=0.3, bins = binarray, density=True, color='green', rwidth=1, histtype='step')

    # sns.distplot(np.array(reach246), kde_kws={"bw":0.3, "cut":0, "linestyle":'--', "marker":'o', "markevery":0.1}, hist=False, label='246 RSU')
    # sns.distplot(np.array(reach500),kde_kws={"bw":0.3, "cut":0, "linestyle":'-.', "marker":'v', "markevery":0.1}, hist=False, label='500 RSU')
    # sns.distplot(np.array(reach1000), kde_kws={"bw":0.3, "cut":0, "linestyle":':', "marker":'1', "markevery":0.1}, hist=False, label='1000 RSU')
    plt.xlabel('% Cars Reached')
    plt.ylabel('Density')
    plt.legend()
    plt.tight_layout(True)
    plt.savefig('graphs/RSUReachPDF.png', dpi=300)

def plotRSUHIST():
    reach246 = loadData("APReachNew_246.txt")
    reach500 = loadData("APReachNew_500.txt")
    reach1000 = loadData("APReachNew_1000.txt")
    plt.figure()
    binum = 50
    x246, c246 = countFloat2(reach246, binum, 5)
    x500, c500 = countFloat2(reach500, binum, 5)
    x1000, c1000 = countFloat2(reach1000, binum, 5)
    avg246 = avg(reach246)
    avg500 = avg(reach500)
    avg1000 = avg(reach1000)
    plt.step(x=x246, y=c246, alpha=0.5, color='#2d84c3', where='post', lw=3)
    plt.step(x=x500, y=c500, alpha=0.5, color='#d19e46', where='post', lw=3)
    plt.step(x=x1000, y=c1000, alpha=0.5, color='#a31e15', where='post', lw=3)
    markx246, marky246 = setMarkerPlace(x246, c246)
    markx500, marky500 = setMarkerPlace(x500, c500)
    markx1000, marky1000 = setMarkerPlace(x1000, c1000)
    plt.scatter(markx246, marky246, marker='o', color='#2d84c3')
    plt.scatter(markx500, marky500, marker='v', color='#d19e46')
    plt.scatter(markx1000, marky1000, marker='s', color='#a31e15')

    plt.axvline(x=10, lw=3, marker='o', color='#2d84c3', label='246 RSUs')
    plt.axvline(x=avg246, ls=':', color='#2d84c3', lw=2, zorder=10, clip_on=False, marker='o', markevery=2, label='average = {:.2f}'.format(avg246))
    plt.axvline(x=10, lw=3, marker='v', color='#d19e46', label='500 RSUs')
    plt.axvline(x=avg500, ls=':', color='#d19e46', lw=2, zorder=10, clip_on=False, marker='v', markevery=2, label='average = {:.2f}'.format(avg500))
    plt.axvline(x=10, lw=3, marker='s', color='#a31e15', label='1000 RSUs')
    plt.axvline(x=avg1000, ls=':', color='#a31e15', lw=2, zorder=10, clip_on=False, marker='s', markevery=2, label='average = {:.2f}'.format(avg1000))
    plt.axis([0, 5, 0, 0.6])
    plt.legend()
    plt.xlabel('\% Cars Reached')
    plt.ylabel('Frequency')
    plt.tight_layout(True)
    plt.savefig('graphs/RSUReachHIST.png', dpi=300)

def plotV2VHIST():
    carsReached = loadData("carsReachSingle.txt")
    multiReach = loadData("carsReachMulti.txt")
    plt.figure()
    binum = 50
    sx, sc = countFloat2(carsReached, binum, 5)
    dx, dc = countFloat2(multiReach, binum, 5)
    avgSingle = avg(carsReached)
    avgDouble = avg(multiReach)
    plt.step(x=sx, y=sc, alpha=0.5, color='#2d84c3', where='post', lw=3)
    plt.step(x=dx, y=dc, alpha=0.5, color='#d19e46', where='post', lw=3)
    smarkx, smarky = setMarkerPlace(sx, sc)
    dmarkx, dmarky = setMarkerPlace(dx, dc)
    plt.scatter(smarkx, smarky, marker='o', color='#2d84c3')
    plt.scatter(dmarkx, dmarky, marker='v', color='#d19e46')
    plt.axvline(x=10, lw=3, marker='o', color='#2d84c3', label='single hop')
    plt.axvline(x=avgSingle, ls=':', color='#2d84c3', lw=2, zorder=10, clip_on=False, marker='o', markevery=2, label='average = {:.2f}'.format(avgSingle))
    plt.axvline(x=10, lw=3, marker='v', color='#d19e46', label='double hop')
    plt.axvline(x=avgDouble, ls=':', color='#d19e46', lw=2, zorder=10, clip_on=False, marker='v', markevery=2, label='average = {:.2f}'.format(avgDouble))
    # fs = interp1d(sx, sc, kind='cubic')
    # fd = interp1d(dx, dc, kind='cubic')
    # sxnew = np.linspace(0, max(sx), num=500, endpoint=True)
    # dxnew = np.linspace(0, max(dx), num=500, endpoint=True)
    # plt.plot(sxnew, fs(sxnew), color='red', label='single hop', lw=2, ls='--', marker='o', markevery=0.1)
    # plt.plot(dxnew, fd(dxnew), color='blue', label='double hop', lw=2, ls='-.', marker='v', markevery=0.1)
    plt.axis([0, 5, 0, 0.6])
    plt.legend()
    plt.xlabel('\% Cars Reached')
    plt.ylabel('Frequency')
    plt.tight_layout(True)
    plt.savefig('graphs/V2VReachHIST.png', dpi=300)

def plotRSUCDF():
    reach246 = loadData("APReachNew_246.txt")
    reach500 = loadData("APReachNew_500.txt")
    reach1000 = loadData("APReachNew_1000.txt")
    plt.figure()
    x246, c246 = countFloat2(reach246, 100, 5)
    x500, c500 = countFloat2(reach500, 100, 5)
    x1000, c1000 = countFloat2(reach1000, 100, 5)
    plt.plot(x246, c246, linewidth=3, linestyle='-', marker='o', label='246 RSUs', markevery=0.1)
    plt.plot(x500, c500, linewidth=3, linestyle='-.', marker='v', label='500 RSUs', markevery=0.1)
    plt.plot(x1000, c1000, linewidth=3, linestyle='--', marker='s', label='1000 RSUs', markevery=0.1)
    # plt.axis([0, 5, 0, 0.35])
    plt.legend()
    plt.xlabel('% Cars Reached')
    plt.ylabel('Density')
    plt.tight_layout(True)
    plt.savefig('graphs/RSUReachCDF.png', dpi=300)

def plotRSUDelay():
    multi_246 = loadData("delayMulti_246.txt")
    single_246 = loadData("delaySingle_246.txt")
    multi_500 = loadData("delayMulti_500.txt")
    single_500 = loadData("delaySingle_500.txt")
    multi_1000 = loadData("delayMulti_1000.txt")
    single_1000 = loadData("delaySingle_1000.txt")
    plt.figure()
    s246, cs246 = countTotal(single_246)
    plt.plot(s246, cs246, linestyle='--', marker='o', label='single hop : 246 RSUs', markevery=0.1)
    s500, cs500 = countTotal(single_500)
    plt.plot(s500, cs500, linestyle='--', marker='v', label='single hop : 500 RSUs', markevery=0.1)
    s1000, cs1000 = countTotal(single_1000)
    plt.plot(s1000, cs1000, linestyle='--', marker='1', label='single hop : 1000 RSUs', markevery=0.1)
    m246, cm246 = countTotal(multi_246)
    plt.plot(m246, cm246, linestyle=':', marker='o', label='double hop : 246 RSUs', markevery=0.1)
    m500, cm500 = countTotal(multi_500)
    plt.plot(m500, cm500, linestyle=':', marker='v', label='double hop : 500 RSUs', markevery=0.1)
    m1000, cm1000 = countTotal(multi_1000)
    plt.plot(m1000, cm1000, linestyle=':', marker='1', label='double hop : 1000 RSUs', markevery=0.1)
    plt.axis([-1, 600, 0, 1])
    plt.legend()
    plt.xlabel('Delay (seconds)')
    plt.ylabel('Cumulative Probability')
    plt.tight_layout(True)
    plt.savefig('graphs/RSUdelayCDF.png', dpi=300)


plotRSUHIST()
plotTimeReach()
plotRSUDelay()
plotV2VHIST()
