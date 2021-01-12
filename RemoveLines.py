#ِApply on image without solo keys
#Try on several images
#Choose horizontal_projection_parameter
#Check that vertical window doesn't exceed image border
from commonfunctions import *
import cv2 as cv2
def removeLines(image,line_height):
    binarized = image.copy()
    horizontal_projection_parameter=(35/100)
    # Construct horizontal projection
    horizontal_projection=[]
    projection_img=np.zeros((binarized.shape[0],binarized.shape[1]))
    projection_img[binarized==255]=0
    projection_img[binarized==0]=1
    horizontal_projection=np.sum(projection_img,axis=1)
    #Get peaks
    peak_threshold = horizontal_projection_parameter*horizontal_projection.max()
    boolpeaks=horizontal_projection
    boolpeaks[boolpeaks<peak_threshold]=0
    boolpeaks[boolpeaks>peak_threshold]=1
    peaks=np.where(boolpeaks)[0]    
    # Line Height Tracking Removal
    for peak in peaks:
        sum_row=binarized[peak,:]
        addition=0
        for i in range(1,(line_height*2)+1):
            if(peak+i < binarized.shape[0]):
                addition=np.add(binarized[peak+i,:],0,dtype=float)
            if(peak-i >= 0 ):
                addition=np.add(binarized[peak-i,:],addition,dtype=float)
            sum_row=np.add(addition,sum_row,dtype=float)  
        sum_row=sum_row/255
        binarized[peak,sum_row>(2*line_height+1)]=255
    return binarized,peaks

# def removeLinesErod(binarized):
#     orig_img=binarized.copy()
#     binarized[binarized==255]=1
#     binarized=1-binarized
#     rows = binarized.shape[0]
#     verticalsize = rows// 25
#     # Create structure element for extracting vertical lines through morphology operations
#     verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
#     # Apply morphology operations
#     binarized = cv2.erode(binarized, verticalStructure)
#     show_images([binarized])
#     binarized = cv2.dilate(binarized, verticalStructure)
#     # Show extracted vertical lines
#     show_images([1-binarized])