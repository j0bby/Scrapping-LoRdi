import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt

def findCapot(red):
    
    densityL=sum(red==255)/red.shape[1]
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

def locateLogo(image):
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    eroded = cv2.erode(image, kernel, iterations = 1)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
    dilated = cv2.dilate(eroded, kernel, iterations = 1)
    cv2.imwrite('dilated.png',dilated)
    contour = cv2.Canny(dilated, 50, 200)
    cv2.imwrite('contour.png',contour)
    plt.imshow(dilated,'gray')
    plt.show()
    cv2.imshow("Image", contour)
    cv2.waitKey(0)
    tdil=np.transpose(dilated)
    nbBlanc=sum(sum(tdil==255))
    densityL=sum(tdil==255)/nbBlanc
    print(densityL)
    
    
image = cv2.imread("..\\Exemple-annonces\\oo1.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([120, 80, 80]) #RGB
upper = np.array([179, 255, 255]) #RGB
red = cv2.inRange(hsv, lower, upper)
nbRed=sum(sum(red ==255))
freqRed=nbRed/(red.shape[1]*red.shape[0])
print(freqRed)

if freqRed >0.2 :
    if freqRed>0.8:
        print("Care, background Red")
    else :
        print("Red computer")
    startX,startY,endX,endY = findCapot(red)
    
    img = image[startY:endY,startX:endX]
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    _,binaire = cv2.threshold(gray,170,255,cv2.THRESH_BINARY)
    
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
    locateLogo(binaire)
    
    
elif freqRed>0.05 :
    print("Some Red")
elif freqRed>0.02:
    print("some Red")
else:
    print("not ordi")




