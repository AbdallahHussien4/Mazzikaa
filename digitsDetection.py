from commonfunctions import *
from skimage.measure import find_contours
from skimage.morphology import binary_dilation,binary_erosion
from digitsClassifier import runTest
def detectDigits(img,img_withLines,white_spce,line_thick,start_col,end_col):
    img[img==255]=1
    img=1-img
    digits=[]
    staff_height=((4*white_spce)+(5*line_thick))
    cnts=find_contours(img,0)
    for cnt in cnts:
        yMax = int(np.max(cnt[:,0]))
        yMin = int(np.min(cnt[:,0]))
        if(staff_height/4<(yMax-yMin)<staff_height/2):
            digits.append(img_withLines[yMin:yMax,start_col:end_col])
    if(len(digits)==2):
        return runTest(digits[0])[0],runTest(digits[1])[0]
    else:
        return 1, 1
    
