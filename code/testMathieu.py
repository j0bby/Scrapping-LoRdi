import numpy as np
import cv2
from scipy import ndimage
import matplotlib.pyplot as plt
import math

def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255
    for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

def findCapot(image,freqRed):
    maxRed=0
    good=-1
    red = rotateImage(image, 0)
    nbRed=sum(sum(red ==255))
    freqRed=nbRed/(red.shape[1]*red.shape[0])
    for angle in range(0,95,5):
        red = rotateImage(image, angle)
        densityL=sum(red==255)/red.shape[0]
        startX=0
        freqtemp=freqRed
        while densityL[startX]<freqtemp:
            startX+=1
            if startX==len(densityL)-1:
                startX=0
                freqtemp*=0.9

        
        freqtemp=freqRed
        endX=-1
        while densityL[endX]<freqtemp:
            endX-=1
            if endX == -len(densityL)+startX:
                endX=-1
                freqtemp*=0.9
        endX+=len(densityL)

        
        
        Tred = np.transpose(red)
        densityC=sum(Tred==255)/Tred.shape[0]
        
        freqtemp=freqRed
        startY =0
        while densityC[startY]<freqtemp:
            startY+=1
            if startY==len(densityC)-1:
                startY=0
                freqtemp*=0.9

        
        freqtemp=freqRed
        endY =-1
        while densityC[endY]<freqRed:
            endY-=1
            if endY == -len(densityC)+startY:
                endY=-1
                freqtemp*=0.9
        endY+=len(densityC)

        

        temp= red[startY:endY,startX:endX]
        nbRed= sum(sum(temp==255))
        if nbRed>maxRed : 
            RstartX,RstartY,RendX,RendY=startX,startY,endX,endY
            maxRed=nbRed
            good = angle
    print(good) 
    return RstartX,RstartY,RendX,RendY, good
    
def rotateImage(src, angle,scale=1.):
    w = src.shape[1]
    h = src.shape[0]
    # now calculate new image width and height
    nw = (w**2+h**2)**0.5
    nh = nw
    # ask OpenCV for the rotation matrix
    rot_mat = cv2.getRotationMatrix2D((nw*0.5, nh*0.5), angle, scale)
    # calculate the move from the old center to the new center combined
    # with the rotation
    rot_move = np.dot(rot_mat, np.array([(nw-w)*0.5, (nh-h)*0.5,0]))
    # the move only affects the translation, so update the translation
    # part of the transform
    rot_mat[0,2] += rot_move[0]
    rot_mat[1,2] += rot_move[1]
    return cv2.warpAffine(src, rot_mat, (int(math.ceil(nw)), int(math.ceil(nh))), flags=cv2.INTER_LANCZOS4)

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

def recentre (pict):
    
    plt.imshow(pict,'gray')
    plt.show()
    tpict=np.transpose(pict)
    
    densityL=sum(tpict==0)

    densityC=sum(pict==0)
    
    startC=0
    endC=-1
    while densityC[startC]==0:
        startC+=1
    
    while densityC[endC]==0:
        endC-=1
        
    print(startC)
    print(endC)
    
    startL=0
    endL=-1
    while densityL[startL]==0:
        startL+=1
    
    while densityL[endL]==0:
        endL-=1
        
    print(startL)
    print(endL)
    
    return startL,endL,startC,endC
    
def isRed(img):
    fRed=sum(sum(img==255))/(img.shape[0]*img.shape[1])
    print(fRed)
    return fRed>0.9
    
def extendArea(pict,startX,startY,endX,endY):
    
    while sum(pict[startY:endY,startX]==0)!=0 and startX>0:
        startX-=1
    print(startX)
    
    while sum(pict[startY:endY,endX]==0)!=0 and endX<pict.shape[1]-1:
        endX+=1
    print(endX)    

    while sum(pict[startY,startX:endX]==0)!=0 and startY>0:
        startY-=1
    print(startY)
    
    while sum(pict[endY,startX:endX]==0)!=0 and endY<pict.shape[0]-1:
        endY+=1
    print(endY)
    
    return startX,endX,startY,endY
    

