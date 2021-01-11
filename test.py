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
import math
from operator import itemgetter
##################################################TEST ML MODEL#######################################################3333
run_experiment('hog')
# img_seven=img = cv2.imread("numbers/8_2.png",cv2.IMREAD_GRAYSCALE)
img_three=img = cv2.imread("numbers/4_10.png",cv2.IMREAD_GRAYSCALE)
#img_three_again=img = cv2.imread("numbers/3_11.png",cv2.IMREAD_GRAYSCALE)
# print(runTest(img_three_again)[0])

print(runTest(img_three)[0])
# print(runTest(img_seven)[0])
##########################################################################################################################

# # lines=cv2.imread("imgs/m1.png",cv2.IMREAD_GRAYSCALE)
# # lines=AdaptiveThresholding(lines)
# # sls, wss = getSLsThickness_Whitespaces(lines, vertical=True)

# # imgs=SegmentWithMorph(lines,sls,wss)
# # NoLines=removeLines(imgs[0], sls)
# # show_images([imgs[0]])
# # digits=imgs[0].copy()
# # digits=digits[:,66:86]
# # digits=255-digits
# # digits[digits==255]=1
# # window=np.ones((3,3))
# # digits=binary_dilation(digits,selem=window)
# # digits=np.array(digits,dtype=np.uint8)
# # show_images([digits])
# # x=[]
# # staff_height=((4*wss)+(5*sls))
# # cnts=find_contours(digits,0)
# # for cnt in cnts:
# #     yMax = int(np.max(cnt[:,0]))
# #     yMin = int(np.min(cnt[:,0]))
# #     if(staff_height/4<(yMax-yMin)<staff_height/2):
# #         x.append(imgs[0][yMin:yMax,66:86])
# # print(runTest(x[1]))
# # print(runTest(x[0]))

# # show_images(x)
# rotated=cv2.imread("PublicTestCases/test-set-camera-captured/test-cases/19.jpg",cv2.IMREAD_GRAYSCALE)
# retval, binary = cv2.threshold(rotated, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# show_images([rotated])
# binary=255-binary
# orig=binary.copy()
# horizontal_size = rotated.shape[1] // 30
# window=np.ones((horizontal_size,1))

# binary=binary_dilation(binary,selem=window)

# # rotated=255-rotated
# show_images([binary])
# binary=np.array(binary,dtype=np.uint8)
# contours,hierarchy = cv2.findContours(binary, 1, 2)
# max_area =0
# cnt=[]
# for contour in contours:
#     area = cv2.contourArea(contour)
#     if(area>max_area):
#         max_area=area
#         cnt = contour
        
# rect = cv2.minAreaRect(cnt)
# box = cv2.boxPoints(rect)

# print(box.shape)
# sorted_x=sorted(box, key=itemgetter(0))
# print(sorted_x)
# if(sorted_x[0][1]<sorted_x[1][1]):
#     top_left=sorted_x[0]
#     bottom_left=sorted_x[1]
# else:
#     top_left=sorted_x[1]
#     bottom_left=sorted_x[0]

# if(sorted_x[2][1]<sorted_x[3][1]):
#     top_right=sorted_x[2]
#     bottom_right=sorted_x[3]
# else:
#     top_right=sorted_x[3]
#     bottom_right=sorted_x[2]


# # print(top_left,top_right,bottom_left,bottom_right)
# # print(box[2],box[3],box[1],box[0])
# #pts1=np.float32([box[2],box[3],box[1],box[0]])
# pts1=np.float32([top_left,top_right,bottom_left,bottom_right])
# print(pts1)
# pts2 = np.float32([[0,0],[binary.shape[1],0],[0,binary.shape[0]],[binary.shape[1],binary.shape[0]]])
# M = cv2.getPerspectiveTransform(pts1,pts2)
# perspectiv = cv2.warpPerspective(orig,M,(binary.shape[1],binary.shape[0]))
# #perspectiv=cv2.resize(perspectiv,(1000,1000))
# show_images([255-perspectiv])

