import cv2
from matplotlib import pyplot as plt
from scipy import ndimage
import imutils
import numpy as np

img = ndimage.imread( "..\\Exemple-annonces\\ordi1.jpg")
h=len(img)
l=len(img[0])

# découpage de l'image:
nb_cells=16
pas_h=int(h/nb_cells)
pas_l=int(l/nb_cells)
cells ={}
for i in range(1,nb_cells-2):
    for j in range(1,nb_cells-2):
        if (i+1)*pas_h>h:
           end_i = -1
        else :
            end_i=(i+1)*pas_h
        if (j+1)*pas_h>l:
            end_j=-1
        else :
            end_j=(j+1)*pas_l
        
        cells[(i,j)]=img[(i-1)*pas_h:end_i,(j-1)*pas_l:(j+1)*pas_l]
        


plt.imshow(cells[(1,3)])
plt.show()

