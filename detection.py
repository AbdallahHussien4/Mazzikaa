from commonfunctions import np, show_images
from skimage.morphology import binary_opening, binary_closing, binary_erosion, binary_dilation
from skimage.draw import rectangle
from skimage.measure import find_contours
from cv2 import cv2
from StaffLines import getSLsThickness_Whitespaces
from scipy.ndimage.morphology import binary_fill_holes


def getShortestDistance(curPos, linesPos):
    minDist = np.sqrt(abs(np.square(curPos) - np.square(linesPos[0])))
    minIndex = 0
    for index, i in enumerate(linesPos):
        dist = np.sqrt(abs(np.square(curPos) - np.square(i)))
        if dist < minDist:
            minDist = dist
            minIndex = index
    return minIndex


def generateLinesArray(sl, dim, firstLine, lastLine):

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


def quarterEighthNoteDetection(segmentedSymbol, linesPositions, structElementDim):

    segmentedSymbol[segmentedSymbol == 255] = 1
    if structElementDim % 2 == 0:
        structElementDim -= 1

    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (structElementDim, structElementDim))

    opened = binary_opening(1 - segmentedSymbol, selem=element)
    contours = find_contours(opened, 0.8)
    for contour in contours:
        Ymin = min(contour[:, 0])
        Ymax = max(contour[:, 0])
        rr = int((Ymax - Ymin) / 2 + Ymin)
        lineIndex = getShortestDistance(rr, linesPositions)
        # print(lineIndex)



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

    # show_images([binary_opening(1 - segmentedSymbol, selem=element), binary_opening(1 - filled, selem=element)])
    contours = find_contours(opened, 0.8)

    for contour in contours:
        Xmin = min(contour[:, 1])
        Xmax = max(contour[:, 1])
        Ymin = min(contour[:, 0])
        Ymax = max(contour[:, 0])

        if Max / 2 > (Xmax - Xmin) - Max >= 0 and Max / 2 > (Ymax - Ymin) - Max >= 0:
            rr = int((Ymax - Ymin) / 2 + Ymin)
            lineIndex = getShortestDistance(rr, linesPositions)
            print("half:", lineIndex)

    # show_images([opened])


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
    #show_images([img, opened])
    return np.uint8((1 - opened) * 255)
