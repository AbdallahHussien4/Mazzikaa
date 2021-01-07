from cv2 import cv2
import numpy as np
import skimage.io as io
from RemoveLines import removeLines
from skimage.morphology import binary_opening, binary_erosion, binary_dilation
from StaffLines import getSLsThickness_Whitespaces, get_StartingEnding_StaffLinePosition, encodeList
from commonfunctions import show_images
from skimage.measure import find_contours
from enum import Enum
from Note import Note
from detection import getShortestDistance

positionNotationDict = {
    0: 'b3',
    1: 'a3',
    2: 'g3',
    3: 'f3',
    4: 'e3',
    5: 'd3',
    6: 'c3',
    7: 'b2',
    8: 'a2',
    9: 'g2',
    10: 'f2',
    11: 'e2',
    12: 'd2',
    13: 'c2',
    14: 'b',
    15: 'a',
    16: 'g',
    17: 'f',
    18: 'e',
    19: 'd',
    20: 'c'
}

quarterPaths = ["Notes/quarter.jpg"]
halfPaths = ["Notes/half1.jpg", "Notes/half2.jpg"]
wholePaths = ["Notes/whole.jpg"]
sharpPaths = ["Accidentals/sharp.jpg"]
flatPaths = ["Accidentals/flat.jpg"]
doubleSharpPaths = ["Accidentals/doublesharp.jpg"]
flagPaths = ["Flags/flag.jpg"]
doubleFlagPaths = ["Flags/doubleflag.jpg"]
tripleFlagPaths = ["Flags/tripleflag.jpg"]


class HorizontalWhiteSpaceRatio(Enum):

    SHARP = 1
    DOUBLE_SHARP = 1.1
    FLAT = 1
    DOUBLE_FLAT = 2
    FLAG = 1
    DOUBLE_FLAG = 1.2
    TRIPLE_FLAG = 1.1

class StaffLinesRatio(Enum):

    BEAMS_lOWER = 3
    BEAMS_UPPER = 8

class VerticalWhiteSpaceRatio(Enum):

    QUARTER_NOTE = 1
    HALF_NOTE = 1
    WHOLE_NOTE = 1
    SHARP = 2.5
    DOUBLE_SHARP = 1
    FLAT = 2.5
    DOUBLE_FLAT = 2
    FLAG = 3
    DOUBLE_FLAG = 3.5
    TRIPLE_FLAG = 4

class MatchingThreshold(Enum):

    QUARTER_NOTE = 0.7
    HALF_NOTE = 0.7
    WHOLE_NOTE = 0.7
    SHARP = 0.7
    DOUBLE_SHARP = 0.7
    FLAT = 0.7
    DOUBLE_FLAT = 0.7
    FLAG = 0.7
    DOUBLE_FLAG = 0.7
    TRIPLE_FLAG = 0.7


def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img


def match(img, templates, start_percent=50, stop_percent=150, threshold=0.8):
    best_location_count = -1
    best_locations = []
    best_scale = 1

    for scale in [i/100.0 for i in range(start_percent, stop_percent + 1, 3)]:
        locations = []
        location_count = 0

        for template in templates:
            if (scale*template.shape[0] > img.shape[0] or scale*template.shape[1] > img.shape[1]):
                continue

            template = cv2.resize(template, None,
                                  fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            result = np.where(result >= threshold)
            location_count += len(result[0])
            locations += [result]

        if (location_count > best_location_count):
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
        elif (location_count < best_location_count):
            pass
    return best_locations, best_scale


##########################################################################################
##########                                                                   #############
##########                                                                   #############
##########                                                                   #############
##########                              NOTES                                #############
##########                                                                   #############
##########                                                                   #############
##########                                                                   #############
##########################################################################################

def matchNotes(binary, sl, ws, linesPositions):

    Notes = []

######################################################################
#                                                                    #
#                          QUARTER NOTES                             #
#                                                                    #
######################################################################
    ws += 1

    quarter_imgs = [cv2.imread(quarter, 0) for quarter in quarterPaths]

    quarters = []
    for i in quarter_imgs:
        scaleFactor = i.shape[0] / \
            (ws * VerticalWhiteSpaceRatio.QUARTER_NOTE.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        quarters.append(i)
    if ws % 2 == 0:
        ws += 1
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, quarters, 50, 150,
                      MatchingThreshold.QUARTER_NOTE.value)[0]
    # print(locations)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)

    for contour in contours:

        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        x = int((Xmax - Xmin) / 2 + Xmin)
        y = int((Ymax - Ymin) / 2 + Ymin)
        pos = getShortestDistance(y, linesPositions)

        # TODO Don't check all rows in that area, instead, bound it with vertical WS ratio
        sharp = matchSharp(
            binary[:, x-int(ws*HorizontalWhiteSpaceRatio.SHARP.value)-ws:x], ws)
        DoubleSharp = matchDoubleSharp(
            binary[:, x-int(ws*HorizontalWhiteSpaceRatio.DOUBLE_SHARP.value)-ws:x], ws)
        Flat = matchFlat(
            binary[:, x-int(ws*HorizontalWhiteSpaceRatio.DOUBLE_FLAT.value)-ws:x], ws)
        Flag1 = matchFlags(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.FLAG.value)+ws], ws, 1)
        Flag2 = matchFlags(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOUBLE_FLAG.value)+ws], ws, 2)
        Flag3 = matchFlags(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.TRIPLE_FLAG.value)+ws], ws, 3)
        note = Note(x, y, positionNotationDict[pos], 4)

        if sharp == 1:
            note.accidental = '#'
        elif DoubleSharp == 1:
            note.accidental = '##'
        elif Flat == 2:
            note.accidental = '&&'
        elif Flat == 1:
            note.accidental = '&'

        if Flag3 == 1:
            note.duration *= 8
        elif Flag2 == 1:
            note.duration *= 4
        elif Flag1 == 1:
            note.duration *= 2

        Notes.append(note)

    #print(xCenters, yCenters)
    # print(xCenters)
    #binary[binary == 255] = 1
    #result2 = np.bitwise_or(binary, result)
    # show_images([result2])
    # TODO build an array of quarter notes containing their positions
    #show_images([result, binary])


