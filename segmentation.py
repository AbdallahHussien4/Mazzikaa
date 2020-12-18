from commonfunctions import np, show_images, io
from scipy.signal import find_peaks

def segmentLines(img):
    show_images([img])
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
    peak=int((70/100)*black_hist.max())
    print(peak)
    black_lines=find_peaks(black_hist.ravel(),height=peak)
    print(black_lines)
    staff_num=int(len(black_lines[0])/5)
    print(staff_num)
    Ysub=np.empty(staff_num,dtype=np.uint)
    Yinf=np.empty(staff_num,dtype=np.uint)
    m=0
    # print(black_lines[0])
    for i in range(0,len(black_lines[0]),5):
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
        io.imshow(new_img)
        io.show()
        imgs.append(new_img)
    show_images(imgs)
    return imgs
