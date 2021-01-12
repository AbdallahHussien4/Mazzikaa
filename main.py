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
img_dir = "./dummmy/"

for path in os.listdir(img_dir):
    try:
        img = io.imread(img_dir+path,as_gray=True)
        show_images([img])
        isScanned = False
        #Normalize ,binarize and rotate the img
        img = normalizeImage(img)
        binary,isScanned =  binarize(img)

        binary,Angle = Make_IMG_HORIZONTAL(binary)

        binary = normalizeImage(binary)
        binary = binarize(binary)[0]

        if Angle > 90:
                binary = rotate(binary,180,resize=True,mode='constant',cval=1)
                binary = normalizeImage(binary)
                binary = binarize(binary)[0]
        sl, ws = getSLsThickness_Whitespaces(binary, vertical=True)

        #to check existance of clefs after rotation
        # if not matchClefs(binary, ws,False):
        #     binary = rotate(binary,180,resize=True,mode='constant',cval=1)
        #     binary = normalizeImage(binary)
        #     binary = binarize(binary)[0]

        sls, wss = getSLsThickness_Whitespaces(binary, min_max=True)
        #segment img to get every staff lines group
        if isScanned:
            segmented = segmentwithmorph(binary, white_spce=ws, line_thick=sl)
        else:
            segmented = SegmentWithMorphCont(binary, ws, sl)
        numStaffs = len(segmented)
        #start detection of symbols
        f = open("output-tests/"+path[0:2]+'.txt', "w")
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
            #to remove staff lines in every segment    
            removed, p = removeLines(seg, sls[1])
            #match all notes and its neighbours
            Notes = matchNotes(removed, sl, ws, linesPositions,isScanned)
            #localize digits if there is any
            if len(Notes) >0:
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
        # f = open("output-tests/"+path[0:2]+'.txt','r')
        # str1 = f.read()

        # f = open(r"Mo3ed/"+path[0:2]+'.txt')
        # str2 = f.read()
        # print(' ')
        # print(path[0:2], ":  ", SequenceMatcher(
        #     lambda x: x == " ", str1, str2).ratio() * 100)
        # print(' ')
    except:
        f.write('\n}')
        continue    
