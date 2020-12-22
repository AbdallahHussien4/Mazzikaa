from StaffLines import getSLsThickness_WhiteSpaces
from commonfunctions import np, show_images
from skimage.morphology import binary_opening, binary_closing, binary_erosion
import cv2

def quarterEighthNoteDetection(img):

    neg = img.copy()
    neg[img == 1] = 0
    neg[img == 0] = 1
    sl, dim = getSLsThickness_WhiteSpaces(img)
    horiElement = np.ones((3 * (dim + sl), 1), dtype=np.uint8)
    if dim % 2 == 0:
        dim -= 1
    '''element = np.zeros((dim, dim), dtype=np.uint8)
    mid = int(dim/2)
    print(mid)
    s = 0
    dec = False
    for i in range(dim):
        element[i, mid - s : mid + s + 1] = 1
        if s >= mid:
            dec = True
        s -= 1 if dec else -1'''
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (dim, dim))
    opened = binary_opening(neg, selem=element)
    opened2 = binary_opening(neg, selem=horiElement)
    show_images([neg, opened, opened2, opened2 + opened])
