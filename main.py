from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import * 
from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
from detection import quarterEighthNoteDetection

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
rotated=Make_IMG_HORIZONTAL(binary,1)
#show_images([rotated])
segmented,firstLine, lastLine, segStart=SegmentWithMorph(binary)
removedLineImgs=[]
Symbols=[]
structElementDim = getSLsThickness_Whitespaces(binary, min_max=True)[1][1]
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    NoLines=removeLines(image,staffLinesThicc)
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    for symbol in segmentSymbol(NoLines):
        quarterEighthNoteDetection(symbol, index, firstLine, lastLine, segStart, structElementDim, staffLinesThicc, whitespaceLen)
    show_images([NoLines])

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)