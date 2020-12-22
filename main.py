from commonfunctions import show_images, io, np
from skimage.filters import threshold_otsu as to
from StaffLines import getSLsThickness_WhiteSpaces
from Preprocessing import AdaptiveThresholding as AT
from detection import quarterEighthNoteDetection
from segmentation import segmentLines, segmentSymbol

def normalizeImage(img):
    if(img.max() == 1):
        return np.uint16(img * 255)
    return img

img = io.imread('imgs/score_2.jpg', as_gray=True)
img = normalizeImage(img)
binary = AT(img)

for image in segmentLines(binary):
    segmentSymbol(image)
#quarterEighthNoteDetection(binary)