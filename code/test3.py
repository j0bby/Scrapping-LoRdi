from skimage import exposure
from skimage import feature
import cv2
from scipy import ndimage
import imutils
import matplotlib.pyplot as plt
import numpy as np

image = ndimage.imread( "..\\Exemple-annonces\\ordi7.jpg")
plt.imshow(image)
plt.show()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([115, 135, 135]) #RGB
upper = np.array([125, 255, 255]) #RGB
red = cv2.inRange(hsv, lower, upper)

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
plt.imshow(gray,cmap='gray')
plt.show()

edged = imutils.auto_canny(red)
plt.imshow(edged,cmap='gray')
plt.show()

im2,contours, hierarchy = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

contours.sort(key=cv2.contourArea,reverse=True )
area = [cv2.contourArea(contours[i]) for i in range(len(contours)) ]
(x, y, w, h) = cv2.boundingRect(contours[1])
logo = gray[y:y + h, x:x + w]

 
plt.imshow(logo)
plt.show()

H = feature.hog(logo, orientations=9, pixels_per_cell=(10, 10),
		cells_per_block=(2, 2), transform_sqrt=True)
