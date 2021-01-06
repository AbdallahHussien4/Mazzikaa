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

run_experiment('raw')
img_seven=img = cv2.imread("numbers/8_2.png",cv2.IMREAD_GRAYSCALE)
img_three=img = cv2.imread("numbers/3_1.png",cv2.IMREAD_GRAYSCALE)
img_three_again=img = cv2.imread("numbers/3_11.png",cv2.IMREAD_GRAYSCALE)
print(runTest(img_three_again)[0])

print(runTest(img_three)[0])
print(runTest(img_seven)[0])