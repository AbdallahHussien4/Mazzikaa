from commonfunctions import io, show_images, np
from StaffLines import getSLsThickness_Whitespaces
from Preprocessing import AdaptiveThresholding
from detection import quarterEighthNoteDetection
from segmentation import segmentLines, segmentSymbol
from RemoveLines import removeLines
from MakeImgHorizontal import Make_IMG_HORIZONTAL

def normalizeImage(img):
    if(img.max() == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/m1.jpg', as_gray=True)
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
#show_images([binary])
staffLinesThicc, whitespaceLen = getSLsThickness_Whitespaces(binary)
rotated=Make_IMG_HORIZONTAL(binary,1)
#show_images([rotated])
segmented=segmentLines(rotated)
#show_images([segmented[0]])
removedLineImgs=[]
Symbols=[]
for index, image in enumerate(segmented):
    #removedLineImgs.append(removeLines(image,staffLinesThicc))
    NoLines=removeLines(image,staffLinesThicc)
    Symbols.append(segmentSymbol(NoLines))
    show_images(segmentSymbol(NoLines))

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)