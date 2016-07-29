import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import imutils
import numpy as np

# load the image
img2 = ndimage.imread( "..\\Exemple-annonces\\ordi3.jpg")
lower = np.array([70, 2, 2]) #RGB
upper = np.array([250, 65, 65]) #RGB
#img2 = cv2.inRange(img2, lower, upper)

#img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
#img2 = imutils.auto_canny(img2)

img1 = ndimage.imread( "..\\Exemple-annonces\\template.jpg")
#img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#img1 = imutils.auto_canny(img1)

#img1 = cv2.inRange(img1, lower, upper)

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
#matches = sorted(matches, key = lambda x:x.distance)


good = []
for m in range(len(matches)):
    for n in range(len(matches)):
        if matches[m].distance < 0.8*matches[n].distance:
            good.append(matches[m])            

MIN_MATCH_COUNT = 10
        
if len(good)>MIN_MATCH_COUNT:
    src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5.0)
    matchesMask = mask.ravel().tolist()
    h,w, c = img1.shape
    pts = np.float32([ [0,0],[0,h-1],[w-1,h-1],[w-1,0] ]).reshape(-1,1,2)
    dst = cv2.perspectiveTransform(pts,M)

    img2 = cv2.polylines(img2,[np.int32(dst)],True,255,3, cv2.LINE_AA)

else:
    print ("Not enough matches are found"+ str(len(good)) + " " + str(MIN_MATCH_COUNT))
    matchesMask = None
    
    
draw_params = dict(matchColor = (0,255,0), # draw matches in green color
                   singlePointColor = None,
                   matchesMask = matchesMask, # draw only inliers
                   flags = 2)

img3 = cv2.drawMatches(img1,kp1,img2,kp2,good,None,**draw_params)

plt.imshow(img3),plt.show()

# Draw first 10 matches.
img3=img2.copy()
img3 = cv2.drawMatches(img1,kp1,img2,kp2,matches[:20],img3)
cv2.drawMatches
plt.imshow(img3),plt.show()