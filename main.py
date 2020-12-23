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

img = io.imread('imgs/score_2.jpg', as_gray=True)
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
rotated=Make_IMG_HORIZONTAL(binary,1)
staffLinesThicc, whitespaceLen = getSLsThickness_WhiteSpaces(rotated)
segmented=segmentLines(rotated)
removedLineImgs=[]
count=0
for image in segmented:
    removedLineImgs.append(removeLines(img,staffLinesThicc))
    show_images(removedLineImgs[count])
    count+=1
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)