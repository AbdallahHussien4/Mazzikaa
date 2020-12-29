from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import * 
#from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
from detection import quarterEighthNoteDetection

def normalizeImage(img):
    if(img.max() == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/m1.png', as_gray=True)
show_images([img])
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
#show_images([binary])
staffLinesThicc, whitespaceLen = getSLsThickness_Whitespaces(binary)
#staffLinesThicc = staffLinesThiccs[1]
#whitespaceLen = whitespaceLens[1]
print(staffLinesThicc, whitespaceLen)
#rotated=Make_IMG_HORIZONTAL(binary,1)
#show_images([rotated])
#rotated[rotated==255]=1
binary[binary==255]=1
segmented, firstLine, lastLine, segStart=segmentLines(binary)
removedLineImgs=[]
Symbols=[]
structElementDim = getSLsThickness_Whitespaces(binary, min_max=True)[1][1]
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    image[image==1]=255
    NoLines=removeLines(image,staffLinesThicc)
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    for symbol in segmentSymbol(NoLines):
        symbol[symbol==255]=1
        quarterEighthNoteDetection(symbol, index, firstLine, lastLine, segStart, structElementDim, staffLinesThicc, whitespaceLen)
    show_images([NoLines])

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)