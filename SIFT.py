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

def normalizeImage(img):
    if(img.max() <= 1):
        return np.uint8(img * 255)
    return img


img = io.imread('compare.JPG', as_gray=True)
compare=io.imread('compare1.JPG',as_gray=True)
compare=normalizeImage(compare)
binary_compare=AdaptiveThresholding(compare)
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
sift=cv2.SIFT_create()
kp_1,desc_1=sift.detectAndCompute(binary_compare,None)
kp_2,desc_2=sift.detectAndCompute(binary,None)
print(len(kp_1))
print(len(kp_2))

index_params = dict(algorithm=0, trees=5)
search_params = dict()
flann = cv2.FlannBasedMatcher(index_params, search_params)
matches = flann.knnMatch(desc_1, desc_2, k=2)
result=np.copy(img)
#result = cv2.drawMatches(binary_compare, kp_1, binary, kp_2, matches[:10],  None, flags=2)
#cv2.drawMatches()

binary_compare = cv2.drawKeypoints(binary_compare,kp_1,binary_compare,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
binary = cv2.drawKeypoints(binary,kp_2,binary,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

draw_params = dict(matchColor = (0,255,0),
                   singlePointColor = (255,0,0),
                   flags = 0)
good_points=[]
print(len(matches))
for m, n in matches:
    if m.distance <= 0.7*n.distance:
        good_points.append((m,n))
################################
#to calculate the percentage of similarity:
#get the minmum of length of kp_1,kp_2
#get the good points length 
#divide the length of good points by the legnth of minimum
################################
key_points_num=0
if(len(kp_1)>len(kp_2)):
    key_points_num=len(kp_2)
else:
    key_points_num=len(kp_1)
print("percentage of similarity =" ,str((len(good_points)/key_points_num)*100))

img3 = cv2.drawMatchesKnn(binary_compare,kp_1,binary,kp_2,good_points,None,**draw_params)
show_images([binary,binary_compare,img3],["org","result","match"])
print(len(good_points))