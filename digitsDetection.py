from commonfunctions import *
from skimage.measure import find_contours
from skimage.morphology import binary_dilation,binary_erosion
from digitsClassifier import runTest
# def detectDigits(img,img_withLines):
#     orig_img=img.copy()
#     img[img==255]=1
#     img=1-img
#     window2=np.ones((2,2))
#     window=np.ones((3,3))
#     img=binary_dilation(img,selem=window2)
#     img=binary_erosion(img,selem=window)
#     show_images([img])
#     white_hist=np.zeros((img.shape[0],1))
#     for row in range(0,img.shape[0]):
#         white_hist[row,0]=(img[row, :] == 1).sum()
#     black=np.where(white_hist == white_hist.min())
#     white=np.where(white_hist != white_hist.min())
#     white=white[0]
#     black=black[0]
#     cut=black[black>int(img.shape[0]/3)]
#     cut=cut[0]
#     first_digit=img_withLines[white[0]:cut+1,:]
#     second_digit=img_withLines[cut+2:first_digit.shape[0]+cut+2,:]
#     show_images([first_digit])
#     show_images([second_digit])
#     print(first_digit.shape)
#     print(second_digit.shape)
#     print(runTest(255-first_digit))
#     print(runTest(255-second_digit))
def detectDigits(img,img_withLines,white_spce,line_thick,start_col,end_col):
    img[img==255]=1
    show_images([img])
    img=1-img
    digits=[]
    staff_height=((4*white_spce)+(5*line_thick))
    cnts=find_contours(img,0)
    for cnt in cnts:
        yMax = int(np.max(cnt[:,0]))
        yMin = int(np.min(cnt[:,0]))
        if(staff_height/4<(yMax-yMin)<staff_height/2):
            digits.append(img_withLines[yMin:yMax,start_col:end_col])
    show_images(digits)
    if(len(digits)==2):
        return runTest(digits[0])[0],runTest(digits[1])[0]
    else:
        return 1, 1
    
