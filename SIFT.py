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

def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img


binary = cv2.imread('corner.png', 0)
#img = cv2.imread('3.png', 0)

binary_compare=cv2.imread('symbols/flag2_nolines.png',0)
binary_compare=normalizeImage(binary_compare)
#binary_compare=AdaptiveThresholding(binary_compare)
binary = normalizeImage(binary)
binary=sobel(binary)
binary_compare=sobel(binary_compare)
binary=np.array(binary*255,dtype=np.uint8)
binary_compare=np.array(binary_compare*255,dtype=np.uint8)

show_images([binary,binary_compare])
print(binary_compare.shape)
#binary = AdaptiveThresholding(binary)
sift=cv2.SIFT_create()
#orb = cv2.ORB_create()
show_images([255*binary_compare,255*binary])
kp_1,desc_1=sift.detectAndCompute(binary_compare,None)
kp_2,desc_2=sift.detectAndCompute(binary,None)
print(len(kp_1))
print(len(kp_2))

# index_params = dict(algorithm=0, trees=5)
# search_params = dict()
#flann = cv2.FlannBasedMatcher(index_params, search_params)
bf = cv2.BFMatcher()
matches=bf.knnMatch(desc_1,desc_2,k=2)
#matches = sorted(matches, key = lambda x:x.distance)
draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   flags = 0)
good_points=[]
# for m,n in matches:
#     if(m.distance<=0.4*n.distance):
#         good_points.append([m])
# print(len(good_points))
#img3 = cv2.drawMatches(binary_compare,kp_1,binary,kp_2,matches[:10], flags=2)
# truematches=0
# if(len(kp_2)<len(kp_1)):
#     truematches=len(kp_2)
# else:
#     truematches=len(kp_1)
img3 = cv2.drawMatchesKnn(binary_compare,kp_1,binary,kp_2,matches,None,**draw_params)

plt.imshow(img3),plt.show()

#print()
#show_images([img3])
# sift = cv2.SIFT_create()
# kp_1, desc_1 = sift.detectAndCompute(binary,None)
# kp_2, desc_2 = sift.detectAndCompute(binary_compare,None)
# matches = flann.knnMatch(desc_1, desc_2, k=1)
# result=np.copy(img)
# result = cv2.drawMatches(binary_compare, kp_1, binary, kp_2, matches[:10],  None, flags=2)
# cv2.drawMatches()

# binary_compare = cv2.drawKeypoints(binary_compare,kp_1,binary_compare,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
# binary = cv2.drawKeypoints(binary,kp_2,binary,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# draw_params = dict(matchColor = (0,255,0),
#                    singlePointColor = (255,0,0),
#                    flags = 0)
# good_points=[]
# print(truematches)
# for m, n in matches:
#     if m.distance <= 0.7*n.distance:
#         good_points.append((m,n))
# ###############################
# to calculate the percentage of similarity:
# get the minmum of length of kp_1,kp_2
# get the good points length 
# divide the length of good points by the legnth of minimum
# ###############################
# key_points_num=0
# if(len(kp_1)>len(kp_2)):
#     key_points_num=len(kp_2)
# else:
#     key_points_num=len(kp_1)
# print("percentage of similarity =" ,str((len(good_points)/key_points_num)*100))

