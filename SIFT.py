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


img = io.imread('3.png', as_gray=True)
compare=io.imread('compare1.JPG',as_gray=True)
compare=normalizeImage(compare)
binary_compare=AdaptiveThresholding(compare)
img = normalizeImage(img)
binary = AdaptiveThresholding(img)
sift=cv2.SIFT_create()
kp_1,desc_1=sift.detectAndCompute(binary_compare,None)
kp_2,desc_2=sift.detectAndCompute(binary,None)

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
#print(matches[0])
for m, n in matches:
    if m.distance <= 0.5*n.distance:
        good_points.append((m,n))
################################
#to calculate the percentage of similarity:
#get the minmum of length of kp_1,kp_2
#get the good points length 
#divide the length of good points by the legnth of minimum
################################
img3 = cv2.drawMatchesKnn(binary_compare,kp_1,binary,kp_2,good_points,None,**draw_params)
show_images([binary,binary_compare,img3],["org","result","match"])
print(len(good_points))