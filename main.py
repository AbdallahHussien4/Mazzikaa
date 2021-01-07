from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import *
from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
from detection import quarterEighthNoteDetection, fillHalfNoteHeads
# from digitsDetection import *
# from digitsClassifier import *
from cv2 import cv2
from TemplateMatching import *
from skimage.morphology import skeletonize

def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img

img = cv2.imread(r'PublicTestCases\test-set-scanned\test-cases\05.PNG', 0)
img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
# eighth = []
# for i in eighth_flag_imgs:
#     image = normalizeImage(i)
#     retval, image = cv2.threshold(image, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#     eighth.append(image)
# compare = io.imread('quarter.png', as_gray=True)
# compare = normalizeImage(compare)
# binary_compare = AdaptiveThresholding(compare)
# for_numer=cv2.imread('imgs/m1.png')
#for_numer = normalizeImage(for_numer)
#for_numer = AdaptiveThresholding(for_numer)
# show_images([img])
img = normalizeImage(img)
retval, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
#binary = AdaptiveThresholding(img)
sl, ws = getSLsThickness_Whitespaces(binary, vertical=True)
sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
removeLines(binary, sls[1])
print(ws*2.5)
matchNotes(binary,ws)

# run_experiment('raw')
# img_seven=img = cv2.imread("numbers/8_2.png",cv2.IMREAD_GRAYSCALE)
# img_three=img = cv2.imread("numbers/3_1.png",cv2.IMREAD_GRAYSCALE)
# img_three_again=img = cv2.imread("3.png",cv2.IMREAD_GRAYSCALE)
# print(runTest(img_three_again))

# #show_images([binary])
# # staffLinesThicc, whitespaceLen = getSLsThickness_Whitespaces(binary, vertical=True)
# # sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
# # sl = int((sls[0] + sls[1]) / 2)
# # ws = int((wss[0] + wss[1]) / 2)
# # rotated=Make_IMG_HORIZONTAL(binary,1)
# #segmented = SegmentWithMorph(binary,staff_thick=staffLinesThicc,white_spce=whitespaceLen)

# # for image in segmented:
# # removedLineImgs.append(removeLines(image,staffLinesThicc))
# #firstLine, lastLine = get_StartingEnding_StaffLinePosition(image, whitespaceLen)
# #linesPositions = generateLinesArray(staffLinesThicc, whitespaceLen, firstLine, lastLine)
# #halfNoteDetection(image, linesPositions, (whitespaceLen, whitespaceLen))
# #quarterEighthNoteDetection(image, linesPositions, (whitespaceLen, whitespaceLen))
# #NoLines=removeLines(segmented[1], sls[1])

# # detectDigits(NoLines[:,60:90],binary[:,60:90])
# # show_images([NoLines[:,60:90]])
# # show_images([NoLines])
# # Symbols.append(segmentSymbol(NoLines))
# # show_images(segmentSymbol(NoLines))
# # for symbol in segmentSymbol(binary):
# #     #quarterEighthNoteDetection(symbol, linesPositions, whitespaceLen)
# #     show_images([symbol])
# #halfNoteDetection(symbol, linesPositions, wss)
# # show_images([NoLines])

# # show_images(removedLineImgs[count])
# #quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)
