from commonfunctions import io, show_images, np
from StaffLines import getSLsThickness_WhiteSpaces
from Preprocessing import AdaptiveThresholding
from detection import quarterEighthNoteDetection
from segmentation import segmentLines, segmentSymbol
from RemoveLines import removeLines
from MakeImgHorizontal import Make_IMG_HORIZONTAL

def normalizeImage(img):
    if(img.max() == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/m3.jpg', as_gray=True)
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
show_images([binary])
rotated=Make_IMG_HORIZONTAL(binary,1)
show_images([rotated])
staffLinesThicc, whitespaceLen = getSLsThickness_WhiteSpaces(rotated, showHist=True)
segmented=segmentLines(binary)
removedLineImgs=[]
for image in segmented:
    removedLineImgs.append(removeLines(image,staffLinesThicc))
#show_images(removedLineImgs)
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)