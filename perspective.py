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

def getPerspective(binary):
    binary=255-binary
    orig=binary.copy()

    horizontal_size = binary.shape[1] // 10
    window=np.ones((horizontal_size,1))
    binary=binary_dilation(binary,selem=window)
    binary=np.array(binary,dtype=np.uint8)
    contours,hierarchy = cv2.findContours(binary, 1, 2)
    cnt=[]
    for contour in contours:
        area = cv2.contourArea(contour)
        if(area>max_area):
            max_area=area
            cnt = contour       
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    sorted_x=sorted(box, key=itemgetter(0))
    if(sorted_x[0][1]<sorted_x[1][1]):
        top_left=sorted_x[0]
        bottom_left=sorted_x[1]
    else:
        top_left=sorted_x[1]
        bottom_left=sorted_x[0]

    if(sorted_x[2][1]<sorted_x[3][1]):
        top_right=sorted_x[2]
        bottom_right=sorted_x[3]
    else:
        top_right=sorted_x[3]
        bottom_right=sorted_x[2]

    pts1=np.float32([top_left,top_right,bottom_left,bottom_right])
    pts2 = np.float32([[0,0],[binary.shape[1],0],[0,binary.shape[0]],[binary.shape[1],binary.shape[0]]])
    M = cv2.getPerspectiveTransform(pts1,pts2)
    perspectiv = cv2.warpPerspective(orig,M,(binary.shape[1],binary.shape[0]))
    show_images([255-perspectiv])
    return perspectiv
