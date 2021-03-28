# Mazzikaa
The aim of this project is to develop a sheet music reader. This field is called Optical Music Recognition (OMR).\
Its objective is to convert sheet music to a machine-readable version.\
We take a simplified version where we convert an image of sheet music to a textual representation\
that can be further processed to produce midi files or audio files like wav or mp3. 

# Implementation:
## Binarization:
The first step is to binarize the input image, and even though it seems like an easy step, some test cases produce undesirable outputs when using certain binarization technique. Meaning, if we use Otsu, it will output precise binary images most of the times, specially when the input image is a scanned music sheet. But if the input image was camera captured, Otsu produces a lot of noise in the image and makes the subsequent processing steps harder. On the other hand, adaptive thresholding gives great results on camera captured images with almost no noise, but on scanned images it loses especially important image info. Particularly, it creates holes inside the originally filled music note heads, which results in wrong detection and classification later. So, on observing the histograms of the input images and the histograms of each binarization method’s output image. We found a way to choose the right thresholding method depending on the histograms mentioned.
For a scanned image we noticed that its histogram had two peaks one near the zero and another near 255. That makes sense because a music sheet is in black and white and scanning it produces a uniform histogram.

![](/assets_for_readme/scanned_bin.jpg)   ![](/assets_for_readme/scanned_bin_hist.jpg)

Here we can see how adaptive thresholding corrupts the image. So, if we detect only a few peaks in the input image histogram, we use Otsu.
For Camera captured images we have two cases, the first one is when Otsu produces a lot of noise while the adaptive method produces a valid clean output. The other case is when Otsu produces a valid output while adaptive corrupts the music notes like in the previous example on scanned. 
Detecting which case we have is simple, we first check for the input image’s histogram to see if it was scanned or not just like we did previously, and here we’ll find a great number of peaks or in other words a non-uniform histogram. Now we check the histogram of each thresholding method’s output binary image, if the number of black pixels exceed a certain threshold when using Otsu, we would know that it produced some noise, so we would choose adaptive thresholding. If the number of black pixels did not exceed the threshold then we use Otsu. Here are two examples on how we can’t use the same technique on all captured images.

![](/assets_for_readme/cam_cap_bin1.jpg)   ![](/assets_for_readme/cam_cap_bin1_hist.jpg) ![](/assets_for_readme/cam_cap_bin1_out_hist.jpg)

![](/assets_for_readme/cam_cap_bin2.jpg)   ![](/assets_for_readme/cam_cap_bin2_hist.jpg) ![](/assets_for_readme/cam_cap_bin2_out_hist.jpg)

It's obvious that in the second example the black pixels are much greater than the white ones and that's due to the extreme noise added.
The behavior of adaptive thresholding is due to the block size, it scans the image with, being too small. And since we don’t know which block size to use in advance, we use the small block size when it’s appropriate and change the technique altogether when it’s not.

## Rotation & De-Skewing:
The second step is to detect if the image is rotated (i.e., the staff lines aren’t horizontal) and if so, we find the angle and rotate it accordingly. Here we use hough lines to 
detect the angle. After rotating the image, we notice that the lines aren’t exactly horizontal and they’re a bit skewed at points. This issue is addressed in a later step. 
Another problem is if the image is rotated 180 degrees, as in this case the lines are horizontal, but the image is flipped upside-down, and we’ll address this problem later as 
well.
![](/assets_for_readme/rotation.JPG)

## Staff Lines’ Thickness and spaces between them:
Here we perform run length encoding on the image using vertical columns and checking the most frequent runs of zeros and runs of ones. The most frequent run of zeros is the 
staff lines’ thickness, and the most frequent run of ones is obviously the spaces between them.
In this example it’s clear that the staff lines’ thickness is mostly 1 or 2 pixels, while the spaces are 17 or 18 pixels.

![](/assets_for_readme/staff.JPG)

