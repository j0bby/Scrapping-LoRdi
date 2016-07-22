import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import imutils

# load the image
img2 = ndimage.imread( "..\\Exemple-annonces\\ordi7.jpg")
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
img2 = imutils.auto_canny(img2)

img1 = ndimage.imread( "..\\Exemple-annonces\\template.jpg")
img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img1 = imutils.auto_canny(img1)

# Initiate SIFT detector
orb = cv2.ORB_create()
# find the keypoints and descriptors with SIFT
kp1, des1 = orb.detectAndCompute(img1,None)
kp2, des2 = orb.detectAndCompute(img2,None)

# create BFMatcher object
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# Match descriptors.
matches = bf.match(des1,des2)

# Sort them in the order of their distance.
matches = sorted(matches, key = lambda x:x.distance)

# Draw first 10 matches.
img3=img2.copy()
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:10],img3)
cv2.drawMatches
plt.imshow(img3),plt.show()