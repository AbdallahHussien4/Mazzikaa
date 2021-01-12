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
import cv2 as cv2

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
    14: 'b1',
    15: 'a1',
    16: 'g1',
    17: 'f1',
    18: 'e1',
    19: 'd1',
    20: 'c1'
}

clefPaths = ["clefs/treble_1.jpg", "clefs/treble_2.jpg"]
timePaths = ["Accidentals/4_4.JPG"]
quarterPaths = ["Notes/quarter.JPG", "Notes/quarter2.jpg"]
halfPaths = ["Notes/half1.JPG", "Notes/half2.JPG"]
wholePaths = ["Notes/whole.JPG", "Notes/whole2.JPG", "Notes/whole3.JPG"]
dotPaths = ["Notes/dot.JPG"]
twoDotsPaths = ["Notes/dots.JPG"]
sharpPaths = ["Accidentals/sharp.JPG", "Accidentals/sharp2.JPG" ]#,"Accidentals/sharp-space.png"]
flatPaths = ["Accidentals/flat.JPG"]
doubleSharpPaths = ["Accidentals/doublesharp.JPG"]
flagPaths = ["Flags/flag.JPG"]
doubleFlagPaths = ["Flags/doubleflag.JPG"]
tripleFlagPaths = ["Flags/tripleflag.JPG"]


class TemplateScalingStartPercent(Enum):

    QUARTER_NOTE = 80
    HALF_NOTE = 80
    WHOLE_NOTE = 80
    SHARP = 80
    DOUBLE_SHARP = 80
    FLAT = 80
    DOUBLE_FLAT = 80
    FLAG = 70
    DOUBLE_FLAG = 70
    TRIPLE_FLAG = 70
    DOT = 80
    DOTS = 80
    CLEF = 80
    TIME = 80


class TemplateScalingEndPercent(Enum):

    QUARTER_NOTE = 120
    HALF_NOTE = 120
    WHOLE_NOTE = 120
    SHARP = 120
    DOUBLE_SHARP = 120
    FLAT = 120
    DOUBLE_FLAT = 120
    FLAG = 140
    DOUBLE_FLAG = 140
    TRIPLE_FLAG = 140
    DOT = 120
    DOTS = 120
    CLEF = 120
    TIME = 120


class StaffLinesRatio(Enum):

    BEAMS_lOWER = 3
    BEAMS_UPPER = 9


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
    DOUBLE_FLAG = 3
    TRIPLE_FLAG = 3
    DOT = 0.5
    DOTS = 0.5
    TIME = 4.5


class MatchingThreshold(Enum):
    CLEF = 0.35
    QUARTER_NOTE = 0.65
    HALF_NOTE = 0.6
    WHOLE_NOTE = 0.65
    SHARP = 0.65
    DOUBLE_SHARP = 0.7
    FLAT = 0.7
    DOUBLE_FLAT = 0.7
    FLAG = 0.7
    DOUBLE_FLAG = 0.7
    TRIPLE_FLAG = 0.65
    DOT = 0.7
    DOTS = 0.7
    TIME = 0.5


def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img


def match(img, templates, start_percent=50, stop_percent=150, threshold=0.8):
    best_location_count = -1
    best_locations = []

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
        elif (location_count < best_location_count):
            pass
    return best_locations


##########################################################################################
##########                                                                   #############
##########                                                                   #############
##########                                                                   #############
##########                              NOTES                                #############
##########                                                                   #############
##########                                                                   #############
##########                                                                   #############
##########################################################################################

