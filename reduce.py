
import xml.etree.ElementTree as ET


def readTraces(traceFile):
    traces = [] # list with traces
    tree = ET.parse(traceFile)
    root = tree.getroot()
    timeID = 0
    for second in root.iter('timestep'):
        traces.append(Time(float(second.get('time'))))
        if not second:
            print("timestep empty")
        else:
            for car in second.iter('vehicle'):
                traces[timeID].cars.append(Car(car.get('id'), float(car.get('x')), float(car.get('y'))))
        timeID += 1
    return traces
