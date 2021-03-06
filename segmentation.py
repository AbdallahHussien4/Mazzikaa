from commonfunctions import *
from scipy.signal import find_peaks
from skimage.morphology import binary_erosion,binary_dilation
from skimage.measure import find_contours
from skimage.draw import rectangle
import cv2 as cv2

##############################################this segmentation based on projection and morphology and has a bad output###########################
#############################################but its advatage that it holds the position of every black line#####################################
def segmentwithmorph(img,white_spce,line_thick):
    width=img.shape[1]
    orig_img=img
    img=255-img
    cols = img.shape[1]
    horizontal_size = cols // 30
    window=np.ones((1,horizontal_size))
    img=binary_erosion(img,selem=window)
    img=binary_dilation(img,selem=window)
    img=1-img
    black_hist=np.zeros((img.shape[0],1))
    for row in range(0,img.shape[0]):
        black_hist[row,0]=(img[row, :] == 0).sum()
    filtered_blackLines=[]
    black_lines=np.where(black_hist>=int(0.3*width))
    for i in range(0,len(black_lines[0])-1):
        diff=black_lines[0][i+1]-black_lines[0][i]
        if(diff>=white_spce-line_thick):
            filtered_blackLines.append(black_lines[0][i])
    filtered_blackLines.append(black_lines[0][len(black_lines[0])-1])
    staff_num=int(np.ceil(len(filtered_blackLines)/5))
    imgs=[]
    if(staff_num==1):
        imgs.append(orig_img)
        return imgs
    Ysub=np.empty(staff_num,dtype=np.uint)
    Yinf=np.empty(staff_num,dtype=np.uint)
    m=0
    for i in range(0,len(filtered_blackLines),5):
        if(i>len(filtered_blackLines)-5):
            Ysub[m]=filtered_blackLines[i-5]
            Yinf[m]=filtered_blackLines[len(filtered_blackLines)-1]
            m+=1
        else:    
            Ysub[m]=filtered_blackLines[i]
            Yinf[m]=filtered_blackLines[i+4]
            m+=1
    Yinf_centre=np.empty(staff_num,dtype=np.uint)
    Ysub_centre=np.empty(staff_num,dtype=np.uint)
    Ysub_centre[0]=0
    Yinf_centre[0]=((Ysub[1]+Yinf[0])/2)

    for i in range(1,int(len(filtered_blackLines)/5)-1):
        Ysub_centre[i]=((Ysub[i]+Yinf[i-1])/2)
        Yinf_centre[i]=((Ysub[i+1]+Yinf[i])/2)
    Ysub_centre[staff_num-1]=((Ysub[staff_num-1]+Yinf[staff_num-2])/2)
    Yinf_centre[staff_num-1]=img.shape[0]
    
    for i in range(0,int(len(filtered_blackLines)/5)):
        new_img=orig_img[Ysub_centre[i]:Yinf_centre[i],:]
        new_img[new_img==1]=255
        imgs.append(new_img)
    return imgs

