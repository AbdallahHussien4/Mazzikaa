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
compare=io.imread('compare.JPG',as_gray=True)
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
#result = cv2.drawMatches(binary_compare, kp_1, binary, kp_2, matches, None)

binary = cv2.drawKeypoints(binary_compare,kp_1,binary,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
show_images([binary],["result"])
print(len(matches))