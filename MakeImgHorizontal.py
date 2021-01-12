from commonfunctions import *
from skimage.transform import *
from Preprocessing import Rotate

def Make_IMG_HORIZONTAL(BinarizedImg,percesion=1,resize=True,Horizontal=False):
    NegativeBinarizedImg=255-BinarizedImg
    DegAngles=np.arange(-90,91,percesion)
    RadAngles=np.deg2rad(DegAngles)
    Accumilation, angles, rho=hough_line(NegativeBinarizedImg,RadAngles)
    MaxAccumilation=np.max(Accumilation)

    #rotation_angle=np.average(np.where(Accumilation==MaxAccumilation)[1])
    rotation_angle=np.where(Accumilation==MaxAccumilation)[1][0] 
    MAxRho=np.where(Accumilation==MaxAccumilation)[0][0]
    #print("Angle : ",rotation_angle)       
    if(rotation_angle<90):
        rotated_img=rotate(BinarizedImg,rotation_angle,resize,mode='constant',cval=1)
    elif(rotation_angle>90):
        rotated_img=rotate(BinarizedImg,rotation_angle-180,resize,mode='constant',cval=1) 
    else:
        if(MAxRho < BinarizedImg.shape[0]):
            return BinarizedImg
        rotated_img=rotate(BinarizedImg,rotation_angle,resize,mode='constant',cval=1)
    return rotated_img,rotation_angle
