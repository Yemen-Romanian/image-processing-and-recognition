import numpy as np
import cv2
import matplotlib.pyplot as plt


def otsu(image_hist, imax=255, eps=0.0001):
    pxl_probs = image_hist / np.sum(image_hist)
    variances = []

    first_group_probs = 0
    second_group_probs = np.sum(pxl_probs[:imax + 1])

    for t in range(imax):
        first_group_probs += pxl_probs[t]
        second_group_probs -= pxl_probs[t]

        mu_first = np.sum(np.arange(t + 1) * pxl_probs[:t + 1]) / (first_group_probs + eps)
        mu_second = np.sum(np.arange(t + 1, imax) * pxl_probs[t + 1:imax + 1]) / (second_group_probs + eps)

        sigma_first = np.sum((np.arange(t + 1) - mu_first)**2 * pxl_probs[: t + 1]) / (first_group_probs + eps)
        sigma_second = np.sum((np.arange(t + 1, imax) - mu_second)**2 * pxl_probs[t + 1: imax + 1]) / (second_group_probs + eps)

        variance = first_group_probs * sigma_first + second_group_probs * sigma_second
        variances.append(variance)

    return np.argmin(variances)


def histogram(image):
    hist = np.zeros(255)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            hist[image[i, j]] += 1
    
    return hist


if __name__ == '__main__':
    image = cv2.imread('examples/Lenna_(test_image).png')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plt.imshow(image, cmap='gray')
    plt.title('Original image')
    plt.show()

    threshold = otsu(histogram(image))
    binarized_image = image > threshold
    plt.imshow(binarized_image, cmap='gray')
    plt.title('Otsu method')
    plt.show()