## Segmentation:
An extremely important step is segmenting the staffs to work on each one independently. We have two ways to segment the staffs. The first one is by detecting the position of the 
five staff lines that comprise the staff, we do that by taking a horizontal projection of the image and detecting the peaks in the histogram. This way works well with scanned 
images, but in case of camera captured ones, the lines aren’t exactly horizontal as we’ve mentioned before, giving us a faulty histogram. So, in that case we perform dilation on 
the negative of the binary image, sticking staffs together followed by finding the contours in the result and segmenting according to these contours. Here, knowing the nature of 
the image (whether it’s scanned, or camera captured) plays an important part in choosing which method to go with.
In the first example, where the music sheet is scanned, the histogram looks so neat and we can find three groups each consisting of five peaks, representing the three staffs 
having five staff lines each. The second example however would produce a rather awful histogram as most lines aren’t horizontal, so, as shown after dilation the image contains 
three major contiguous blocks (contours) representing the three staffs.

## First method:
![](/assets_for_readme/seg1.jpg) 
![](/assets_for_readme/seg1_.jpg)

## Second method: 
![](/assets_for_readme/seg2.jpg) 
![](/assets_for_readme/seg2_.jpg)


## Clefs detection and removal:
Since in our implementation we don’t care for the clefs, we match a clef’s template to the staff we’re currently processing to find its position and remove it. Knowing that the clef must always be present at the start of the staff we only check in the first 30% of the staff as some noise might make us detect false clefs. If we didn’t detect a clef, we then know that we must have an upside-down image, so we rotate it 180 degrees and check again for the clef to remove it. 

![](/assets_for_readme/clefs.JPG) 



Before we start detecting the music notes we want to straighten the lines correctly as we’ve stated that the rotation phase didn’t quite de-skewed the image. So, we divide each 
staff into equal parts and then rotate each part on its own, so the lines are locally almost straight.

![](/assets_for_readme/deskewing.JPG) 


## Note Heads detection:
One of the most important steps as well is to find the note heads and determining their exact position (on which line). Our initial implementation was using a disk-shaped structuring element to perform binary opening on the staff followed by a simple way of template matching(just comparing the pixels and checking on the percentage of matched pixels) to remove noise. But this way was inefficient in localizing the noteheads, so we moved on to another implementation.
![](/assets_for_readme/noteHeads1.JPG) 


The current implementation is to use template matching(by open cv) and that gave us accurate outputs with an accurate localization on most test cases.
The template used here and the subsequent ones are obtained by cropping the symbols from different images and then scaling them according to the image we’re working on. We do that by knowing how much space the symbol occupies and scaling it according to the space we calculated earlier(space between staff lines). For example, the notehead occupies 1 space while a sharp accidental occupies approximately 3 spaces.
![](/assets_for_readme/noteHeads2.JPG) 


If we detected a half or a whole note, we skip some of the following steps(for example they can’t have flags or be beamed).

## Accidentals & Flags detection:
After detecting the noteheads we want to check if they have flags attached or have accidentals just before them. So, we use template matching again, using all accidentals’ templates and checking just a small portion left to the notehead, and using different flags’ templates to check just right of the notehead.

![](/assets_for_readme/acc_flags.JPG) 

## Beams & Chords detection:
Now, we check if several noteheads are beamed together, and we do that by doing run length encoding of a column in the mid point between each two consecutive noteheads, and then 
checking if we have runs of zeros substantially greater than the staff lines’ thickness. For chords, we just check the positions of consecutive noteheads and see if they’re 
close enough to form a chord. 

It’s worth noting that we use a class for representing each note. So, each staff consists of an array of notes sorted according to their X position. Each note holds its 
information(if it has a preceding accidental, is beamed, has a flag or is part of a chord)


## Time Signature detection:
Our last step is to find the time signature. We start by dilating the image to form contiguous objects(contours) and since we’ve removed the clefs, we know that the following 
object is either a note or the time signature. So, we check our first note’s position and if it is contained inside the first object, then this staff doesn’t have a time 
signature and we use the one in a previous staff. Else, we know that it contains the time signature. In that case we cut this part from the image and separate the two numbers of 
the time signature and send each one to a trained SVM classifier to classify them independently. The classifier is previously trained with images for the numbers 2 & 4 since we 
deal with them exclusively in our implementation. The features extracted from the image are the hog features.
![](/assets_for_readme/time_sig.JPG) 

