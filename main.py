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
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img

img = io.imread('imgs/m1.png', as_gray=True)
#show_images([img])
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
#show_images([binary])
staffLinesThicc, whitespaceLen = getSLsThickness_Whitespaces(binary)
sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
sl = int((sls[0] + sls[1]) / 2)
ws = int((wss[0] + wss[1]) / 2)
rotated=Make_IMG_HORIZONTAL(binary,1)
segmented = SegmentWithMorph(binary,staff_thick=sl,white_spce=ws)
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    firstLine, lastLine = get_StartingEnding_StaffLinePosition(image, ws)
    NoLines=removeLines(image,sl)
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    for symbol in segmentSymbol(NoLines):
        quarterEighthNoteDetection(symbol, firstLine, lastLine, wss[1], sl, ws)
        halfNoteDetection(symbol, firstLine, lastLine, wss, sl, ws)
    #show_images([NoLines])

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)