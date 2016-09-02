import numpy as np
import cv2

import matplotlib.pyplot as plt
import math
import imutils

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
    while startC<len(densityC) and densityC[startC]==0  :
        startC+=1
    
    while endC>startC-len(densityC) and densityC[endC]==0  :
        endC-=1
        
    print(startC)
    print(endC)
    
    startL=0
    endL=-1
    while startL<len(densityL) and densityL[startL]==0:
        startL+=1
    
    while endL>startL-len(densityL) and densityL[endL]==0:
        endL-=1
        
    print(startL)
    print(endL)
    
    return startL,endL,startC,endC
    
def isRed(img):
    fRed=sum(sum(img==255))/(img.shape[0]*img.shape[1])
    print(fRed)
    return fRed>0.9
    
def extendArea(pict,startX,startY,endX,endY):
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4,4))
    pict = cv2.dilate(pict, kernel, iterations = 2)
    
    while sum(pict[startY:endY,startX]==255)!=0 and startX>0:
        startX-=1
    print(startX)
    
    while sum(pict[startY:endY,endX]==255)!=0 and endX<pict.shape[1]-1:
        endX+=1
    print(endX)    

    while sum(pict[startY,startX:endX]==255)!=0 and startY>0:
        startY-=1
    print(startY)
    
    while sum(pict[endY,startX:endX]==255)!=0 and endY<pict.shape[0]-1:
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
    
    
def getOutside(zones):
    #TODO : améliorer cette méthode

    for partie in range(len(zones)) : 
            for k in range(len(zones)) :
                if k!=partie:
                    if isInside(zones[partie][0],zones[partie][2],zones[partie][1],zones[partie][3],zones[k][0],zones[k][2])==True and isInside(zones[partie][0],zones[partie][2],zones[partie][1],zones[partie][3],zones[k][1],zones[k][3])==True :
                        print("inside")
                        zones[k]=[0,0,0,0]
                        
                    elif isInside(zones[partie][0],zones[partie][2],zones[partie][1],zones[partie][3],zones[k][0],zones[k][2])==True and isInside(zones[partie][0],zones[partie][2],zones[partie][1],zones[partie][3],zones[k][1],zones[k][3])==False :
                        print("prems")                        
                        zones[partie][1]=zones[k][1]
                        zones[partie][3]=zones[k][3]
                        zones[k]=[0,0,0,0]
                    elif isInside(zones[partie][0],zones[partie][2],zones[partie][1],zones[partie][3],zones[k][0],zones[k][2])==False and isInside(zones[partie][0],zones[partie][2],zones[partie][1],zones[partie][3],zones[k][1],zones[k][3])==True :
                        print("sec")                        
                        zones[partie][0]=zones[k][0]
                        zones[partie][2]=zones[k][2]
                        zones[k]=[0,0,0,0]
    ret =[]
    for k in zones:
        if k != [0,0,0,0] :
            ret.append(k)
    return ret
    
def isInside(x1,y1, x2,y2, xx, yy):
    if xx>=x1 and xx<=x2 and yy>=y1 and yy<=y2:
        print(str(x1) + " "+ str(y1) + " " + str(x2) + " " + str(y2)+ " " + str(xx)+ " " + str(yy) )
        return True
    else: return False


image = cv2.imread("..\\Exemple-annonces\\oo2.jpg")
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

