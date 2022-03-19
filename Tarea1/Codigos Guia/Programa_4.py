import cv2
import numpy as np
import matplotlib.pyplot as plt 

#Insertar imagen
dirImagen="3 objetos.jpg"
img = cv2.imread(dirImagen)


#Calculo de Histograma
#--------------------------------------------------------------------
fig,axes=plt.subplots(nrows=2, ncols=2)
#Con OpenCV
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
#print(hist)
axes[0,0].plot(hist, color="r")

#Con Numpy
#hist2,bins = np.histogram(img.ravel(),256,[0,256])
#print(hist2)
#axes[0,1].plot(hist2, color="g") 

#Con matplotlib
#axes[1,0].hist(img.ravel(),256,[0,256])


#Con matplotlib para 3 canales

def histcolor (imagen):

    color = ('b','g','r')
    for i,col in enumerate(color):
        histr = cv2.calcHist([imagen],[i],None,[256],[0,256])
        plt.plot(histr,color = col)
        plt.xlim([0,256])

histcolor(img)
plt.show()

#------------------------------------------------------------------------
#Mostrar imagen 
cv2.imshow('Imagen original',img)  #Mostrar imagen 



#-----------------------------------------------------------------------
cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()