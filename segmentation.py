# from commonfunctions import *
# from scipy.signal import find_peaks
# from skimage.morphology import binary_erosion,binary_dilation
# from skimage.measure import find_contours
# from skimage.draw import rectangle

# ##############################################this segmentation based on projection and morphology and has a bad output###########################
# #############################################but its advatage that it holds the position of every black line#####################################
# # def segmentwithmorph(img):
# #     orig_img=img
# #     img=1-img
# #     cols = img.shape[1]
# #     horizontal_size = cols // 30
# #     window=np.ones((1,horizontal_size))
# #     img=binary_erosion(img,selem=window)
# #     img=binary_dilation(img,selem=window)
# #     img=1-img
# #     show_images([img])
# #     black_hist=np.zeros((img.shape[0],1))
# #     for row in range(0,img.shape[0]):
# #         black_hist[row,0]=(img[row, :] == 0).sum()
# #     x = np.arange(img.shape[0])
# #     fig = plt.figure(figsize =(10, 7))
# #     plt.plot(x,black_hist)
# #     plt.show()
# #     peak=int((40/100)*black_hist.max())
# #     black_lines=find_peaks(black_hist.ravel(),height=peak)
# #     print(black_lines)
# #     print(black_hist)
# #     staff_num=int(np.ceil(len(black_lines[0])/5))
# #     Ysub=np.empty(staff_num,dtype=np.uint)
# #     Yinf=np.empty(staff_num,dtype=np.uint)
# #     m=0
# #     for i in range(0,len(black_lines[0]),5):
# #         if(i>len(black_lines[0])-5):
# #             Ysub[m]=black_lines[0][i-5]
# #             Yinf[m]=black_lines[0][len(black_lines[0])-1]
# #             m+=1
# #         else:    
# #             Ysub[m]=black_lines[0][i]
# #             Yinf[m]=black_lines[0][i+4]
# #             m+=1
# #     Yinf_centre=np.empty(staff_num,dtype=np.uint)
# #     Ysub_centre=np.empty(staff_num,dtype=np.uint)
# #     tolerance=3
# #     Ysub_centre[0]=0
# #     Yinf_centre[0]=((Ysub[1]+Yinf[0])/2)+tolerance

# #     for i in range(1,int(len(black_lines[0])/5)-1):
# #         Ysub_centre[i]=((Ysub[i]+Yinf[i-1])/2)-tolerance
# #         Yinf_centre[i]=((Ysub[i+1]+Yinf[i])/2)+tolerance
# #     Ysub_centre[staff_num-1]=((Ysub[staff_num-1]+Yinf[staff_num-2])/2)-tolerance
# #     Yinf_centre[staff_num-1]=img.shape[0]
# #     imgs=[]
# #     for i in range(0,int(len(black_lines[0])/5)):
# #         new_img=orig_img[Ysub_centre[i]:Yinf_centre[i],:]
# #         new_img[new_img==1]=255
# #         imgs.append(new_img)
# #     show_images(imgs)    
# #     return imgs

