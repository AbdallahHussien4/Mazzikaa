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

# lines=cv2.imread("imgs/m1.png",cv2.IMREAD_GRAYSCALE)
# lines=AdaptiveThresholding(lines)
# sls, wss = getSLsThickness_Whitespaces(lines, vertical=True)

# imgs=SegmentWithMorph(lines,sls,wss)
# NoLines=removeLines(imgs[0], sls)
# show_images([imgs[0]])
# digits=imgs[0].copy()
# digits=digits[:,66:86]
# digits=255-digits
# digits[digits==255]=1
# window=np.ones((3,3))
# digits=binary_dilation(digits,selem=window)
# digits=np.array(digits,dtype=np.uint8)
# show_images([digits])
# x=[]
# staff_height=((4*wss)+(5*sls))
# cnts=find_contours(digits,0)
# for cnt in cnts:
#     yMax = int(np.max(cnt[:,0]))
#     yMin = int(np.min(cnt[:,0]))
#     if(staff_height/4<(yMax-yMin)<staff_height/2):
#         x.append(imgs[0][yMin:yMax,66:86])
# print(runTest(x[1]))
# print(runTest(x[0]))

# show_images(x)
rotated=cv2.imread("PublicTestCases/test-set-camera-captured/test-cases/25.jpg",cv2.IMREAD_GRAYSCALE)
#rotated=deskew(img)
show_images([rotated])
before=rotated.copy()
rotated=AdaptiveThresholding(rotated,15)
rotated=255-rotated
horizontal_size = rotated.shape[1] // 30
window=np.ones((1,horizontal_size))
window2=np.ones((20,20))

rotated=binary_erosion(rotated,selem=window)
rotated=binary_dilation(rotated,selem=window)
rotated=binary_dilation(rotated,selem=window2)
rotated=1-rotated
black_hist=np.zeros((rotated.shape[0],1))
show_images([rotated])
for row in range(0,rotated.shape[0]):
    black_hist[row,0]=(rotated[row, :] == 0).sum()
black_lines=np.where(black_hist>=int(0.1*rotated.shape[1]))
start=int(black_lines[0][0])
end=int(black_lines[0][-1])
startY=start-50
endY=end+50
black_hist=np.zeros((1,rotated.shape[1]))
for col in range(0,rotated.shape[1]):
    black_hist[0,col]=(rotated[:, col] == 0).sum()

black_lines=np.where(black_hist>=30)
startX=int(black_lines[1][0])
endX=int(black_lines[1][-1])+50
show_images([before[startY:endY,startX:endX],before])
