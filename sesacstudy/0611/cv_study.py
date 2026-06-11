import cv2 as cv
import numpy as np

img = cv.imread("sesacstudy/0611/assets/RGB2.jpg",cv.IMREAD_GRAYSCALE)

if img is None:
    raise ValueError("Image not found or could not be read")

ret, binary_img = cv.threshold(img, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

print(ret)

cv.imshow('Original Image', img)
cv.imshow('THRESH_OTSU', binary_img)

cv.waitKey(0)
cv.destroyAllWindows()