######################################################################
#                                                                    #
#                          HALF NOTES                                #
#                                                                    #
######################################################################

    half_imgs = [cv2.imread(half, 0) for half in halfPaths]

    halfs = []
    for i in half_imgs:
        scaleFactor = i.shape[0]/(ws * VerticalWhiteSpaceRatio.HALF_NOTE.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        halfs.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, halfs, 70, 140,
                      MatchingThreshold.HALF_NOTE.value)[0]
    # print(locations)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    xCenters = []
    yCenters = []
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        xCenters.append((Xmax - Xmin) / 2 + Xmin)
        yCenters.append((Ymax - Ymin) / 2 + Ymin)

    for i in range(len(xCenters)):
        pos = getShortestDistance(yCenters[i], linesPositions)
        Notes.append(Note(xCenters[i], yCenters[i],
                          positionNotationDict[pos], 2))


######################################################################
#                                                                    #
#                          WHOLE NOTES                               #
#                                                                    #
######################################################################
#
    whole_imgs = [cv2.imread(whole, 0) for whole in wholePaths]

    wholes = []
    for i in whole_imgs:
        scaleFactor = i.shape[0] / \
            (ws * VerticalWhiteSpaceRatio.WHOLE_NOTE.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        wholes.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, wholes, 70, 140,
                      MatchingThreshold.WHOLE_NOTE.value)[0]
    # print(locations)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    xCenters = []
    yCenters = []
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        pos = getShortestDistance((Ymax - Ymin) / 2 + Ymin, linesPositions)
        Notes.append(Note((Xmax - Xmin) / 2 + Xmin, (Ymax - Ymin) / 2 + Ymin,
                          positionNotationDict[pos], 1))


    Notes.sort(key=lambda x: x.xPosition)

    ###
    # Looking for beams between two quarter notes
    ###
    finished = -1
    entered = False
    for i in range(len(Notes) - 1):
        # Both are quarter
        if Notes[i].duration == 4 and Notes[i + 1].duration == 4:
            col = (Notes[i].xPosition + Notes[i + 1].xPosition) / 2
            encoded = encodeList(binary[:, int(col)])
            print('From', i, 'to', i+1, encoded)
            for x, y in encoded:
                if y == 0:
                    if sl * StaffLinesRatio.BEAMS_lOWER.value < x < sl *StaffLinesRatio.BEAMS_UPPER.value:
                        if finished != i:
                            Notes[i].numBeams += 1
                        Notes[i+1].numBeams += 1
                        entered = True
            if entered:
                finished = i + 1
                entered = False

    for note in Notes:
        note.duration *= 2**note.numBeams

    return Notes


##############################################################################################
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
#############                          ACCIDENTALS                              ##############
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
##############################################################################################

######################################################################
#                                                                    #
#                               SHARPS                               #
#                                                                    #
######################################################################