# ##########################################this approach depends on morphological opeartions and find contours and has a great output relatively#########
# ##########################################we must modify the commented parameter below to be generic###################################
# def SegmentWithMorph(img):
#     orig_img=img
#     img=1-img
#     cols = img.shape[1]
#     horizontal_size = cols // 30
#     window=np.ones((1,horizontal_size))
#     #this parameter must be modified
#     window2=np.ones((10,15))
#     img=binary_erosion(img,selem=window)
#     img=binary_dilation(img,selem=window)
#     img=binary_dilation(img,selem=window2)
#     show_images([img])
#     boxes=find_contours(img,0)
#     imgs=[]
#     yStart=[]
#     yEnd=[]
#     yStartCent=[]
#     yEndCent=[]
#     for box in boxes:
#         yMax = int(np.max(box[:,0]))
#         yMin = int(np.min(box[:,0]))
#         xMax = int(np.max(box[:,1]))
#         xMin = int(np.min(box[:,1]))
#         #10 must be modified with parameters from slama which represents the hight of each staff(aspect ration)
#         if (xMax-xMin)/(yMax-yMin) > 10:
#             yStart.append(yMin)
#             yEnd.append(yMax)
#     staff_num=len(yStart)
#     yStart[0]=0
#     yEnd[staff_num-1]=img.shape[0]
#     yStartCent.append(0)
#     yEndCent.append(int(((yStart[1]+yEnd[0])/2)))
#     for i in range(1,staff_num-1):
#         yStartCent.append(int(((yStart[i]+yEnd[i-1])/2)))
#         yEndCent.append(int(((yStart[i+1]+yEnd[i])/2)))
#     yStartCent.append(int(((yStart[staff_num-1]+yEnd[staff_num-2])/2)))
#     yEndCent.append(int(img.shape[0]))
#     for i in range(0,staff_num):
#         imgs.append(orig_img[yStartCent[i]:yEndCent[i],:])
#     show_images(imgs) 
#     return imgs
# ################################################first version of segmentation###################################
# def segmentLines(img):
#     #show_images([img])
#     black_hist=np.zeros((img.shape[0],1))
#     for row in range(0,img.shape[0]):
#         black_hist[row,0]=(img[row, :] == 0).sum()
#     x = np.arange(img.shape[0])
#     fig = plt.figure(figsize =(10, 7))
#     plt.plot(x,black_hist)
#     plt.show()
#     ########################################################
#     # note here : I'm not sure if this tolerance is okay or not to decide the peak value of the black lines detection
#     ########################################################
#     peak=int((35/100)*black_hist.max())
#     #print(peak)
#     black_lines=find_peaks(black_hist.ravel(),height=peak)
#     #print(black_lines)
#     staff_num=int(np.ceil(len(black_lines[0])/5))
#     #print(staff_num)
#     Ysub=np.empty(staff_num,dtype=np.uint)
#     Yinf=np.empty(staff_num,dtype=np.uint)
#     m=0
#     #print(len(black_lines[0]))
#     for i in range(0,len(black_lines[0]),5):
#         if(i>len(black_lines[0])-5):
#             Ysub[m]=black_lines[0][i-5]
#             Yinf[m]=black_lines[0][len(black_lines[0])-1]
#             m+=1
#         else:    
#             Ysub[m]=black_lines[0][i]
#             Yinf[m]=black_lines[0][i+4]
#             m+=1
#     # print("Y_sub=",Ysub)
#     # print("Y_inf=",Yinf)
#     Yinf_centre=np.empty(staff_num,dtype=np.uint)
#     Ysub_centre=np.empty(staff_num,dtype=np.uint)
#     tolerance=3
#     Ysub_centre[0]=0
#     Yinf_centre[0]=((Ysub[1]+Yinf[0])/2)+tolerance
#     # print(Yinf_centre[0],Ysub[1],Yinf[0],Ysub[1]+Yinf[0])

#     for i in range(1,int(len(black_lines[0])/5)-1):
#         Ysub_centre[i]=((Ysub[i]+Yinf[i-1])/2)-tolerance
#         Yinf_centre[i]=((Ysub[i+1]+Yinf[i])/2)+tolerance
#     Ysub_centre[staff_num-1]=((Ysub[staff_num-1]+Yinf[staff_num-2])/2)-tolerance
#     Yinf_centre[staff_num-1]=img.shape[0]
#     # print("centre_sub: ",Ysub_centre)
#     # print("centre_inf: ",Yinf_centre)
#     imgs=[]
#     for i in range(0,int(len(black_lines[0])/5)):
#         new_img=img[Ysub_centre[i]:Yinf_centre[i],:]
#         #io.imshow(new_img)
#         #io.show()
#         imgs.append(new_img)
#     #show_images(imgs)
#     return imgs, Ysub, Yinf, Ysub_centre

# ##############################################this function segments symbols and must be modified to hold more accurate output#########################
# def segmentSymbol(img):
#     # show_images([img])
#     black_hist=np.zeros((img.shape[1],1))
#     for column in range(0,img.shape[1]):
#         black_hist[column,0]=(img[:,column] == 0).sum()

#     # x = np.arange(img.shape[1])
#     # fig = plt.figure(figsize =(10, 7))
#     # plt.plot(x,black_hist)
#     # plt.show()

#     peaks=find_peaks(black_hist.ravel(),height=1,distance=10)
#     #max=peaks[1]['peak_heights'].max()
#     #min=peaks[1]['peak_heights'].min()
#     #avg=(max+min)/2
#     height=np.array(peaks[1]['peak_heights'])    
#     peaks=np.array(peaks[0])
#     avg=height.max()*0.3
#     #print(peaks)
#     #print(height)
#     index= peaks[height >= avg]
#     #print(index)
#     Cuts =[]
#     for i in range(0,len(index)-1):
#         Cuts.append((index[i]+index[i+1])/2)
#     #print(Cuts)
#     prev=0
#     FinalImgs=[]
#     for c in Cuts:
#         #show_images([img[:,prev:int(c)]])
#         FinalImgs.append(img[:,prev:int(c)])
#         prev=int(c)
#     #show_images([img[:,prev:img.shape[1]]])
#     FinalImgs.append(img[:,prev:img.shape[1]])
#     #show_images(FinalImgs) 
#     return FinalImgs   


