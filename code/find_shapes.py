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
shapeMask = cv2.inRange(image, lower, upper)

plt.imshow(shapeMask)
plt.show()

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([115, 135, 135]) #RGB
upper = np.array([125, 255, 255]) #RGB
red = cv2.inRange(hsv, lower, upper)

plt.imshow(red)
plt.show()

green = np.uint8([[[0,0,255]]])
hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
print(hsv_green)