if freqRed >0.15 :
    if freqRed>0.8:
        print("Care, background Red")
    else :
        print("Red computer")
    #réduit au capot de l'ordi (rotation pour récupérer bien)
    startX,startY,endX,endY, angle = findCapot(red,freqRed)
    
    #réduit image normale
    image= rotateImage(image,angle)
    img = image[startY:endY,startX:endX]
    im=img.copy() # copie 
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    contours = cv2.Canny(gray, 30, 200)
    cv2.imshow("Image", contours)
    cv2.waitKey(0)
    
    #réduit le red
    red = rotateImage(red,angle)
    red= red[startY:endY,startX:endX]
    
    #traitement homogénéisation lumière
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=8, tileGridSize=(20,20))
    gray = clahe.apply(gray)
    cv2.fastNlMeansDenoising(gray,gray,30,41,61)
    cv2.imshow("Image", gray)
    cv2.waitKey(0)
    
    
    edged = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(edged, 30, 200)
    cv2.imshow("Image", edged)
    cv2.waitKey(0)
    
    #binarisation
    _,binaire = cv2.threshold(gray,180,255,cv2.THRESH_BINARY)
    plt.imshow(binaire,'gray')
    plt.show()
    
    #affiche ou est le capot
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
        
    dilated = locateLogo(edged)
    MethodeMoy(dilated)
    zoneL,zoneC=findLogo(dilated)
    zoneLb,zoneCb=MethodeMoy(dilated)

    zones=[]
    for l in zoneLb:
        for c in zoneCb:
            propBlancs = sum(sum(dilated[l[0]:l[1],c[0]:c[1]]))
            if propBlancs>0.5:
                if isRed(red[l[0]:l[1],c[0]:c[1]])==False:
                    cv2.rectangle(img, (c[0], l[0]), (c[1], l[1]), (0, 255, 0), 2)
                    
                    #recentre la zone sur le logo (à partir de l'image rouge)
                    startL,endL,startC,endC = recentre(red[l[0]:l[1],c[0]:c[1]])
                    cv2.rectangle(img, (c[0]+startC, l[0]+startL), (c[1]+endC, l[1]+endL), (255, 0, 0), 2)
                    
                    #agrandi la zone si on trouve toujours des contours autour
                    
                    startX,endX,startY,endY = extendArea(contours,c[0]+startC , l[0]+startL , c[1]+endC ,l[1]+endL)
                    cv2.rectangle(img, (startX, startY), (endX, endY), (255, 255, 255), 2)
                    if  endX - startX >10 and endY - startY >10:
                        zones.append([startX,endX,startY,endY])
                    
    cv2.imshow("Image", img)
    cv2.waitKey(0)
    
    print("*"*100)
    print(zones)
    zones = getOutside(zones)
    print("*"*100)
    print(zones)
    

    for z in zones :
        cv2.rectangle(im, (z[0], z[2]), (z[1], z[3]), (255, 255, 255), 2) 
    cv2.imshow("Image", im)
    cv2.waitKey(0)
    
    #logoreco 
    
    template = cv2.imread("..\\Exemple-annonces\\template5.jpg")
    template= cv2.flip(template, -1)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    template = cv2.Canny(template, 50, 200)
    (tH, tW) = template.shape[:2]
    
    for z in zones:
        logo = im[z[2]:z[3],z[0]:z[1]]
        logo = cv2.cvtColor(logo, cv2.COLOR_BGR2GRAY)
        plt.imshow(logo,'gray')
        plt.show()
        found = None
        for rotangle in range(0,360,20):
            grayt = rotateImage(logo,rotangle)
        # loop over the scales of the image
            for scale in np.linspace(0.5, 3, 50)[::-1]:
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
                result = cv2.matchTemplate(edged, template, cv2.TM_CCOEFF_NORMED)
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
        print(found[0])
        if found[0]>0.25:
            print('-'*100 + '\n' + '*'*100)
            print("TROUVéééééééééééééééééééééééééééééé")
            print('-'*100 + '\n' + '*'*100)
        # draw a bounding box around the detected result and display the image
        image=rotateImage(logo,found[3])
        cv2.rectangle(image, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("Image", image)
        cv2.waitKey(0)
#    logoPosition={}
#    pos=0
#    for l in zoneL:
#        for c in zoneC:
#            propBlancs = sum(sum(dilated[l[0]:l[1],c[0]:c[1]]))
#            if propBlancs>0.5:
#                if isRed(red[l[0]:l[1],c[0]:c[1]])==False:
#                    cv2.rectangle(img, (c[0], l[0]), (c[1], l[1]), (0, 255, 0), 2)
#                    
#                    #recentre la zone sur le logo (à partir de l'image rouge)
#                    startL,endL,startC,endC = recentre(red[l[0]:l[1],c[0]:c[1]])
#                    cv2.rectangle(img, (c[0]+startC, l[0]+startL), (c[1]+endC, l[1]+endL), (255, 0, 0), 2)
#                    
#                    #agrandi la zone si on trouve toujours des zones non rouges autour
#                    startX,endX,startY,endY = extendArea(red,c[0]+startC , l[0]+startL , c[1]+endC ,l[1]+endL)
#                    
#                    #TODO : si c'est au bord ca dégage (marche pas tous le temps)
#                    if startX==0 or startY==0 or endX==red.shape[0]-1 or endY==red.shape[1]-1:
#                        print("AU BORD DONC DEGAGE")
#                    else :
#                        logoPosition[pos]=[startX,startY,endX,endY]
#                        cv2.rectangle(img, (startX, startY), (endX, endY), (255, 255, 255), 2)
#    cv2.imshow("Image", img)
#    cv2.waitKey(0)
    
elif freqRed>0.05 :
    print("Some Red")
elif freqRed>0.02:
    print("some Red")
else:
    print("not ordi")




