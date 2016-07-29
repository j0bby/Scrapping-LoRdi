# import the necessary packages
import numpy as np
import cv2
from scipy import ndimage
 
# load the image
image = ndimage.imread( "..\\Exemple-annonces\\ordi3.jpg")

import matplotlib.pyplot as plt
plt.imshow(image)
plt.show()

# find all the 'black' shapes in the image
lower = np.array([70, 2, 2]) #RGB
upper = np.array([250, 65, 65]) #RGB
red = cv2.inRange(image, lower, upper)
plt.imshow(red,cmap='gray')
plt.show()


lower = np.array([160, 160, 160]) #RGB
upper = np.array([250, 255, 255]) #RGB
red = cv2.inRange(image, lower, upper)
plt.imshow(red,cmap='gray')
plt.show()


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([115, 135, 135]) #RGB
upper = np.array([125, 255, 255]) #RGB
red = cv2.inRange(hsv, lower, upper)

plt.imshow(red)
plt.show()


gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret,thresh1 = cv2.threshold(gray,170,255,cv2.THRESH_BINARY)

plt.imshow(thresh1,'gray')
plt.show()


green = np.uint8([[[0,0,255]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)