def matchSharp(binary, ws):
    sharp_imgs = [cv2.imread(sharp, 0) for sharp in sharpPaths]
    sharps = []
    for i in sharp_imgs:
        scaleFactor = i.shape[0]/(ws * VerticalWhiteSpaceRatio.SHARP.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        #print(int(cols / scaleFactor)+ws)
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        sharps.append(i)
    if ws % 2 == 0:
        ws += 1
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, sharps, 70, 140,
                      MatchingThreshold.SHARP.value)[0]
    # print(locations)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    xCenters = []
    yCenters = []
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        xCenters.append((Xmax - Xmin) / 2 + Xmin)
        yCenters.append((Ymax - Ymin) / 2 + Ymin)
    # print(xCenters, yCenters)
    # print(len(xCenters))
    #binary[binary == 255] = 1
    #result2 = np.bitwise_or(binary, result)
    # show_images([result2])
    # TODO build an array of sharps containing their positions
    # show_images([result])
    if(len(xCenters) > 0):
        return 1
    return 0

######################################################################
#                                                                    #
#                               FLATS                                #
#                                                                    #
######################################################################


def matchFlat(binary, ws):
    flat_imgs = [cv2.imread(flat, 0) for flat in flatPaths]

    flats = []
    for i in flat_imgs:
        scaleFactor = i.shape[0]/(ws * VerticalWhiteSpaceRatio.FLAT.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        flats.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    # TODO if we match more templates then send them all and check all locations
    locations = match(binary, flats, 70, 140, MatchingThreshold.FLAT.value)[0]
    # print(locations)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    xCenters = []
    yCenters = []
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        xCenters.append((Xmax - Xmin) / 2 + Xmin)
        yCenters.append((Ymax - Ymin) / 2 + Ymin)
        if(abs(Xmax-Xmin-HorizontalWhiteSpaceRatio.FLAT.value*ws) < abs(Xmax-Xmin-HorizontalWhiteSpaceRatio.DOUBLE_FLAT.value*ws)):
            return 1
        else:
            return 2
    # print(xCenters, yCenters)
    # print(len(xCenters))
    #binary[binary == 255] = 1
    #result2 = np.bitwise_or(binary, result)
    # TODO build an array of half notes containing their positions
    # show_images([result])
    if(len(xCenters) > 0):
        return 1
    return 0


######################################################################
#                                                                    #
#                          DOUBLE SHARPS                             #
#                                                                    #
######################################################################
def matchDoubleSharp(binary, ws):
    doubleSharp_imgs = [cv2.imread(doubleSharp, 0)
                        for doubleSharp in doubleSharpPaths]

    doubleSharps = []
    for i in doubleSharp_imgs:
        scaleFactor = i.shape[0] / \
            (ws * VerticalWhiteSpaceRatio.DOUBLE_SHARP.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        doubleSharps.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, doubleSharps, 70, 140,
                      MatchingThreshold.DOUBLE_SHARP.value)[0]
    # print(locations)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    xCenters = []
    yCenters = []
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        xCenters.append((Xmax - Xmin) / 2 + Xmin)
        yCenters.append((Ymax - Ymin) / 2 + Ymin)
    # print(xCenters, yCenters)
    # print(len(xCenters))
    #binary[binary == 255] = 1
    #result2 = np.bitwise_or(binary, result)
    # show_images([result])
    if(len(xCenters) > 0):
        return 1
    return 0
    # TODO build an array of half notes containing their positions


##############################################################################################
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
#############                          FLAGS                                    ##############
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
##############################################################################################

def matchFlags(binary, ws, numFlags=1):

    if numFlags == 1:
        flagMatchingThresh = MatchingThreshold.FLAG.value
        flagVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.FLAG.value
        mflagPaths = flagPaths
    elif numFlags == 2:
        flagMatchingThresh = MatchingThreshold.DOUBLE_FLAG.value
        flagVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.DOUBLE_FLAG.value
        mflagPaths = doubleFlagPaths
    else:
        flagMatchingThresh = MatchingThreshold.TRIPLE_FLAG.value
        flagVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.TRIPLE_FLAG.value
        mflagPaths = tripleFlagPaths

    flag_imgs = [cv2.imread(flag, 0) for flag in mflagPaths]

    flags = []
    for i in flag_imgs:
        scaleFactor = i.shape[0]/(ws * flagVerticalWhiteSpaceRatio)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        flags.append(i)
    if ws % 2 == 0:
        ws += 1
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, flags, 70, 140, flagMatchingThresh)[0]
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)

    # print(xCenters, yCenters)
    # print(len(xCenters))
    #binary[binary == 255] = 1
    #result2 = np.bitwise_or(binary, result)
    # show_images([result2])
    # show_images([result])
    if(len(contours) > 0):
        return 1
    return 0
