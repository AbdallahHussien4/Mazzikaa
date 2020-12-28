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

def getMostCommonHorizontally(aList):
    freq = countFrequency(aList)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sortedFreq[0][0]
    
def getMostCommonMinMaxHorizontally(aList):
    freq = countFrequency(aList)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    mMin = sortedFreq[0][0]
    mMax = sortedFreq[0][0]
    ref = sortedFreq[0][0]
    for i in sortedFreq:
        diff = abs(i[0] - ref)
        if 1 <= ref <= 3: 
            if diff > 3 or i[0] == 0:
                continue
            if(i[0] < mMin):
                mMin = i[0]
            if(i[0] > mMax):
                mMax = i[0]
        elif 4 <= ref <= 15:
            if diff > int(ref/2):
                continue
            if(i[0] < mMin):
                mMin = i[0]
            if(i[0] > mMax):
                mMax = i[0]
        else:
            if diff > 10:
                continue
            if(i[0] < mMin):
                mMin = i[0]
            if(i[0] > mMax):
                mMax = i[0]
    return mMin, mMax

def getSLsThickness_WhiteSpacesHorizontally(binary, min_max=False, show_hist=False):

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
    
    if show_hist:
        x = np.arange(height)
        plt.figure(figsize =(10, 7)) 
        plt.plot(x, maBlackList)
        plt.show()
    
    if min_max:
        return getMostCommonMinMaxHorizontally(staffLinesWidth), getMostCommonMinMaxHorizontally(distBetweenStaffs)
    return getMostCommonHorizontally(staffLinesWidth), getMostCommonHorizontally(distBetweenStaffs)

def encodeList(s_list):
    return [[len(list(group)), key] for key, group in groupby(s_list)]

def getMostCommonVertically(rle_list):
    freq = countFrequency(rle_list)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    return sortedFreq[0][0]

def getMostCommonMinMaxVertically(rle_list):
    topFive = np.empty(1, dtype=np.uint32)
    freq = countFrequency(rle_list)
    sortedFreq = sorted(freq.items(), key=lambda x: x[1], reverse=True)
    topFive = sortedFreq[0:5]
    mMin = sortedFreq[0][0]
    mMax = sortedFreq[0][0]
    ref = sortedFreq[0][0]
    for i in topFive:
        diff = abs(i[0] - ref)
        if 1 <= ref <= 3: 
            if diff > 3 or i[0] == 0:
                continue
            if(i[0] < mMin):
                mMin = i[0]
            if(i[0] > mMax):
                mMax = i[0]
        elif 4 <= ref <= 15:
            if diff > int(ref/2):
                continue
            if(i[0] < mMin):
                mMin = i[0]
            if(i[0] > mMax):
                mMax = i[0]
        else:
            if diff > 10:
                continue
            if(i[0] < mMin):
                mMin = i[0]
            if(i[0] > mMax):
                mMax = i[0]
    return mMin, mMax

def getSLsThickness_WhiteSpacesVertically(binary, min_max=False):

    distBetweenStaffs = np.empty(1, dtype=np.uint32)
    staffLinesWidth = np.empty(1, dtype=np.uint32)
    width = binary.shape[1]
    for col in range(width):
        lista = encodeList(binary[:, col])
        for x, y in lista:
            if(y == 1):
                distBetweenStaffs = np.append(distBetweenStaffs, x)
            else:
                staffLinesWidth = np.append(staffLinesWidth, x)
    if min_max:
        return getMostCommonMinMaxVertically(staffLinesWidth), getMostCommonMinMaxVertically(distBetweenStaffs)
    return getMostCommonVertically(staffLinesWidth), getMostCommonVertically(distBetweenStaffs)

# Takes a binary image as an input
# Returns the staff lines thickness and whitespace between each two lines respectively as a tuple
# If min_max is set to True, it returns min and max values for the lines thickness and space

def getSLsThickness_Whitespaces(binary, min_max=False, vertical=False, horizontal=False, show_hist=False):
    if min_max:
        SLs1, WS1 = getSLsThickness_WhiteSpacesHorizontally(binary, min_max=True)
        SLs2, WS2 = getSLsThickness_WhiteSpacesVertically(binary, min_max=True)
        minSL = min(SLs1[0], SLs2[0])
        maxSL = max(SLs1[1], SLs2[1])
        minWS = min(WS1[0], WS2[0])
        maxWS = max(WS1[1], WS2[1])
        SL = minSL, maxSL
        WS = minWS, maxWS
        return SL, WS
    if vertical:
        return getSLsThickness_WhiteSpacesVertically(binary, show_hist)
    if horizontal:
        return getSLsThickness_WhiteSpacesHorizontally(binary, show_hist=show_hist)
    SlWs1 = getSLsThickness_WhiteSpacesHorizontally(binary)
    SlWs2 = getSLsThickness_WhiteSpacesVertically(binary)
    print(SlWs1, SlWs2)
    return int((SlWs1[0] + SlWs2[0]) / 2), int((SlWs1[1] + SlWs2[1]) / 2)
    