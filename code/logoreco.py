# import the necessary packages
import numpy as np
import imutils
import cv2
import math
from scipy import ndimage


def rotateImage(image, angle):
  rows, cols = image.shape
  rot_mat = cv2.getRotationMatrix2D((cols/2,rows/2),angle,1)
  diag = int(0.8*math.sqrt(cols**2+rows**2))
  result = cv2.warpAffine(image, rot_mat, (diag,diag),flags=cv2.INTER_LINEAR)
  return result

def initimage(image) :
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    lower = np.array([115, 135, 135])  # RGB
    upper = np.array([125, 255, 255])  # RGB
    red = cv2.inRange(hsv, lower, upper)

    densityL = sum(red == 255) / red.shape[1]
    startX = 0
    while densityL[startX] < 0.2:
        startX += 1

    endX = -1
    while densityL[endX] < 0.2:
        endX -= 1
    endX += len(densityL)

    Tred = np.transpose(red)
    densityC = sum(Tred == 255) / Tred.shape[0]
    print(densityC)
    startY = 0
    while densityC[startY] < 0.2:
        startY += 1

    endY = -1
    while densityC[endY] < 0.2:
        endY -= 1
    endY += len(densityC)
    crop_img = image[startY:endY, startX:endX]
    return crop_img

# load the image image, convert it to grayscale, and detect edges
template = cv2.imread("..\\Exemple-annonces\\template4.jpg")
template= cv2.flip(template, -1)
template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
template = cv2.Canny(template, 50, 200)
(tH, tW) = template.shape[:2]
image2 = ndimage.imread( "..\\Exemple-annonces\\ordi3.jpg")
image = initimage(image2)
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
            found = (maxVal, maxLoc, r,rotangle)

# unpack the bookkeeping varaible and compute the (x, y) coordinates
# of the bounding box based on the resized ratio
(_, maxLoc, r) = (found[0],found[1],found[2])
(startX, startY) = (int(maxLoc[0] * r), int(maxLoc[1] * r))
(endX, endY) = (int((maxLoc[0] + tW) * r), int((maxLoc[1] + tH) * r))

# draw a bounding box around the detected result and display the image
image=rotateImage(gray,found[3])
cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
cv2.imshow("Image", image)
cv2.waitKey(0)