def MethodeMoy(dilated):
    tdil=np.transpose(dilated)
    densityL=sum(tdil==255)/tdil.shape[0]
    densityC=sum(dilated==255)/dilated.shape[0]
    moyL=sum(densityL)/sum(densityL>0)
    moyC=sum(densityC)/sum(densityC>0)
    print("-----------------------------------------------------------------------------")
    print(moyL)
    print(moyC)
    print("-----------------------------------------------------------------------------")
    
    tdil=np.transpose(dilated)
    densityL=sum(tdil==255)/tdil.shape[0]
    densityC=sum(dilated==255)/dilated.shape[0]
    zoneL=[]
    zonestart=-1
    for i in range(len(densityL)-1):
        if densityL[i]>=moyL:
            if zonestart==-1 :
                zonestart=i
            
        elif zonestart!=-1 and densityL[i]<moyL:
            zoneL.append([zonestart,i])
            zonestart=-1
        
    if zonestart!=-1:
        zoneL.append([zonestart,len(densityL)-1])
    print(zoneL)
    
    zoneC=[]
    zonestart=-1
    for i in range(len(densityC)-1):
        if densityC[i]>=moyC:
            if zonestart==-1 :
                zonestart=i
            
        elif zonestart!=-1 and densityC[i]<moyC:
            zoneC.append([zonestart,i])
            zonestart=-1
        
    if zonestart!=-1:
        zoneC.append([zonestart,len(densityC)-1])
    print(zoneC)

    return zoneL,zoneC
    
image = cv2.imread("..\\Exemple-annonces\\oo4.jpg")
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
    startX,startY,endX,endY, angle = findCapot(red,freqRed)
    image= rotateImage(image,angle)
    img = image[startY:endY,startX:endX]
    cv2.imwrite('subimg.png',img)
    red = rotateImage(red,angle)
    red= red[startY:endY,startX:endX]
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
    
    # TODO: enlever le bruit issue des bords trop clairs 
    if sum(binaire[0,:]==0)>3:
        print("premire ligne")
    if sum(binaire[-1,:]==0)>3:
        print("derniere ligne")
    if sum(binaire[:,0]==0)>3:
        print("premire colone")
    if sum(binaire[:,-1]==0)>3:
        print("derniere colone")
        
    dilated = locateLogo(binaire)
    MethodeMoy(dilated)
    zoneL,zoneC=findLogo(dilated)
    zoneLb,zoneCb=MethodeMoy(dilated)
    
    for l in zoneLb:
        for c in zoneCb:
            propBlancs = sum(sum(dilated[l[0]:l[1],c[0]:c[1]]))
            if propBlancs>0.5:
                if isRed(red[l[0]:l[1],c[0]:c[1]])==False:
                    cv2.rectangle(img, (c[0], l[0]), (c[1], l[1]), (0, 255, 0), 2)
                    
                    #recentre la zone sur le logo (à partir de l'image rouge)
                    startL,endL,startC,endC = recentre(red[l[0]:l[1],c[0]:c[1]])
                    cv2.rectangle(img, (c[0]+startC, l[0]+startL), (c[1]+endC, l[1]+endL), (255, 0, 0), 2)
                    
                    #agrandi la zone si on trouve toujours des zones non rouges autour
                    startX,endX,startY,endY = extendArea(red,c[0]+startC , l[0]+startL , c[1]+endC ,l[1]+endL)
                    cv2.rectangle(img, (startX, startY), (endX, endY), (255, 255, 255), 2)
            
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    logoPosition={}
    pos=0
    for l in zoneL:
        for c in zoneC:
            propBlancs = sum(sum(dilated[l[0]:l[1],c[0]:c[1]]))
            if propBlancs>0.5:
                if isRed(red[l[0]:l[1],c[0]:c[1]])==False:
                    cv2.rectangle(img, (c[0], l[0]), (c[1], l[1]), (0, 255, 0), 2)
                    
                    #recentre la zone sur le logo (à partir de l'image rouge)
                    startL,endL,startC,endC = recentre(red[l[0]:l[1],c[0]:c[1]])
                    cv2.rectangle(img, (c[0]+startC, l[0]+startL), (c[1]+endC, l[1]+endL), (255, 0, 0), 2)
                    
                    #agrandi la zone si on trouve toujours des zones non rouges autour
                    startX,endX,startY,endY = extendArea(red,c[0]+startC , l[0]+startL , c[1]+endC ,l[1]+endL)
                    
                    #TODO : si c'est au bord ca dégage (marche pas tous le temps)
                    if startX==0 or startY==0 or endX==red.shape[0]-1 or endY==red.shape[1]-1:
                        print("AU BORD DONC DEGAGE")
                    else :
                        logoPosition[pos]=[startX,startY,endX,endY]
                        cv2.rectangle(img, (startX, startY), (endX, endY), (255, 255, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    
elif freqRed>0.05 :
    print("Some Red")
elif freqRed>0.02:
    print("some Red")
else:
    print("not ordi")




