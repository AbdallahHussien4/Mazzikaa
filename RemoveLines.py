#ِApply on image without solo keys
#Try on several images
#Choose horizontal_projection_parameter
#Check that vertical window doesn't exceed image border

horizontal_projection_parameter=0.2
img=io.imread("./1.png")
binarized=RGB2binary("./1.png",140)
show_images([img,binarized],['1','2'])
# Construct horizontal projection
horizontal_projection=[]
projection_img=np.zeros((img.shape[0],img.shape[1]))
projection_img[binarized==255]=0
projection_img[binarized==0]=1
horizontal_projection=np.sum(projection_img,axis=1)
# Plt horizontal projection
x = np.arange(img.shape[0])
fig = plt.figure(figsize =(10, 7))
plt.plot(x,horizontal_projection)
plt.show()

#Get peaks
peak_threshold = horizontal_projection_parameter*horizontal_projection.max()
boolpeaks=horizontal_projection
boolpeaks[boolpeaks<peak_threshold]=0
boolpeaks[boolpeaks>peak_threshold]=1
peaks=np.where(boolpeaks)[0]
line_height=2
# Line Height Tracking Removal
for peak in peaks:
    sum_row=binarized[peak,:]
    for i in range(1,(line_height*2)+1):
        addition=np.add(binarized[peak+i,:],binarized[peak-i,:],dtype=float)
        sum_row=np.add(addition,sum_row,dtype=float)
    sum_row=sum_row/255
    binarized[peak,sum_row>(2*line_height+1)]=255