##########################################this approach depends on morphological opeartions and find contours and has a great output relatively#########
##########################################we must modify the commented parameter below to be generic###################################
def SegmentWithMorphCont(img,white_spce,staff_thick):
    orig_img=img.copy()
    img[img==255]=1
    img=1-img
    cols = img.shape[1]
    horizontal_size = cols // 30
    window=np.ones((1,horizontal_size))
    #this parameter must be modified
    staff_height=int(((4*white_spce)+(5*staff_thick))//3)
    window2=np.ones((staff_height,20))
    img=binary_erosion(img,selem=window)
    img=binary_dilation(img,selem=window)
    #for dilation
    img=binary_dilation(img,selem=window2)
    boxes=find_contours(img,0)
    imgs=[]
    yStart=[]
    yEnd=[]
    yStartCent=[]
    yEndCent=[]
    aspect_ratio=cols/((4*white_spce)+(5*staff_thick))
    for box in boxes:
        yMax = int(np.max(box[:,0]))
        yMin = int(np.min(box[:,0]))
        xMax = int(np.max(box[:,1]))
        xMin = int(np.min(box[:,1]))
        if ((aspect_ratio*0.3) <(xMax-xMin)/(yMax-yMin) < aspect_ratio):
            yStart.append(yMin)
            yEnd.append(yMax)
    if(len(yStart)==0):
        return [orig_img]        
    staff_num=len(yStart)
    yStart[0]=0
    yEnd[staff_num-1]=img.shape[0]
    yStartCent.append(0)
    if (len(yStart)>1):
        yEndCent.append(int(((yStart[1]+yEnd[0])/2)))
    else:
        imgs.append(orig_img[yStart[0]:yEnd[0],:])
        return imgs
    for i in range(1,staff_num-1):
        yStartCent.append(int(((yStart[i]+yEnd[i-1])/2)))
        yEndCent.append(int(((yStart[i+1]+yEnd[i])/2)))
    yStartCent.append(int(((yStart[staff_num-1]+yEnd[staff_num-2])/2)))
    yEndCent.append(int(img.shape[0]))
    for i in range(0,staff_num):
        imgs.append(orig_img[yStartCent[i]:yEndCent[i],:])
    return imgs
################################################first version of segmentation###################################
def segmentLines(img):
    black_hist=np.zeros((img.shape[0],1))
    for row in range(0,img.shape[0]):
        black_hist[row,0]=(img[row, :] == 0).sum()
    x = np.arange(img.shape[0])
    fig = plt.figure(figsize =(10, 7))
    plt.plot(x,black_hist)
    plt.show()
    ########################################################
    # note here : I'm not sure if this tolerance is okay or not to decide the peak value of the black lines detection
    ########################################################
    peak=int((35/100)*black_hist.max())
    black_lines=find_peaks(black_hist.ravel(),height=peak)
    staff_num=int(np.ceil(len(black_lines[0])/5))
    Ysub=np.empty(staff_num,dtype=np.uint)
    Yinf=np.empty(staff_num,dtype=np.uint)
    m=0
    for i in range(0,len(black_lines[0]),5):
        if(i>len(black_lines[0])-5):
            Ysub[m]=black_lines[0][i-5]
            Yinf[m]=black_lines[0][len(black_lines[0])-1]
            m+=1
        else:    
            Ysub[m]=black_lines[0][i]
            Yinf[m]=black_lines[0][i+4]
            m+=1
    Yinf_centre=np.empty(staff_num,dtype=np.uint)
    Ysub_centre=np.empty(staff_num,dtype=np.uint)
    tolerance=3
    Ysub_centre[0]=0
    Yinf_centre[0]=((Ysub[1]+Yinf[0])/2)+tolerance

    for i in range(1,int(len(black_lines[0])/5)-1):
        Ysub_centre[i]=((Ysub[i]+Yinf[i-1])/2)-tolerance
        Yinf_centre[i]=((Ysub[i+1]+Yinf[i])/2)+tolerance
    Ysub_centre[staff_num-1]=((Ysub[staff_num-1]+Yinf[staff_num-2])/2)-tolerance
    Yinf_centre[staff_num-1]=img.shape[0]
    return Ysub, Yinf, Ysub_centre

##############################################this function segments symbols and must be modified to hold more accurate output#########################
def segmentSymbol(img):
    black_hist=np.zeros((img.shape[1],1))
    for column in range(0,img.shape[1]):
        black_hist[column,0]=(img[:,column] == 0).sum()

    peaks=find_peaks(black_hist.ravel(),height=1,distance=10)
    height=np.array(peaks[1]['peak_heights'])    
    peaks=np.array(peaks[0])
    avg=height.max()*0.3
    index= peaks[height >= avg]
    Cuts =[]
    for i in range(0,len(index)-1):
        Cuts.append((index[i]+index[i+1])/2)
    prev=0
    FinalImgs=[]
    for c in Cuts:
        FinalImgs.append(img[:,prev:int(c)])
        prev=int(c)
    FinalImgs.append(img[:,prev:img.shape[1]])
    return FinalImgs   


def SegmentSymbolMorph(img,ws):
    # Negative Threasholding
    img = img-255
    # Get Contours
    element = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (ws, ws))
    img = binary_dilation(img, selem=element)
    boxes=find_contours(img,0)
    img_with_boxes = np.zeros(img.shape,dtype=np.bool_)
    Cuts=[]
    for box in boxes:
        [Xmin, Xmax, Ymin, Ymax] = np.int16([min(box[:,1]),max(box[:,1]),min(box[:,0]),max(box[:,0])])
        rr, cc = rectangle(start = (Ymin,Xmin), end = (Ymax,Xmax), shape=img.shape)
        #Condition Should Be modified
        if Ymax-Ymin > 0 and (Xmax-Xmin)/(Ymax-Ymin) > 0.25 and (Xmax-Xmin)/(Ymax-Ymin) < 0.6:
            img_with_boxes[rr, cc] = img[rr,cc] #set color white
            Cuts.append(img[:,Xmin-2:Xmax+2])
            #Return un Ordered Objects
            # print(Xmin ,Xmax)
    return Cuts