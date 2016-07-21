# import the necessary packages
import numpy as np
import cv2
from scipy import ndimage
 
# load the image
image = ndimage.imread( "Exemple-annonces\\ordi2.jpg")

import matplotlib.pyplot as plt
plt.imshow(image)
plt.show()

# find all the 'black' shapes in the image
lower = np.array([70, 2, 2]) #RGB
upper = np.array([250, 65, 65]) #RGB
shapeMask = cv2.inRange(image, lower, upper)

plt.imshow(shapeMask)
plt.show()