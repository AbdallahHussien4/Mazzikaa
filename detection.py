from commonfunctions import np, show_images
from skimage.morphology import binary_opening, binary_closing, binary_erosion, binary_dilation
from skimage.draw import rectangle
from skimage.measure import find_contours
from StaffLines import getSLsThickness_Whitespaces
from scipy.ndimage.morphology import binary_fill_holes
from detectSymbols import matchNoteHead
import cv2
from StaffLines import get_StartingEnding_StaffLinePosition

def getShortestDistance(curPosX, curPosY, linesPos, width,isScanned):

    if not isScanned:
        if curPosX < int(width / 4):
            linesPos = linesPos[0]
        elif curPosX < int(width / 2):
            linesPos = linesPos[1]
        elif curPosX < int(3* width / 4):
            linesPos = linesPos[2]
        else:
            linesPos = linesPos[3]
    minDist = np.sqrt(abs(np.square(curPosY) - np.square(linesPos[0])))
    minIndex = 0
    for index, i in enumerate(linesPos):
        dist = np.sqrt(abs(np.square(curPosY) - np.square(i)))
        if dist < minDist:
            minDist = dist
            minIndex = index
    return minIndex



def generateLinesArray(sl, dim, seg):

    width = seg.shape[1]
    allLines = []
    for i in range(4):

        firstLine, lastLine,seg[:, i * int(width/4) : i * int(width/4) + int(width/4)] = get_StartingEnding_StaffLinePosition(seg[:, i * int(width/4) : i * int(width/4) + int(width/4)], dim,False)

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

        allLines.append(combined)

    return allLines

def scannedGenerateLinesArray(sl, dim, seg):
    firstLine, lastLine,seg = get_StartingEnding_StaffLinePosition(seg, dim,True)
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


def quarterEighthNoteDetection(segmentedSymbol, linesPositions, structElementDimMinMax):

    img = segmentedSymbol.copy()
    img[segmentedSymbol == 255] = 0
    img[segmentedSymbol == 1] = 0
    img[segmentedSymbol == 0] = 1

    Max = structElementDimMinMax[1]
    
    Min = Max - 1

    if Min % 2 == 0:
        Min += 1

    if Max % 2 == 0:
        Max -= 1

    element = np.ones((Max * 4, int(Min/2)))

    opened = binary_opening(img, element)

    element = np.ones((Min * 3, 1))

    opened = binary_opening(img - opened, element)

    minElement = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (Min, Min))

    maxElement = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (Max, Max))

    contours = find_contours(opened, 0.8)

    structElementDim = Max + 2

    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        opened[Ymin: Ymax + structElementDim,
               Xmin - structElementDim: Xmax] = binary_dilation(binary_erosion(img[Ymin: Ymax + structElementDim,
                                                                                   Xmin - structElementDim: Xmax], selem=minElement), selem=maxElement)
        opened[Ymin - structElementDim: Ymax,
               Xmin: Xmax + structElementDim] = binary_dilation(binary_erosion(img[Ymin - structElementDim: Ymax,
                                                                                   Xmin: Xmax + structElementDim], selem=minElement), selem=maxElement)
    matches = matchNoteHead(1 - opened, Min)
    for rr in matches:
        lineIndex = getShortestDistance(rr, 0, linesPositions, 0)


def halfNoteDetection(img, linesPositions, structElementDimMinMax):

    Min = structElementDimMinMax[0]
    Max = structElementDimMinMax[1]

    segmentedSymbol = img.copy()
    # Send Max value of whitespaces
    filled = fillHalfNoteHeads(segmentedSymbol, Max)

    segmentedSymbol[segmentedSymbol == 255] = 1
    filled[filled == 255] = 1

    if Min % 2 == 0:
        Min -= 1

    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (Min, Min))

    opened = np.bitwise_xor(binary_opening(
        1 - segmentedSymbol, selem=element), binary_opening(1 - filled, selem=element))

    contours = find_contours(opened, 0.8)

    for contour in contours:
        Xmin = min(contour[:, 1])
        Xmax = max(contour[:, 1])
        Ymin = min(contour[:, 0])
        Ymax = max(contour[:, 0])

        if Max / 2 > (Xmax - Xmin) - Max >= 0 and Max / 2 > (Ymax - Ymin) - Max >= 0:
            rr = int((Ymax - Ymin) / 2 + Ymin)
            lineIndex = getShortestDistance(rr, 0, linesPositions, 0)


def fillHalfNoteHeads(image, structElementDim):

    img = image.copy()
    img[image == 255] = 0
    img[image == 1] = 0
    img[image == 0] = 1

    if structElementDim % 2 == 0:
        structElementDim -= 1

    element = np.ones((structElementDim * 3, 1))
    opened = binary_opening(img, element)

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (structElementDim, structElementDim))

    contours = find_contours(opened, 0.8)

    structElementDim = int(structElementDim * 2)
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        opened[Ymin - structElementDim: Ymax + structElementDim,
               Xmin - structElementDim: Xmax + structElementDim] = binary_fill_holes(img[Ymin - structElementDim: Ymax + structElementDim,
                                                                                         Xmin - structElementDim: Xmax + structElementDim])
    return np.uint8((1 - opened) * 255)
