from commonfunctions import *
from skimage.transform import *

def Make_IMG_HORIZONTAL(BinarizedImg,percesion=1):
    NegativeBinarizedImg=255-BinarizedImg
    DegAngles=np.arange(-90,91,percesion)
    RadAngles=np.deg2rad(DegAngles)
    Accumilation, angles, rho=hough_line(NegativeBinarizedImg,RadAngles)
    MaxAccumilation=np.max(Accumilation)
    rotation_angle=np.average(np.where(Accumilation==MaxAccumilation)[1]) 
    if(rotation_angle<90):
        rotated_img=rotate(BinarizedImg,rotation_angle,resize=True,mode='constant',cval=1)
    if(rotation_angle>90):
        rotated_img=rotate(BinarizedImg,rotation_angle-180,resize=True,mode='constant',cval=1)
    if(rotation_angle==90):
        return BinarizedImg    
    return rotated_img
