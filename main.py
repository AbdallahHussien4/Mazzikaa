from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import * 
from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
from detection import quarterEighthNoteDetection, fillHalfNoteHeads

def normalizeImage(img):

    leftSpan = img.max() - img.min()
    rightSpan = 255 - 0
    img -= img.min()
    img /= float(leftSpan)
    img *= rightSpan
    return np.uint8(img)

img = io.imread('imgs/m0.PNG', as_gray=True)
#show_images([img])
img = normalizeImage(img)
#show_images([img])
binary = AdaptiveThresholding(img)
staffLinesThicc, whitespaceLen = getSLsThickness_Whitespaces(binary)
print(staffLinesThicc, whitespaceLen)
sls, wss = getSLsThickness_Whitespaces(binary, vertical=True, min_max=True)
print(sls, wss)
sl = int((sls[0] + sls[1]) / 2)
ws = int((wss[0] + wss[1]) / 2)
rotated=Make_IMG_HORIZONTAL(binary,1)
#show_images([rotated])
segmented = SegmentWithMorph(binary,staff_thick=sl,white_spce=ws)
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    firstLine, lastLine = get_StartingEnding_StaffLinePosition(image, ws)  # Whitespace is just sent for relativity doesn't matter which one
    linesPositions = generateLinesArray(staffLinesThicc, whitespaceLen, firstLine, lastLine)
    halfNoteDetection(image, linesPositions, wss)
    quarterEighthNoteDetection(image, linesPositions, (whitespaceLen, whitespaceLen))
    NoLines=removeLines(image, sls[1])
    #quarterEighthNoteDetection(image, linesPositions, wss)
    #show_images([NoLines])
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    #for symbol in segmentSymbol(NoLines):
     #   quarterEighthNoteDetection(symbol, linesPositions, wss)
        #halfNoteDetection(symbol, linesPositions, wss)
    print(" ")
    #show_images([NoLines])
#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)