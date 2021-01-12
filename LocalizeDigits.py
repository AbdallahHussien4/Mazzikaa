from TemplateMatching import matchClefs,matchNotes
from RemoveLines import removeLines
from StaffLines import getSLsThickness_Whitespaces
from commonfunctions import *
from skimage.measure import find_contours
import cv2
import numpy as np
from digitsDetection import detectDigits
from segmentation import segmentwithmorph
# path='/home/belal/Downloads/PublicTestCases-version1.1/test-set-scanned/test-cases/'

# orgImg = io.imread(path+'02.PNG',as_gray=True)
# img=orgImg>0.5

# th,w= getSLsThickness_Whitespaces(img,vertical=True)
# img=segmentwithmorph((255*img).astype(np.uint8),w,th)[0]
# show_images([img])
# img_withlines=np.copy(img)
# img,peaks=removeLines(img,th)
# img,x,y=matchClefs(img,w)

# img : one staff-lines without lines 0-255 without clefs 
def localize_digits(img,firstNoteXposition,white_space):
        img = 255-img
        contours = find_contours(img, 0.8)
        minXmin=10000
        minXmax=10000
        for contour in contours:
            Xmin = int(min(contour[:, 1]))
            Xmax = int(max(contour[:, 1]))
            Ymin = int(min(contour[:, 0]))
            Ymax = int(max(contour[:, 0]))
            if Xmin < minXmin and (Xmax - Xmin ) > white_space and (Ymax - Ymin ) > white_space:
                minXmin=Xmin
                minXmax=Xmax
        if firstNoteXposition > minXmin and firstNoteXposition < minXmax:
            return None
        else:
            return img[:,minXmin-int(white_space/2):minXmax+int(white_space/2)],minXmin-int(white_space/2),minXmax+int(white_space/2)