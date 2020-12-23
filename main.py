from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import * 
from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
def normalizeImage(img):
    if(img.max() == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/m1.jpg', as_gray=True)
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
#show_images([binary])
staffLinesThicc, whitespaceLen = getSLsThickness_WhiteSpaces(binary)
rotated=Make_IMG_HORIZONTAL(binary,1)
#show_images([rotated])
segmented=segmentLines(rotated)
#show_images([segmented[0]])
removedLineImgs=[]
Symbols=[]
for image in segmented:
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    NoLines=removeLines(image,staffLinesThicc)
    Symbols.append(segmentSymbol(NoLines))
    show_images(segmentSymbol(NoLines))

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)