def matchNotes(binary, sl, ws, linesPositions,isScanned):

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
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        quarters.append(i)
    if ws % 2 == 0:
        ws += 1
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (int(ws/2), int(ws/2)))
    locations = match(binary, quarters, TemplateScalingStartPercent.QUARTER_NOTE.value,
                      TemplateScalingEndPercent.QUARTER_NOTE.value, MatchingThreshold.QUARTER_NOTE.value)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    #show_images([result,binary])
    contours = find_contours(result, 0.8)

    for contour in contours:

        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        Ymin = int(min(contour[:, 0]))
        Ymax = int(max(contour[:, 0]))
        x = int((Xmax + Xmin) / 2)
        y = int((Ymax + Ymin) / 2)

        pos = getShortestDistance(x, y, linesPositions, binary.shape[1],isScanned)
        if pos > 20:
            continue
        #print(pos)
        # TODO Optimization: Don't check all rows in that area, instead, bound it with vertical WS ratio
        sharp = matchSharp(
            binary[:, x-int(ws*HorizontalWhiteSpaceRatio.SHARP.value)-ws:x], ws)
        DoubleSharp = matchDoubleSharp(
            binary[:, x-int(ws*HorizontalWhiteSpaceRatio.DOUBLE_SHARP.value)-ws:x], ws)
        Flat = matchFlat(
            binary[:, x-int(ws*HorizontalWhiteSpaceRatio.DOUBLE_FLAT.value)-ws:x], ws)
        flags = numFlags(binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.FLAG.value)+ws], ws)
        
        Dot = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOT.value)+ws], ws, 1)
        Dots = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOTS.value)+ws], ws, 2)

        note = Note(x, y, positionNotationDict[pos][0], positionNotationDict[pos][1], 4)

        if sharp == 1:
            note.accidental = '#'
        elif DoubleSharp == 1:
            note.accidental = '##'
        elif Flat == 2:
            note.accidental = '&&'
        elif Flat == 1:
            note.accidental = '&'

        note.duration *= 2**flags

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
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        halfs.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, halfs, TemplateScalingStartPercent.HALF_NOTE.value, TemplateScalingEndPercent.HALF_NOTE.value,
                      MatchingThreshold.HALF_NOTE.value)
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

        pos = getShortestDistance(x, y, linesPositions, binary.shape[1],isScanned)
        if pos > 20:
            continue

        note = Note(x, y, positionNotationDict[pos][0], positionNotationDict[pos][1], 2)

        Dot = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOT.value)+ws], ws, 1)
        Dots = matchDots(
            binary[:, x:x+int(ws*HorizontalWhiteSpaceRatio.DOTS.value)+ws], ws, 2)

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
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        wholes.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, wholes, TemplateScalingStartPercent.WHOLE_NOTE.value, TemplateScalingEndPercent.WHOLE_NOTE.value,
                      MatchingThreshold.WHOLE_NOTE.value)
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
        pos = getShortestDistance(x, y, linesPositions, binary.shape[1],isScanned)
        if pos > 20:
            continue
        Notes.append(
            Note(x, y, positionNotationDict[pos][0], positionNotationDict[pos][1], 1))

    Notes.sort(key=lambda x: x.xPosition)

    ###
    # Looking for beams between two quarter notes
    ###
    finished = -1
    entered = False
    for i in range(len(Notes) - 1):
        # Both are quarter and relatively far
        if Notes[i].duration == 4 and Notes[i + 1].duration == 4 and Notes[i + 1].xPosition - Notes[i].xPosition > 1.5 * ws:
            col = (Notes[i].xPosition + Notes[i + 1].xPosition) / 2
            encoded = encodeList(binary[:, int(col)])
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


##################################################
################ Detect Chords ###################
##################################################
    Started = False
    chordStarts = []
    chordEnds = []
    chords = []
    chord = []
    end = -1
    for i in range(len(Notes) - 1):
        if abs(Notes[i].xPosition - Notes[i+1].xPosition) < (ws*1.5):
            if not Started:
                end = i + 1
                Started = True
                chordStarts.append(i)
                chordEnds.append(i+1)
                notation = Notes[i].notation + Notes[i].notationP
                chord.append(notation)
                notation = Notes[i+1].notation + Notes[i+1].notationP
                chord.append(notation)
            else:
                if end == i:
                    chordEnds.pop()
                end = i + 1
                notation = Notes[i+1].notation + Notes[i+1].notationP
                chord.append(notation)
                chordEnds.append(i+1)
        else:
            Started = False
            end = -1
            if len(chord) > 1:
                chords.append(chord)
                chord = []
    if len(chord) > 1:
        chords.append(chord)
    for index, chord in enumerate(chords):
        chord.sort()
        cIndex = 0
        Notes[chordStarts[index]].ChordStart = 1
        for n in range(chordStarts[index], chordEnds[index] + 1):
            Notes[n].notation = chord[cIndex][0]
            Notes[n].notationP = chord[cIndex][1]
            Notes[n].ChordMid = 1
            cIndex += 1
        Notes[chordEnds[index]].ChordEnd = 1

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


def matchClefs(binary, ws,Clear=True):
    clef_imgs = [cv2.imread(clef, 0) for clef in clefPaths]
    clefs = []
    for i in clef_imgs:
        scaleFactor = i.shape[0]/(ws * VerticalWhiteSpaceRatio.CLEF.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        clefs.append(i)
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, clefs, TemplateScalingStartPercent.CLEF.value,
                      TemplateScalingEndPercent.CLEF.value, MatchingThreshold.CLEF.value)
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    hasClef = False
    Xs=[]
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        xCenters = int(((Xmax - Xmin) / 2 + Xmin))
        Xs.append(xCenters)
    if len(Xs)>0:    
        minX=np.min(Xs)    
        if minX < binary.shape[1]/3:
            if Clear:
                binary[:, 0:minX + int((HorizontalWhiteSpaceRatio.CLEF.value*ws))] = 255
            #print("XCenter :" , minX)    
            hasClef = True

    return hasClef
    # show_images([result, binary])

