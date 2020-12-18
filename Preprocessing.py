from commonfunctions import show_images, np, math, convolve2d
import os
import skimage.filters as filters

def Rotate(img, angle):
    # convert rotation amount to radian
    RadAngle = -1*(angle) * np.pi / 180.0

    # get dimension info
    Wi, Hi = img.shape

    # create output image, for worst case size (45 degree)
    #max_len = int(math.sqrt(Hi*Hi + Wi*Wi))
    #Rimg = np.zeros((max_len,max_len))
    Rimg = np.ones(img.shape)
    W, H = Rimg.shape

    mid_row = int((H)/2)
    mid_col = int((W)/2)

    # Rotate
    for y in range(H):
        for x in range(W):
            #  apply rotation matrix
            newx = (x-mid_row)*math.cos(RadAngle) - \
                (y-mid_col)*math.sin(RadAngle)
            newy = (x-mid_row)*math.sin(RadAngle) + \
                (y-mid_col)*math.cos(RadAngle)
            #newx = (x)*math.cos(RadAngle) -(y)*math.sin(RadAngle)
            #newy = (x)*math.sin(RadAngle) + (y)*math.cos(RadAngle)
            #  add offset
            newx += mid_row
            newy += mid_col

            #  get nearest index
            newx = round(newx)
            newy = round(newy)

            #  check if x/y corresponds to a valid pixel in input image
            if (newx >= 0 and newy >= 0 and newx < Wi and newy < Hi):
                Rimg[x][y] = img[newx][newy]
    #show_images([img,Rimg],['Original','Rotated'])
    return Rimg 

def AdaptiveThresholding(img,BlockSize=9,C=8):
    Filter=np.ones(BlockSize**2).reshape(BlockSize,BlockSize)/BlockSize**2  #Averaging Filter
    img_F = convolve2d(img,Filter)
    img_Th = img_F[(BlockSize-1)//2:img_F.shape[0]-(BlockSize-1)//2,(BlockSize-1)//2:img_F.shape[1]-(BlockSize-1)//2] - img
    img_Th = img_Th - C              #Handle Background
    img_Out = img_Th>0
    img_Out = 1-img_Out
    return img_Out
