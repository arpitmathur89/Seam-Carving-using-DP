from pylab import *
from skimage import img_as_float
from skimage.filters import sobel_h, sobel_v
from numpy import *


def dual_gradient_energy(img):
    R = img[:, :, 0]
    G = img[:, :, 1]
    B = img[:, :, 2]
    return sobel_h(R)**2 + sobel_v(R)**2 + sobel_h(G)**2 + \
        sobel_v(G)**2 + sobel_h(B)**2 + sobel_v(B)**2


def find_seam(img):
    x = dual_gradient_energy(img)
    x = x[1:-1, 1:-1]
    w = len(x[0])
    h = len(x)
    newarr = zeros((h, w))
    index = zeros((h, w), dtype=int32)
    seam = zeros(len(x), dtype=int32)

    for i in range(0, h):
        for j in range(0, w):
            if i == 0:
                newarr[i][j] = x[i][j]
                index[i][j] = 0
            else:
                newarr[i][j] = Infinity
                index[i][j] = -1

    for i in range(1, h):
        for j in range(0, w):
            shortest = Infinity
            Imin = -1
            if j is not 0:
                if newarr[i-1][j-1] < shortest:
                    shortest = newarr[i-1][j-1]
                    Imin = j-1
            if newarr[i-1][j] < shortest:
                shortest = newarr[i-1][j]
                Imin = j

            if j != w-1:
                if newarr[i-1][j+1] < shortest:
                    shortest = newarr[i-1][j+1]
                    Imin = j+1

            newarr[i][j] = shortest + x[i][j]
            index[i][j] = Imin

    min = Infinity
    tmin = -1

    for j in range(0, w):
        shortest = newarr[h-1][j]
        if shortest < min:
            min = shortest
            tmin = j

    seam = zeros(h, dtype=int32)
    seam[h-1] = tmin
    for i in range(h-2, -1, -1):
        seam[i] = index[i+1][seam[i+1]]
    seam = insert(seam, 0, seam[0])
    seam = append(seam, seam[h-1])
    print "Cost of Minimum seam :", min
    return seam


def plot_seam(img, seam):
    x = dual_gradient_energy(img)
    s = []
    for i in range(0, len(x)):
        s.append((seam[i], i))
    plt.tight_layout()
    plt.plot(*zip(*s), color='r')
    plt.imshow(x)


def remove_seam(img, seam):
    img = img_as_float(img)
    img = img.tolist()
    seam = seam.tolist()
    for i in range(0, len(img)):
        del img[i][seam[i]]
    plt.imshow(img)
    print "Width of the image is: ", len(img[0])
    return img


def remove_multiple_pixels(img, count):
    for i in range(0, count):
        img = remove_seam(img, find_seam(img))
        img = img_as_float(img)
    plt.imshow(img)


if __name__ == '__main__':
    img = imread("test1.png")
    img = img_as_float(img)
    print " Removing only 1 seam..."
    seam1 = find_seam(img)
    figure()
    gray()
    subplot(1, 5, 1)
    imshow(img)
    title("Orignal")
    subplot(1, 5, 2)
    imshow(dual_gradient_energy(img))
    title("Gradient")
    subplot(1, 5, 3)
    plot_seam(img, seam1)
    title("Seam Plotting")
    subplot(1, 5, 4)
    remove_seam(img, seam1)
    title("1 seam removed")
    print "Now Removing 50 seam..."
    subplot(1, 5, 5)
    remove_multiple_pixels(img, 50)
    title("50 seams removed")
    plt.imsave("carved.jpg", img)
    show()
