
import numpy as np
import cv2
import math

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
  
image = cv2.imread("..\\Exemple-annonces\\oo14.jpg")
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
        startX,startY,endX,endY,angle = findCapot(red,freqRed)
        rot= rotateImage(image, angle)
        cv2.rectangle(rot, (startX, startY), (endX, endY), (0, 0, 255), 2)
        cv2.imshow("Image", rot)
        cv2.waitKey(0)