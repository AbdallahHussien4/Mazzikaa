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
import cv2 as cv2
from TemplateMatching import match

flag_paths = [  "flags/eighth_flag_1.jpg",
                "flags/eighth_flag_2.jpg",
                "flags/eighth_flag_3.jpg",
                "flags/eighth_flag_4.jpg",
                "flags/eighth_flag_5.jpg",
                "flags/eighth_flag_6.jpg"]

sharp_paths = [
    "imgs/sharp-line.png", 
    "imgs/sharp-space.png"
] 

quarters = ["quarter.png", "solid-note.png"]
def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img

eighth_flag_imgs = [ io.imread(flag, as_gray=True) for flag in flag_paths]

img = io.imread('imgs/score_10.jpg', as_gray=True)
eighth = []
for i in eighth_flag_imgs:
    image = normalizeImage(i)
    retval, image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    eighth.append(image)
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
result = np.zeros_like(binary)
element = cv2.getStructuringElement(
    cv2.MORPH_ELLIPSE, (15, 15))
locations = match(binary, eighth, 50, 150, 0.65)[0]
print(locations)
for i in locations:
    for j in range(len(i[0])):
        result[i[0][j], i[1][j]] = 1
result = binary_dilation(result, selem=element)
contours = find_contours(result, 0.8)
xCenters = []
yCenters = []
for contour in contours:
    Xmin = int(min(contour[:, 1]))
    Xmax = int(max(contour[:, 1]))
    Ymin = int(min(contour[:, 0]))
    Ymax = int(max(contour[:, 0]))
    xCenters.append((Xmax - Xmin) / 2 + Xmin)
    yCenters.append((Ymax - Ymin) / 2 + Ymin)
print(xCenters, yCenters)
print(len(xCenters))
show_images([binary, result])

#show_images([binary])
# staffLinesThicc, whitespaceLen = getSLsThickness_Whitespaces(binary, vertical=True)
# sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
# sl = int((sls[0] + sls[1]) / 2)
# ws = int((wss[0] + wss[1]) / 2)
# rotated=Make_IMG_HORIZONTAL(binary,1)
#segmented = SegmentWithMorph(binary,staff_thick=staffLinesThicc,white_spce=whitespaceLen)

# for image in segmented:
# removedLineImgs.append(removeLines(image,staffLinesThicc))
#firstLine, lastLine = get_StartingEnding_StaffLinePosition(image, whitespaceLen)
#linesPositions = generateLinesArray(staffLinesThicc, whitespaceLen, firstLine, lastLine)
#halfNoteDetection(image, linesPositions, (whitespaceLen, whitespaceLen))
#quarterEighthNoteDetection(image, linesPositions, (whitespaceLen, whitespaceLen))
#NoLines=removeLines(segmented[1], sls[1])

# detectDigits(NoLines[:,60:90],binary[:,60:90])
# show_images([NoLines[:,60:90]])
# show_images([NoLines])
# Symbols.append(segmentSymbol(NoLines))
# show_images(segmentSymbol(NoLines))
# for symbol in segmentSymbol(binary):
#     #quarterEighthNoteDetection(symbol, linesPositions, whitespaceLen)
#     show_images([symbol])
#halfNoteDetection(symbol, linesPositions, wss)
# show_images([NoLines])

# show_images(removedLineImgs[count])
#quarterEighthNoteDetection(binary, staffLinesThicc, whitespaceLen)
