from StaffLines import getSLsThickness_WhiteSpaces
from commonfunctions import np, show_images
from skimage.morphology import binary_opening, binary_closing, binary_erosion
from skimage.draw import rectangle
from skimage.morphology import binary_opening, binary_closing, binary_erosion
from skimage.measure import find_contours
from cv2 import cv2     # a retarded solution for a more retarded error

def quarterEighthNoteDetection(img):

    neg = img.copy()
    neg[img == 1] = 0
    neg[img == 0] = 1
    sl, dim = getSLsThickness_WhiteSpaces(img)
    if dim % 2 == 0:
        dim += 1
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dim, dim))
    opened = binary_opening(neg, selem=element)
    
    verticalElement = np.ones((3 * (dim + sl), 1), dtype=np.uint8)
    verticalLinesImg = binary_opening(neg, selem=verticalElement)
    
    # replacing each notehead with one pixel in its center
    contours = find_contours(opened, 0.8)
    noteHeadsAsOnePixelImg = np.zeros(img.shape, dtype=np.bool_)
    for contour in contours:
        Xmin = min(contour[:,1])
        Xmax = max(contour[:,1])
        Ymin = min(contour[:,0])
        Ymax = max(contour[:,0])
        rr, cc = int((Ymax - Ymin) / 2 + Ymin) , int((Xmax - Xmin) / 2 + Xmin) 
        noteHeadsAsOnePixelImg[rr, cc] = 1

    show_images([neg, opened, noteHeadsAsOnePixelImg, verticalLinesImg])