def matchTimeSig(binary, ws):
    time_imgs = [cv2.imread(time, 0) for time in timePaths]
    times = []
    for i in time_imgs:
        scaleFactor = i.shape[0]/(ws * VerticalWhiteSpaceRatio.CLEF.value)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
        times.append(i)
    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, times, TemplateScalingStartPercent.CLEF.value,
                      TemplateScalingEndPercent.TIME.value, MatchingThreshold.TIME.value)
    #show_images([result, binary])
    for i in locations:
        for j in range(len(i[0])):
            result[i[0][j] + int(ws / 2), i[1][j] + int(ws / 2)] = 1
    result = binary_dilation(result, selem=element)
    contours = find_contours(result, 0.8)
    hasTime = False
    for contour in contours:
        Xmin = int(min(contour[:, 1]))
        Xmax = int(max(contour[:, 1]))
        xCenters = int(((Xmax - Xmin) / 2 + Xmin))
        hasTime = True

    return hasTime


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
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        sharps.append(i)
    locations = match(binary, sharps, TemplateScalingStartPercent.SHARP.value, TemplateScalingEndPercent.SHARP.value,
                      MatchingThreshold.SHARP.value)
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
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        flats.append(i)

    result = np.zeros_like(binary, dtype=np.uint8)
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (ws, ws))
    locations = match(binary, flats, TemplateScalingStartPercent.FLAT.value,
                      TemplateScalingEndPercent.FLAT.value, MatchingThreshold.FLAT.value)
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
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        doubleSharps.append(i)

    locations = match(binary, doubleSharps, TemplateScalingStartPercent.DOUBLE_SHARP.value, TemplateScalingEndPercent.DOUBLE_SHARP.value,
                      MatchingThreshold.DOUBLE_SHARP.value)
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
        startPercent = TemplateScalingStartPercent.FLAG.value
        endPercent = TemplateScalingEndPercent.FLAG.value

    elif numFlags == 2:
        flagMatchingThresh = MatchingThreshold.DOUBLE_FLAG.value
        flagVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.DOUBLE_FLAG.value
        mflagPaths = doubleFlagPaths
        startPercent = TemplateScalingStartPercent.DOUBLE_FLAG.value
        endPercent = TemplateScalingEndPercent.DOUBLE_FLAG.value

    else:
        flagMatchingThresh = MatchingThreshold.TRIPLE_FLAG.value
        flagVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.TRIPLE_FLAG.value
        mflagPaths = tripleFlagPaths
        startPercent = TemplateScalingStartPercent.TRIPLE_FLAG.value
        endPercent = TemplateScalingEndPercent.TRIPLE_FLAG.value

    flag_imgs = [cv2.imread(flag, 0) for flag in mflagPaths]

    flags = []
    for i in flag_imgs:
        scaleFactor = i.shape[0]/(ws * flagVerticalWhiteSpaceRatio)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        flags.append(i)

    locations = match(binary, flags, startPercent,
                      endPercent, flagMatchingThresh)
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
        startPercent = TemplateScalingStartPercent.DOT.value
        endPercent = TemplateScalingEndPercent.DOT.value

    else:
        dotMatchingThresh = MatchingThreshold.DOTS.value
        dotVerticalWhiteSpaceRatio = VerticalWhiteSpaceRatio.DOTS.value
        mdotPaths = twoDotsPaths
        startPercent = TemplateScalingStartPercent.DOTS.value
        endPercent = TemplateScalingEndPercent.DOTS.value

    dot_imgs = [cv2.imread(dot, 0) for dot in mdotPaths]

    dots = []
    for i in dot_imgs:
        scaleFactor = i.shape[0]/(ws * dotVerticalWhiteSpaceRatio)
        rows, cols = i.shape
        i = cv2.resize(i, (int(cols / scaleFactor), int(rows / scaleFactor)))
        i = cv2.threshold(i, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]        
        dots.append(i)

    locations = match(binary, dots, startPercent,
                      endPercent, dotMatchingThresh)
    for i in locations:
        if(len(i[0]) > 0):
            return 1
    return 0


def numFlags(binary, ws):

    if matchFlags(binary, ws, 3):
        return 3
    if matchFlags(binary, ws, 2):
        return 2
    if matchFlags(binary, ws, 1):
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
