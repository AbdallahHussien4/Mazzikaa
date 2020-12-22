import numpy as np
import matplotlib.pyplot as plt
from itertools import groupby

def countFrequency(my_list): 
    freq = {} 
    for item in my_list: 
        if (item in freq): 
            freq[item] += 1
        else: 
            freq[item] = 1
    return freq

def getMostCommon(aList):
    freq = countFrequency(aList)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sortedFreq[0][0]
    
def getMostCommonMinMax(aList):
    freq = countFrequency(aList)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    mMin=sortedFreq[0][0]
    mMax=sortedFreq[0][0]
    ref = sortedFreq[0][0]
    for i in sortedFreq:
        if abs(i[0] - ref) > 10 or i[0] == 0:
            continue
        if(i[0] < mMin):
            mMin = i[0]
        if(i[0] > mMax):
            mMax = i[0]
    return mMin, mMax


# Takes a binary image as an input
# Returns the staff lines thickness and whitespace between each two lines respectively as a tuple
# If min_max is set to True, it returns min and max values for the lines thickness and space

def getSLsThickness_WhiteSpaces(binary, min_max=False, showHist=False):

    height = (binary.shape)[0]
    maBlackList = np.zeros(height, dtype=np.uint32)
    staffLinesWidth = np.empty(1, dtype=np.uint32)
    distBetweenStaffs = np.empty(1, dtype=np.uint32)

    sW = 0
    sB = 0
    for row in range(height - 1):
        maBlackList[row] = (binary[row, :] == 0).sum()

    sumThreshold = int(0.7 * max(maBlackList))
    for row in range(height - 1):
        sumBlack = (binary[row, :] == 0).sum()
        if sumBlack > sumThreshold:
            if sW != 0:
                distBetweenStaffs = np.append(distBetweenStaffs, sW)
                sW = 0
            sB += 1
        else:
            if sB != 0:
                staffLinesWidth = np.append(staffLinesWidth, sB)
                sB = 0
            sW += 1
    
    if showHist:
        x = np.arange(height)
        plt.figure(figsize =(10, 7)) 
        plt.plot(x, maBlackList)
        plt.show()
    
    if min_max:
        return getMostCommonMinMax(staffLinesWidth), getMostCommon(distBetweenStaffs)
    return getMostCommon(staffLinesWidth), getMostCommon(distBetweenStaffs)
