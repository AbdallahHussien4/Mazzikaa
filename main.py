from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import * 
#from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
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
rotated=Make_IMG_HORIZONTAL(binary,1)
#show_images([rotated])
rotated[rotated==255]=1
segmented=SegmentWithMorph(rotated)
#show_images([segmented[0]])
removedLineImgs=[]
Symbols=[]
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    image[image==1]=255
    NoLines=removeLines(image,staffLinesThicc)
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    show_images(SegmentSymbolMorph(NoLines))

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)