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
from difflib import ndiff, SequenceMatcher


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

scannedTests = [r'PublicTestCases-version1.1\test-set-scanned\test-cases\01.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\02.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\03.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\04.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\05.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\06.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\07.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\08.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\09.PNG', 
                r'PublicTestCases-version1.1\test-set-scanned\test-cases\10.PNG']

outs = ['01.txt', '02.txt', '03.txt', '04.txt', '05.txt', '06.txt', '07.txt', '08.txt', '09.txt', '10.txt']

def binarize(img, ratioOfPeakGLVal=1/5, grayLevelsThreshold=10):

    binary = cv2.threshold(img, 0, 1, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]
    imgSize = img.shape[0] * img.shape[1]
    blackPixelsPercentage = histogram(binary, nbins=2)[0][0].sum() / imgSize * 100
    
    numGrayLevels = 0
    hist = histogram(img, nbins=256)
    pixelsThreshold = hist[0].max() * ratioOfPeakGLVal
    for i in hist[0]:
        if i > pixelsThreshold:
            numGrayLevels += 1
    if numGrayLevels >= grayLevelsThreshold and blackPixelsPercentage >= 10:
        return AdaptiveThresholding(img)

    return cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1]

def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img

# fImages=[]
# images = [cv2.imread(img, 0) for img in tests]
# for image in images:
#     #fImages.append(cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)[1])
#     #fImages.append(AdaptiveThresholding(image))
#     show_images([binarize(image)])

for i, path in enumerate(scannedTests):

    try:
        img = cv2.imread(path, 0)
        #img = cv2.fastNlMeansDenoising(img, None, 10, 7, 21)
        #show_images([img])
        img = normalizeImage(img)
        binary = binarize(img)
        sl, ws = getSLsThickness_Whitespaces(binary, vertical=True)
        sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
        segmented = segmentwithmorph(binary, white_spce=ws, line_thick=sl)
        numStaffs = len(segmented)
        f = open("output-tests/" + outs[i], "w")
        if numStaffs > 1:
            f.write('{\n')
        last = False
        for index, seg in enumerate(segmented):
            firstLine, lastLine = get_StartingEnding_StaffLinePosition(seg, ws)
            linesPositions = generateLinesArray(sl, ws, firstLine, lastLine)
            #quarterEighthNoteDetection(seg, linesPositions, (ws, ws))
            #halfNoteDetection(seg, linesPositions, (ws, ws))
            removed,p = removeLines(seg, sls[1])
            matchClefs(removed,ws)
            Notes = matchNotes(removed, sl, ws, linesPositions)
            if Notes[0].accidental != '':
                localizeCheck=localize_digits(removed,Notes[0].xPosition - ws,ws)
            else:
                localizeCheck=localize_digits(removed,Notes[0].xPosition,ws)
            if(localizeCheck!= None):
                digit1,digit2=detectDigits(localizeCheck[0],seg,ws,sl,localizeCheck[1],localizeCheck[2])
                f.write('[ \meter<"'+digit1[0]+'/'+digit2[0]+'"> ')
            else:
                f.write('[ ')
            if index == len(segmented) - 1:
                last = True
            GenerateOutput(Notes, f, last)
            # for i in Notes:
            #     print(i)
        if numStaffs > 1:
            f.write('}')
        try:
            f = open("output-tests/" + outs[i])
            str1 = f.read()
        except :
            continue
        f = open("PublicTestCases-version1.1/test-set-scanned/gt/" + outs[i])
        str2 = f.read()
        print(' ')
        print(outs[i][0:2], ":  ", SequenceMatcher(None, str1, str2).ratio() * 100)
        #diff = ndiff(str1, str2)
        #print(''.join(diff), end="")
        print(' ')

    except:
        continue

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
