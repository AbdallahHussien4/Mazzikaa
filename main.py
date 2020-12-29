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
    if(img.max() == 1):
        return np.uint16(img * 255)
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
#show_images([rotated])
segmented = SegmentWithMorph(binary,staff_thick=staffLinesThicc,white_spce=whitespaceLen)
removedLineImgs=[]
Symbols=[]
structElementDim = getSLsThickness_Whitespaces(binary, min_max=True)[1][1]
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    firstLine, lastLine = get_StartingEnding_StaffLinePosition(image, whitespaceLen)
    NoLines=removeLines(image,staffLinesThicc)
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    halfNoteDetection(image, firstLine, lastLine, structElementDim, wss, sl, ws)
    for symbol in segmentSymbol(NoLines):
        quarterEighthNoteDetection(symbol, firstLine, lastLine, structElementDim, sl, ws)
    #show_images([image])

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)