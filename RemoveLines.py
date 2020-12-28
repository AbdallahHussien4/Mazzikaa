#ِApply on image without solo keys
#Try on several images
#Choose horizontal_projection_parameter
#Check that vertical window doesn't exceed image border
from commonfunctions import *

def RGB2binary(img,threshold):
    img=np.array(img,dtype=np.uint8)
    Vimg=np.reshape(img,(img.shape[0]*img.shape[1],1))
    Vimg[(Vimg<threshold)]=0
    Vimg[(Vimg>=threshold)]=255
    img=np.reshape(Vimg,(img.shape[0],img.shape[1]))
    return img
    
def removeLines(binarized,line_height):
    horizontal_projection_parameter=(35/100)
    # Construct horizontal projection
    horizontal_projection=[]
    projection_img=np.zeros((binarized.shape[0],binarized.shape[1]))
    projection_img[binarized==255]=0
    projection_img[binarized==0]=1
    horizontal_projection=np.sum(projection_img,axis=1)

    # Plt horizontal projection
    # x = np.arange(binarized.shape[0])
    # fig = plt.figure(figsize =(10, 7))
    # plt.plot(x,horizontal_projection)
    # plt.show()

    #Get peaks
    peak_threshold = horizontal_projection_parameter*horizontal_projection.max()
    boolpeaks=horizontal_projection
    boolpeaks[boolpeaks<peak_threshold]=0
    boolpeaks[boolpeaks>peak_threshold]=1
    peaks=np.where(boolpeaks)[0]    
    # Line Height Tracking Removal
    #line_height=3
    #addition=0
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
    #show_images([binarized])
    return binarized