# def SegmentSymbolMorph(img):
#     # Negative Threasholding
#     img = img-255
#     # Get Contours
#     boxes=find_contours(img,0)
#     img_with_boxes = np.zeros(img.shape,dtype=np.bool_)
#     Cuts=[]
#     #print(boxes)
#     for box in boxes:
#         [Xmin, Xmax, Ymin, Ymax] = np.int16([min(box[:,1]),max(box[:,1]),min(box[:,0]),max(box[:,0])])
#         rr, cc = rectangle(start = (Ymin,Xmin), end = (Ymax,Xmax), shape=img.shape)
#         #Condition Should Be modified
#         if Ymax-Ymin > 0 and (Xmax-Xmin)/(Ymax-Ymin) > 0.25 and (Xmax-Xmin)/(Ymax-Ymin) < 0.6:
#             img_with_boxes[rr, cc] = img[rr,cc] #set color white
#             Cuts.append(img[:,Xmin-2:Xmax+2])
#             #Return un Ordered Objects
#             print(Xmin ,Xmax)
#     #show_images([img_with_boxes])
#     return Cuts

from commonfunctions import *
from scipy.signal import find_peaks

def segmentLines(img):
    #show_images([img])
    black_hist=np.zeros((img.shape[0],1))
    for row in range(0,img.shape[0]):
        black_hist[row,0]=(img[row, :] == 0).sum()
    # x = np.arange(img.shape[0])
    # fig = plt.figure(figsize =(10, 7))
    # plt.plot(x,black_hist)
    # plt.show()
    ########################################################
    # note here : I'm not sure if this tolerance is okay or not to decide the peak value of the black lines detection
    ########################################################
    peak=int((35/100)*black_hist.max())
    #print(peak)
    black_lines=find_peaks(black_hist.ravel(),height=peak)
    #print(black_lines)
    staff_num=int(np.ceil(len(black_lines[0])/5))
    #print(staff_num)
    Ysub=np.empty(staff_num,dtype=np.uint)
    Yinf=np.empty(staff_num,dtype=np.uint)
    m=0
    #print(len(black_lines[0]))
    for i in range(0,len(black_lines[0]),5):
        if(i>len(black_lines[0])-5):
            Ysub[m]=black_lines[0][i-5]
            Yinf[m]=black_lines[0][len(black_lines[0])-1]
            m+=1
        else:    
            Ysub[m]=black_lines[0][i]
            Yinf[m]=black_lines[0][i+4]
            m+=1
    # print("Y_sub=",Ysub)
    # print("Y_inf=",Yinf)
    Yinf_centre=np.empty(staff_num,dtype=np.uint)
    Ysub_centre=np.empty(staff_num,dtype=np.uint)
    tolerance=3
    Ysub_centre[0]=0
    Yinf_centre[0]=((Ysub[1]+Yinf[0])/2)+tolerance
    # print(Yinf_centre[0],Ysub[1],Yinf[0],Ysub[1]+Yinf[0])

    for i in range(1,int(len(black_lines[0])/5)-1):
        Ysub_centre[i]=((Ysub[i]+Yinf[i-1])/2)-tolerance
        Yinf_centre[i]=((Ysub[i+1]+Yinf[i])/2)+tolerance
    Ysub_centre[staff_num-1]=((Ysub[staff_num-1]+Yinf[staff_num-2])/2)-tolerance
    Yinf_centre[staff_num-1]=img.shape[0]
    # print("centre_sub: ",Ysub_centre)
    # print("centre_inf: ",Yinf_centre)
    imgs=[]
    for i in range(0,int(len(black_lines[0])/5)):
        new_img=img[Ysub_centre[i]:Yinf_centre[i],:]
        #io.imshow(new_img)
        #io.show()
        imgs.append(new_img)
    #show_images(imgs)
    return imgs, Ysub, Yinf, Ysub_centre


def segmentSymbol(img):
    # show_images([img])
    black_hist=np.zeros((img.shape[1],1))
    for column in range(0,img.shape[1]):
        black_hist[column,0]=(img[:,column] == 0).sum()

    # x = np.arange(img.shape[1])
    # fig = plt.figure(figsize =(10, 7))
    # plt.plot(x,black_hist)
    # plt.show()

    peaks=find_peaks(black_hist.ravel(),height=1,distance=10)
    #max=peaks[1]['peak_heights'].max()
    #min=peaks[1]['peak_heights'].min()
    #avg=(max+min)/2
    height=np.array(peaks[1]['peak_heights'])    
    peaks=np.array(peaks[0])
    avg=height.max()*0.3
    #print(peaks)
    #print(height)
    index= peaks[height >= avg]
    #print(index)
    Cuts =[]
    for i in range(0,len(index)-1):
        Cuts.append((index[i]+index[i+1])/2)
    #print(Cuts)
    prev=0
    FinalImgs=[]
    for c in Cuts:
        #show_images([img[:,prev:int(c)]])
        FinalImgs.append(img[:,prev:int(c)])
        prev=int(c)
    #show_images([img[:,prev:img.shape[1]]])
    FinalImgs.append(img[:,prev:img.shape[1]])
    #show_images(FinalImgs) 
    return FinalImgs   
