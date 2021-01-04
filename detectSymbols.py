import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import match_template
from commonfunctions import show_images, convolve2d
from skimage.measure import find_contours
from skimage.morphology import binary_dilation, binary_closing
from cv2 import cv2


def matchNoteHead(img, dim):

    template = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                         [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                         [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                         [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]], dtype=np.uint8)

    template2 = np.array([[1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                          [1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1]], dtype=np.uint8)

    template = cv2.resize(template, (dim, dim))
    im1 = convolve2d(img, template)
    im2 = convolve2d(1 - img, 1 - template)
    im3 = np.add(im1, im2)
    im3[im3 < 0.9 * dim * dim] = 0

    im3[im3 > 0] = 1

    matches = []
    element = cv2.getStructuringElement(
        cv2.MORPH_ELLIPSE, (dim, dim))

    im3 = binary_dilation(im3, selem=element)
    contours = find_contours(im3, 0.8)

    for contour in contours:
        Ymin = min(contour[:, 0])
        Ymax = max(contour[:, 0])
        matches.append(int((Ymax - Ymin) / 2 + Ymin))

    show_images([im3])
    print(matches)
    return matches
    # result = match_template(img, template)
    # print(np.sum(result))
    # ij = np.unravel_index(np.argmax(result), result.shape)
    # x, y = ij[::-1]

    # fig = plt.figure(figsize=(8, 3))
    # ax1 = plt.subplot(1, 3, 1)
    # ax2 = plt.subplot(1, 3, 2)
    # ax3 = plt.subplot(1, 3, 3, sharex=ax2, sharey=ax2)

    # ax1.imshow(template, cmap=plt.gray())
    # ax1.set_axis_off()
    # ax1.set_title('template')

    # ax2.imshow(img, cmap=plt.gray())
    # ax2.set_axis_off()
    # ax2.set_title('image')
    # # highlight matched region
    # hcoin, wcoin = 6, 6
    # rect = plt.Rectangle((x, y), wcoin, hcoin, edgecolor='r', facecolor='none')
    # ax2.add_patch(rect)

    # ax3.imshow(result)
    # ax3.set_axis_off()
    # ax3.set_title('`match_template`\nresult')
    # # highlight matched region
    # ax3.autoscale(False)
    # ax3.plot(x, y, 'o', markeredgecolor='r',
    #          markerfacecolor='none', markersize=10)

    # plt.show()
