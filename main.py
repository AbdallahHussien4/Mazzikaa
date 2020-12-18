from commonfunctions import show_images, io, np
from skimage.filters import threshold_otsu as to
from StaffLines import getSLsThickness_WhiteSpaces

def normalizeImage(img):
    if(int(max(map(max, img))) == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/score_7.png', as_gray=True)
img = normalizeImage(img)
thresh = to(img, nbins=256)
binary = img.copy()
binary[binary >= thresh] = 255
binary[binary < thresh] = 0

print(getSLsThickness_WhiteSpaces(binary))
show_images([img, binary])