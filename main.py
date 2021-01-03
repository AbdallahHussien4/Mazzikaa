from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import * 
from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
from detection import quarterEighthNoteDetection, fillHalfNoteHeads
from digitsDetection import *
from digitsClassifier import *
def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img

img = io.imread('imgs/m1.png', as_gray=True)
#for_numer=cv2.imread('imgs/m1.png')
#for_numer = normalizeImage(for_numer)
#for_numer = AdaptiveThresholding(for_numer)
#show_images([img])
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
run_experiment('raw')
img_four=img = cv2.imread("numbers/4_0.png",cv2.IMREAD_GRAYSCALE)
img_three=img = cv2.imread("numbers/3_1.png",cv2.IMREAD_GRAYSCALE)
img_three_again=img = cv2.imread("3.png",cv2.IMREAD_GRAYSCALE)
print(runTest(img_three_again))

print(runTest(img_three))
print(runTest(img_four))
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
    linesPositions = generateLinesArray(sl, ws, firstLine, lastLine)
    halfNoteDetection(image, linesPositions, wss)
    quarterEighthNoteDetection(image, linesPositions, ws)
    NoLines=removeLines(image, sls[1])
    detectDigits(NoLines[:,60:90],binary[:,60:90])
    show_images([NoLines[:,60:90]])
    #show_images([NoLines])
    # Symbols.append(segmentSymbol(NoLines))
    # show_images(segmentSymbol(NoLines))
    for symbol in segmentSymbol(NoLines):
        quarterEighthNoteDetection(symbol, linesPositions, ws)
        #halfNoteDetection(symbol, linesPositions, wss)
    #show_images([NoLines])

#show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)


