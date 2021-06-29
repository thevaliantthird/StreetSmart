import cv2 as cv

for i in range(1,116):
    im = cv.imread('screenshots/' + str(i) + '.png')
    im[865:,777:1142,:] = 255
    im[880:,:100,:] = 255
    im[:160,:22,:] = 255
    im[800:,1870:,:] = 255
    im[:150,1800:,:] = 255
    cropped = im[100:980]
    cv.imwrite('cropped_screenshots/' + str(i) + '.png',cropped)

