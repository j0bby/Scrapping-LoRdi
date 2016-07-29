import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import numpy as np


def dist(u,v):
    vect = [u[0]-v[0],u[1]-v[1]]
    return ((vect[0]**2)+(vect[1]**2))**0.5
    
img = ndimage.imread( "..\\Exemple-annonces\\ordi3.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)


dst = cv2.cornerHarris(gray,2,3,0.04)
dst = cv2.dilate(dst,None)
ret, dst = cv2.threshold(dst,0.01*dst.max(),255,0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)

# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray,np.float32(centroids),(5,5),(-1,-1),criteria)

# Now draw them
res = np.hstack((centroids,corners))
res = np.int0(res)
img[res[:,1],res[:,0]]=[0,0,255]
img[res[:,3],res[:,2]] = [0,255,0]




res2=[]
for i in range(len(res)):
    res2.append(res[i,:2])
    res2.append(res[i,2:])

tot=0
cpt=0
for i in res2:
    for j in res2:
        if all(j!=i):
            tot+=dist(i,j)
            cpt+=1

moy=tot/cpt
print(tot/cpt)

packs=[[] for i in range(len(res2))]
for i in range(len(res2)) :
    for j in res2:
        if dist(res2[i],j)<0.2*moy:
            packs[i].append(j)
            

                
         




cv2.imwrite('subpixel5.png',img)