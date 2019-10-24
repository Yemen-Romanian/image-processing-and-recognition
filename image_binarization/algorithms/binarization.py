import numpy as np


def otsu(image_hist, imax=256, eps=0.0001):
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
    hist = np.zeros(256)
    for i in range(image.shape[0]):
        for j in range(image.shape[1]):
            hist[image[i, j]] += 1
    
    return hist


def get_grayscale(image, input='BGR'):
    if input == 'BGR':
        coefficients = [0.11, 0.53, 0.36]
    else:
        coefficients = [0.36, 0.53, 0.11]

    grayscale = np.zeros(image.shape[:-1])
    for channel in range(image.shape[2]):
        grayscale += coefficients[channel] * image[:, :, channel]

    return grayscale.astype(np.int)
