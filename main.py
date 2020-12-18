from commonfunctions import show_images, io, np
from skimage.filters import threshold_otsu as to
from StaffLines import getSLsThickness_WhiteSpaces
from Preprocessing import AdaptiveThresholding as AT

def normalizeImage(img):
    if(int(max(map(max, img))) == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/score_5.png', as_gray=True)
img = normalizeImage(img)
binary = AT(img)

print(getSLsThickness_WhiteSpaces(binary))
show_images([img, binary])