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
from matplotlib import pyplot as plt
import cv2 as cv2
##################################################TEST ML MODEL#######################################################3333
# run_experiment('raw')
# img_seven=img = cv2.imread("numbers/8_2.png",cv2.IMREAD_GRAYSCALE)
# img_three=img = cv2.imread("numbers/3_1.png",cv2.IMREAD_GRAYSCALE)
# img_three_again=img = cv2.imread("numbers/3_11.png",cv2.IMREAD_GRAYSCALE)
# print(runTest(img_three_again)[0])

# print(runTest(img_three)[0])
# print(runTest(img_seven)[0])
##########################################################################################################################

lines=cv2.imread("imgs/m1.png",cv2.IMREAD_GRAYSCALE)
lines=AdaptiveThresholding(lines)
sls, wss = getSLsThickness_Whitespaces(lines, vertical=True)

imgs=SegmentWithMorph(lines,sls,wss)
NoLines=removeLines(imgs[0], sls)
show_images([imgs[0]])
digits=imgs[0].copy()
digits=digits[:,66:86]
digits=255-digits
digits[digits==255]=1
window=np.ones((3,3))
# digits=binary_dilation(digits,selem=window)
# digits=np.array(digits,dtype=np.uint8)
show_images([digits])
x=[]
staff_height=((4*wss)+(5*sls))
cnts=find_contours(digits,0)
for cnt in cnts:
    yMax = int(np.max(cnt[:,0]))
    yMin = int(np.min(cnt[:,0]))
    if(staff_height/4<(yMax-yMin)<staff_height/2):
        x.append(imgs[0][yMin:yMax,66:86])
print(runTest(x[1]))
print(runTest(x[0]))

show_images(x)
