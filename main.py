from commonfunctions import*
from skimage.filters import*
from StaffLines import *
from Preprocessing import *
from detection import *
from segmentation import*
from MakeImgHorizontal import *
from RemoveLines import *
from detection import quarterEighthNoteDetection, fillHalfNoteHeads
from GenerateOutput import *
from LocalizeDigits import localize_digits
# from digitsDetection import *
# from digitsClassifier import *
import cv2 as cv2
from TemplateMatching import matchNotes, matchClefs
from skimage.morphology import skeletonize
from digitsDetection import detectDigits


tests = [r'PublicTestCases\test-set-camera-captured\test-cases\12.jpg', 
         r'PublicTestCases\test-set-camera-captured\test-cases\13.jpg', 
         r'PublicTestCases\test-set-camera-captured\test-cases\16.jpg', 
         r'PublicTestCases\test-set-camera-captured\test-cases\17.jpg', 
         r'PublicTestCases\test-set-camera-captured\test-cases\20.jpg', 
         r'PublicTestCases\test-set-camera-captured\test-cases\30.jpg', 
         r'PublicTestCases\test-set-scanned\test-cases\01.PNG', 
         r'PublicTestCases\test-set-scanned\test-cases\02.png', 
         r'PublicTestCases\test-set-scanned\test-cases\04.png', 
         r'imgs/m2.jpg', 
         r'imgs/m3.jpg']

def show_image_in_freq(img, f):
    img_in_freq = fftpack.fft2(img)
    
    show_images([img,
                fftpack.fftshift(np.log(np.abs(img_in_freq)+1)) # log for better intensity scale,
                ], ['Image', 'Image in Freq. Domain'])

def binarize(img, ratioOfPeakGLVal=1/5, grayLevelsThreshold=10):

    binary = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    imgSize = img.shape[0] * img.shape[1]
    blackPixelsPercentage = histogram(binary, nbins=2)[0][0].sum() / imgSize * 100
    print(blackPixelsPercentage)
    
    numGrayLevels = 0
    hist = histogram(img, nbins=256)
    pixelsThreshold = hist[0].max() * ratioOfPeakGLVal
    #print(pixelsThreshold)
    for i in hist[0]:
        if i > pixelsThreshold:
            numGrayLevels += 1
    #print(numGrayLevels)
    if numGrayLevels >= grayLevelsThreshold and blackPixelsPercentage >= 10:
        print('Solly')
        return AdaptiveThresholding(img)

    print('Otsu')
    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img

fImages=[]
images = [cv2.imread(img, 0) for img in tests]
for image in images:
    #fImages.append(cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
    #fImages.append(AdaptiveThresholding(image))
    show_images([binarize(image)])

img = cv2.imread(r'PublicTestCases\test-set-scanned\test-cases\02.png', 0)
#img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
show_images([img])
img = normalizeImage(img)
retval, binary = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
sl, ws = getSLsThickness_Whitespaces(binary, vertical=True)
sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
segmented = segmentwithmorph(binary, white_spce=ws, line_thick=sl)
f = open("testOut.txt", "w")

for seg in segmented:
    firstLine, lastLine = get_StartingEnding_StaffLinePosition(seg, ws)
    linesPositions = generateLinesArray(sl, ws, firstLine, lastLine)
    #quarterEighthNoteDetection(seg, linesPositions, (ws, ws))
    #halfNoteDetection(seg, linesPositions, (ws, ws))
    removed,p = removeLines(seg, sls[1])
    removed,x,y=matchClefs(removed,ws)
    Notes = matchNotes(removed, sl, ws, linesPositions)
    localizeCheck=localize_digits(removed,Notes[0].xPosition,ws)
    if(localizeCheck!= None):
        digit1,digit2=detectDigits(localizeCheck[0],seg,ws,sl,localizeCheck[1],localizeCheck[2])
        f.write('[\meter<"'+digit1[0]+'/'+digit2[0]+'">')
    GenerateOutput(Notes,f)
    # for i in Notes:
    #     print(i)
    #show_images([seg])
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
