import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
    for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def findCapot(red,freqRed):

    densityL=sum(red==255)/red.shape[0]
    startX=0
    freqtemp=freqRed
    while densityL[startX]<freqtemp:
        startX+=1
        if startX==len(densityL)-1:
            startX=0
            freqtemp*=0.9
    print(startX)
    
    freqtemp=freqRed
    endX=-1
    while densityL[endX]<freqtemp:
        endX-=1
        if endX == -len(densityL)+startX:
            endX=-1
            freqtemp*=0.9
    endX+=len(densityL)
    print(endX)
    
    
    Tred = np.transpose(red)
    densityC=sum(Tred==255)/Tred.shape[0]
    
    freqtemp=freqRed
    startY =0
    while densityC[startY]<freqtemp:
        startY+=1
        if startY==len(densityC)-1:
            startY=0
            freqtemp*=0.9
    print(startY)
    
    freqtemp=freqRed
    endY =-1
    while densityC[endY]<freqRed:
        endY-=1
        if endY == -len(densityC)+startY:
            endY=-1
            freqtemp*=0.9
    endY+=len(densityC)
    print(endY)
    
    print(densityL)
    print(densityC)
    return startX,startY,endX,endY

def locateLogo(image):
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    dilated = cv2.dilate(image, kernel, iterations = 1)
    plt.imshow(dilated,'gray')
    plt.show()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
    eroded = cv2.erode(dilated, kernel, iterations = 2)

    plt.imshow(eroded,'gray')
    plt.show()
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (6,6))
    dilated = cv2.dilate(eroded, kernel, iterations = 2)
    
    contour = cv2.Canny(dilated, 50, 200)
    
    plt.imshow(dilated,'gray')
    plt.show()
    cv2.imshow("Image", contour)
    cv2.waitKey(0)
    
    return dilated
    
def findLogo(dilated):
    tdil=np.transpose(dilated)
    nbBlanc=sum(sum(tdil==255))
    freqBlanc=nbBlanc/(dilated.shape[0]*dilated.shape[1])
    densityL=sum(tdil==255)/tdil.shape[0]
    print(densityL)
    densityC=sum(dilated==255)/dilated.shape[0]
    zoneL=[]
    zonestart=-1
    for i in range(len(densityL)-1):
        if densityL[i]!=0:
            if zonestart==-1 :
                zonestart=i
            
        elif zonestart!=-1:
            zoneL.append([zonestart,i])
            zonestart=-1
        
    if zonestart!=-1:
        zoneL.append([zonestart,len(densityL)-1])
    print(zoneL)
    
    zoneC=[]
    zonestart=-1
    for i in range(len(densityC)-1):
        if densityC[i]!=0:
            if zonestart==-1 :
                zonestart=i
            
        elif zonestart!=-1:
            zoneC.append([zonestart,i])
            zonestart=-1
        
    if zonestart!=-1:
        zoneC.append([zonestart,len(densityC)-1])
    print(zoneC)

    return zoneL,zoneC
    
    
image = cv2.imread("..\\Exemple-annonces\\oo1.jpg")
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

lower = np.array([120, 80, 80]) 
upper = np.array([179, 255, 255]) 
red = cv2.inRange(hsv, lower, upper)
lower = np.array([0, 80, 80]) 
upper = np.array([5, 255, 255]) 
red += cv2.inRange(hsv, lower, upper)
nbRed=sum(sum(red ==255))
freqRed=nbRed/(red.shape[1]*red.shape[0])
print(freqRed)

if freqRed >0.2 :
    if freqRed>0.8:
        print("Care, background Red")
    else :
        print("Red computer")
    startX,startY,endX,endY = findCapot(red,freqRed)
    
    img = image[startY:endY,startX:endX]

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(20,20))
    gray = clahe.apply(gray)
    cv2.fastNlMeansDenoising(gray,gray,30,41,61)
    cv2.imshow("Image", gray)
    cv2.waitKey(0)
    _,binaire = cv2.threshold(gray,180,255,cv2.THRESH_BINARY)
    plt.imshow(binaire,'gray')
    plt.show()
    cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
    cv2.imshow("Image", image)
    cv2.waitKey(0)
    
    dilated = locateLogo(binaire)
    zoneL,zoneC=findLogo(dilated)
    
    for l in zoneL:
        for c in zoneC:
            propBlancs = sum(sum(dilated[l[0]:l[1],c[0]:c[1]]))
            if propBlancs>0.5:
                
                cv2.rectangle(img, (c[0], l[0]), (c[1], l[1]), (0, 255, 0), 2)
            
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    
elif freqRed>0.05 :
    print("Some Red")
elif freqRed>0.02:
    print("some Red")
else:
    print("not ordi")




