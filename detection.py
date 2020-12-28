from commonfunctions import np, show_images
from skimage.morphology import binary_opening, binary_closing, binary_erosion
from skimage.draw import rectangle
from skimage.morphology import binary_opening, binary_closing, binary_erosion
from skimage.measure import find_contours
from cv2 import cv2     
from StaffLines import getSLsThickness_Whitespaces

def getShortestDistance(curPos, linesPos):
    minDist = np.sqrt(abs(np.square(curPos) - np.square(linesPos[0])))
    minIndex = 0 
    for index, i in enumerate(linesPos):
        dist = np.sqrt(abs(np.square(curPos) - np.square(i)))
        if dist < minDist:
            minDist = dist
            minIndex = index
    return minIndex

def generateLinesArray(binary, firstLine, lastLine):

    sl, dim = getSLsThickness_Whitespaces(binary)
    linesPos = []
    initLine = firstLine       
    for i in range(10, 0, -1):
        linesPos.append(initLine - (dim / 2 + sl / 2)*i)
    linesPos.append(initLine)
    for i in range(1, 19):
        linesPos.append(initLine + (dim / 2 + sl / 2)*i)

    linesPos2 = []
    initLine = lastLine
    for i in range(18, 0, -1):
        linesPos2.append(initLine - (dim / 2 + sl / 2)*i)
    linesPos2.append(initLine)
    for i in range(1, 11):
        linesPos2.append(initLine + (dim / 2 + sl / 2)*i)

    combined = []
    for i in range(len(linesPos)):
        combined.append((linesPos[i] + linesPos2[i]) / 2)
        
    return combined


def quarterEighthNoteDetection(segmentedSymbol, index, firstLine, lastLine, segStart):
    
    structElementDim = getSLsThickness_Whitespaces(segmentedSymbol, min_max=True)[1][1] # getting max of whitespaces
    
    if structElementDim % 2 == 0:
        structElementDim += 1
    
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (structElementDim, structElementDim))
    
    opened = binary_opening(1 - segmentedSymbol, selem=element)
    contours = find_contours(opened, 0.8)
    for contour in contours:
        Xmin = min(contour[:,1])
        Xmax = max(contour[:,1])
        Ymin = min(contour[:,0])
        Ymax = max(contour[:,0])
        rr, cc = int((Ymax - Ymin) / 2 + Ymin) , int((Xmax - Xmin) / 2 + Xmin) 
        linesPositions = generateLinesArray(segmentedSymbol, firstLine[index], lastLine[index])
        lineIndex = getShortestDistance(rr + segStart[index], linesPositions)
    