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

clefPaths = ["clefs/treble_1.jpg", "clefs/treble_2.jpg"]
quarterPaths = ["Notes/quarter.jpg","Notes/quarter2.jpg"]
halfPaths = ["Notes/half1.jpg", "Notes/half2.jpg"]
wholePaths = ["Notes/whole.jpg", "Notes/whole2.jpg", "Notes/whole3.jpg"]
dotPaths = ["Notes/dot.jpg"]
twoDotsPaths = ["Notes/dots.jpg"]
sharpPaths = ["Accidentals/sharp.jpg", "Accidentals/sharp2.jpg"]
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
    DOT = 1
    DOTS = 2
    CLEF = 2.7


class StaffLinesRatio(Enum):

    BEAMS_lOWER = 3
    BEAMS_UPPER = 7


class VerticalWhiteSpaceRatio(Enum):

    CLEF = 8
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
    DOT = 0.5
    DOTS = 0.5


class MatchingThreshold(Enum):
    CLEF = 0.4
    QUARTER_NOTE = 0.7
    HALF_NOTE = 0.6
    WHOLE_NOTE = 0.65
    SHARP = 0.65
    DOUBLE_SHARP = 0.7
    FLAT = 0.7
    DOUBLE_FLAT = 0.7
    FLAG = 0.7
    DOUBLE_FLAG = 0.7
    TRIPLE_FLAG = 0.65
    DOT = 0.8
    DOTS = 0.8


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
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(ws/2), int(ws/2)))
    locations = match(binary, quarters, 50, 150,MatchingThreshold.QUARTER_NOTE.value)[0]
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    show_images([result,binary])
    contours = find_contours(result, 0.8)

    for contour in contours:

        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        x = int((Xmax + Xmin) / 2)
        y = int((Ymax + Ymin) / 2)
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
        Dot = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOT.value)+ws], ws, 1)
        Dots = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOTS.value)+ws], ws, 2)

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

        if Dots:
            note.numDots = 2
        elif Dot:
            note.numDots = 1

        Notes.append(note)


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
        x = int((Xmax + Xmin) / 2)
        y = int((Ymax + Ymin) / 2)
        pos = getShortestDistance(y, linesPositions)

        Dot = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOT.value)+ws], ws, 1)
        Dots = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOTS.value)+ws], ws, 2)
        
        note = Note(x, y, positionNotationDict[pos], 2)
        
        if Dots:
            note.numDots = 2
        elif Dot:
            note.numDots = 1

        Notes.append(note)


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
        xCenter = (Xmax + Xmin) / 2
        yCenter = (Ymax + Ymin) / 2
        pos = getShortestDistance(yCenter, linesPositions)
        Notes.append(Note(xCenter, yCenter,
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
            #print(encoded)
            for x, y in encoded:
                if y == 0:
                    if sl * StaffLinesRatio.BEAMS_lOWER.value < x < sl * StaffLinesRatio.BEAMS_UPPER.value:
                        if finished != i:
                            Notes[i].numBeams += 1
                        Notes[i+1].numBeams += 1
                        entered = True
            if entered:
                finished = i + 1
                entered = False

    for note in Notes:
        note.duration *= 2**note.numBeams

    # for i in range(len(Notes) - 1):
    #     if Notes[i].xPosition == Notes[i+1].xPosition and i+2<len(Notes) and abs(Notes[i+2].xPosition-Notes[i].xPosition)>2*ws*VerticalWhiteSpaceRatio.QUARTER_NOTE.value and abs(Notes[i].yPosition -Notes[i+1].yPosition)>ws*VerticalWhiteSpaceRatio.QUARTER_NOTE.value:
    #         #print(VerticalWhiteSpaceRatio.QUARTER_NOTE.value,Notes[i].yPosition -Notes[i+1].yPosition,ws,abs(Notes[i+2].xPosition-Notes[i].xPosition))
    #         y=(Notes[i].yPosition+Notes[i+1].yPosition)/2
    #         pos = getShortestDistance(y, linesPositions)
    #         Notes.append(Note(Notes[i].xPosition, y,positionNotationDict[pos], 1))   

    # Notes.sort(key=lambda x: x.xPosition)
    return Notes

##############################################################################################
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
#############                          clefs                                    ##############
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
##############################################################################################


def matchClefs(binary, ws):
    clef_imgs = [cv2.imread(clef, 0) for clef in clefPaths]
    clefs = []
    for i in clef_imgs:
        scaleFactor = i.shape[0]/(ws * VerticalWhiteSpaceRatio.CLEF.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        clefs.append(i)
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, clefs, 50, 150, MatchingThreshold.CLEF.value)[0]
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
        xCenters = int(((Xmax - Xmin) / 2 + Xmin))
        yCenters = int(((Ymax - Ymin) / 2 + Ymin))
        binary[yCenters:yCenters+int((VerticalWhiteSpaceRatio.CLEF.value*ws)),
               xCenters-ws:xCenters+int((HorizontalWhiteSpaceRatio.CLEF.value*ws))] = 255

    # show_images([result, binary])


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
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        sharps.append(i)
    locations = match(binary, sharps, 70, 140,
                      MatchingThreshold.SHARP.value)[0]
    for i in locations:
        if(len(i[0]) > 0):
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
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        if(abs(Xmax-Xmin-HorizontalWhiteSpaceRatio.FLAT.value*ws) < abs(Xmax-Xmin-HorizontalWhiteSpaceRatio.DOUBLE_FLAT.value*ws)):
            return 1
        else:
            return 2


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

    locations = match(binary, doubleSharps, 70, 140,
                      MatchingThreshold.DOUBLE_SHARP.value)[0]
    for i in locations:
        if(len(i[0]) > 0):
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

    locations = match(binary, flags, 70, 140, flagMatchingThresh)[0]
    for i in locations:
        if(len(i[0]) > 0):
            return 1
    return 0


##############################################################################################
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
#############                            DOTS                                   ##############
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
##############################################################################################

def matchDots(binary, ws, numDots=1):

    if numDots == 1:
        dotMatchingThresh = MatchingThreshold.DOT.value
        dotVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.DOT.value
        mdotPaths = dotPaths
    else:
        dotMatchingThresh = MatchingThreshold.DOTS.value
        dotVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.DOTS.value
        mdotPaths = twoDotsPaths

    dot_imgs = [cv2.imread(dot, 0) for dot in mdotPaths]

    dots = []
    for i in dot_imgs:
        scaleFactor = i.shape[0]/(ws * dotVerticalWhiteSpaceRatio)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        dots.append(i)

    locations = match(binary, dots, 70, 140, dotMatchingThresh)[0]
    for i in locations:
        if(len(i[0]) > 0):
            return 1
    return 0


##############################################################################################
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
#############                            DEBUGGING                              ##############
#############                                                                   ##############
#############                                                                   ##############
#############                                                                   ##############
##############################################################################################

    # if ws % 2 == 0:
    #     ws += 1
    # result = np.zeros_like(binary, dtype=np.uint8)
    # element = cv2.getStructuringElement(
    #     cv2.MORPH_ELLIPSE, (ws, ws))
    # locations = match(binary, sharps, 70, 140,
    #                   MatchingThreshold.SHARP.value)[0]
    # for i in locations:
    #     for j in range(len(i[0])):
    #         result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    # result = binary_dilation(result, selem=element)
    # contours = find_contours(result, 0.8)

    # if(len(contours) > 0):
    #     return 1
    # return 0
