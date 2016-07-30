# import the necessary packages
import numpy as np
import imutils
import glob
import cv2
import math

def rotateImage(image, angle):
  rows, cols = image.shape
  rot_mat = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
  diag = int(0.8*math.sqrt(cols**2+rows**2))
  result = cv2.warpAffine(image, rot_mat, (diag,diag),flags=cv2.INTER_LINEAR)
  return result



# load the image image, convert it to grayscale, and detect edges
template = cv2.imread("..\\Exemple-annonces\\template4.jpg")
template= cv2.flip(template, -1)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
image = cv2.imread("..\\Exemple-annonces\\ordi3.jpg")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
found = None
for rotangle in range(0,360,20):
    grayt = rotateImage(gray,rotangle)
# loop over the scales of the image
    for scale in np.linspace(0.2, 1.0, 20)[::-1]:
        # resize the image according to the scale, and keep track
        # of the ratio of the resizing
        resized = imutils.resize(grayt, width = int(grayt.shape[1] * scale))
        r = grayt.shape[1] / float(resized.shape[1])

        # if the resized image is smaller than the template, then break
        # from the loop
        if resized.shape[0] < tH or resized.shape[1] < tW:
            break
        # detect edges in the resized, grayscale image and apply template
        # matching to find the template in the image
        edged = cv2.Canny(resized, 50, 200)
        result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF)
        (_, maxVal, _, maxLoc) = cv2.minMaxLoc(result)
        # if we have found a new maximum correlation value, then ipdate
        # the bookkeeping variable
        if found is None or maxVal > found[0]:
            found = (maxVal, maxLoc, r)

# unpack the bookkeeping varaible and compute the (x, y) coordinates
# of the bounding box based on the resized ratio
(_, maxLoc, r) = found
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

# draw a bounding box around the detected result and display the image
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)