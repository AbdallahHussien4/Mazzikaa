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
from digitsDetection import *
from digitsClassifier import *
import cv2 as cv2
from TemplateMatching import matchNotes, matchClefs, matchTimeSig
from skimage.morphology import skeletonize
from digitsDetection import detectDigits
from difflib import ndiff, SequenceMatcher
from perspective import getPerspective
import os 
import glob 

# r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\11.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\12.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\13.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\14.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\15.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\16.jpg',


# ,
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\27.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\28.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\29.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\30.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\31.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\32.jpg',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\01.PNG',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\02.png',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\03.png',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\04.PNG',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\05.png',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\06.png',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\07.PNG',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\08.png',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\09.png',
#          r'PublicTestCases-version1.1\test-set-scanned\test-cases\10.png',
#          r'imgs/m1.png',
#          r'imgs/m2.jpg',
#          r'imgs/m3.jpg'

# tests = [r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\17.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\18.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\19.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\20.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\21.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\22.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\23.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\24.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\25.jpg',
#          r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\26.jpg']

#img_dir = "PublicTestCases-version1.1\test-set-camera-captured\test-cases"
img_dir = "./dummy/"
for path in os.listdir(img_dir):
    img = io.imread(img_dir+path,as_gray=True)
    # scannedTests = [r'PublicTestCases-version1.1\test-set-camera-captured\test-cases\12.jpg']

    # outs = ['12.txt', '02.txt', '03.txt', '04.txt', '05.txt',
    #         '06.txt', '07.txt', '08.txt', '09.txt', '10.txt']

    # outs = ['20.txt', '18.txt', '19.txt', '20.txt', '21.txt',
    #         '22.txt', '23.txt', '24.txt', '25.txt', '26.txt']


    isScanned = False
    #img = cv2.imread(r'PublicTestCases-version1.1\test-set-scanned\test-cases\10.PNG', 0)
    #Normalize ,binarize and rotate the img
    img = normalizeImage(img)
    binary,isScanned =  binarize(img)

    binary = Make_IMG_HORIZONTAL(binary)

    binary = normalizeImage(binary)
    binary = binarize(binary)[0]

    show_images([binary])

    sl, ws = getSLsThickness_Whitespaces(binary, vertical=True)

    #show_images([binary])

    #to check existance of clefs after rotation
    if not matchClefs(binary, ws,False):
        binary = rotate(binary,180,resize=True,mode='constant',cval=1)
        binary = normalizeImage(binary)
        binary = binarize(binary)[0]

    sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
    #segment img to get every staff lines group
    print(isScanned)
    if isScanned:
        segmented = segmentwithmorph(binary, white_spce=ws, line_thick=sl)
    else:
        segmented = SegmentWithMorphCont(binary, ws, sl)

    numStaffs = len(segmented)
    #start detection of symbols
    f = open("output-tests/12.txt", "w")
    if numStaffs > 1:
        f.write('{\n')
    last = False
    for index, seg in enumerate(segmented):
        #detect and delete the clef
        matchClefs(seg, ws)
        #to get position for every line in the segment
        if isScanned:
            linesPositions = scannedGenerateLinesArray(sl, ws, seg)
        else:
            linesPositions = generateLinesArray(sl, ws, seg)
        show_images([seg])
        #to remove staff lines in every segment    
        removed, p = removeLines(seg, sls[1])
        #match all notes and its neighbours
        Notes = matchNotes(removed, sl, ws, linesPositions,isScanned)
        #localize digits if there is any
        if Notes[0].accidental != '':
            localizeCheck=localize_digits(removed,Notes[0].xPosition - ws,ws)
        else:
            localizeCheck=localize_digits(removed,Notes[0].xPosition,ws)
        #if there are digits apply ML model to classify them
        if(localizeCheck!= None):
            digit1,digit2=detectDigits(localizeCheck[0],seg,ws,sl,localizeCheck[1],localizeCheck[2])
            if digit1 != 1:
                f.write('[ \meter<"'+ digit1 + '/' + digit2 + '"> ')
            else:
                f.write('[ ')
        else:
            f.write('[ ')
        if index == len(segmented) - 1:
            last = True
        #loop for every note and print its output
        GenerateOutput(Notes, f, last)
    if numStaffs > 1:
        f.write('\n}')
    #generate accuracy percentage
    f = open("output-tests/12.txt")
    str1 = f.read()

    f = open(r"PublicTestCases-version1.1/test-set-camera-captured/gt/12.txt")
    str2 = f.read()
    print(' ')
    print("12.txt"[0:2], ":  ", SequenceMatcher(
        lambda x: x == " ", str1, str2).ratio() * 100)
        #diff = ndiff(str1, str2)
        #print(''.join(diff), end="")
    print(' ')
