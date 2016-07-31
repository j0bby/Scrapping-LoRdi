import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt

def findCapot(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    lower = np.array([115, 135, 135]) #RGB
    upper = np.array([125, 255, 255]) #RGB
    red = cv2.inRange(hsv, lower, upper)
    
    densityL=sum(red==255)/red.shape[1]
    print(densityL)
    startX=0
    while densityL[startX]<0.2:
        startX+=1
    print(startX)
    
    endX=-1
    while densityL[endX]<0.2:
        endX-=1
    endX+=len(densityL)
    print(endX)
    
    
    Tred = np.transpose(red)
    densityC=sum(Tred==255)/Tred.shape[0]
    print(densityC)
    startY =0
    while densityC[startY]<0.2:
        startY+=1
    print(startY)
    
    endY =-1
    while densityC[endY]<0.2:
        endY-=1
    endY+=len(densityC)
    print(endY)
    return startX,startY,endX,endY



image = ndimage.imread( "..\\Exemple-annonces\\ordi5.jpg")

lower = np.array([70, 2, 2]) #RGB
upper = np.array([250, 65, 65]) #RGB
red = cv2.inRange(image, lower, upper)
nbRed=sum(sum(red ==255))
freqRed=nbRed/(red.shape[1]*red.shape[0])
print(freqRed)

hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)   
lower = np.array([115, 135, 135]) #RGB
upper = np.array([125, 255, 255]) #RGB
redH = cv2.inRange(hsv, lower, upper)
nbRedH=sum(sum(redH ==255))
freqRedH=nbRedH/(redH.shape[1]*redH.shape[0])
print(freqRedH)


if freqRed >0.3 :
    if freqRedH<0.3:
        print("not lordi, check background")
    else :
        print("Red computer")
        startX,startY,endX,endY = findCapot(image)
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
elif freqRed>0.05 :
    print("housse region")
elif freqRed>0.02:
    print("some Red")
else:
    print("not ordi")




