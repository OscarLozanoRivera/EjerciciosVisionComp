# Programa rotar, redimensionar, recortar y detectar bordes de imagen



import numpy as np
import cv2 as cv

#Insertar imagen
img = cv.imread("3objetos.jpg")

"""
#--------------------------------------------------------------------
#Rotar imagen 
#obtener ancho y alto de imagen
ancho= img.shape[1]
alto= img.shape[0]
#print(ancho, alto)

#Matriz de rotacion
                                            #Angulo
M = cv.getRotationMatrix2D((ancho//2,alto//2),45,1)
imgr = cv.warpAffine(img,M,(ancho,alto))
cv.imshow('Imagen original',imgr)

#----------------------------------------------------------------------
#Redimenzionar la imagen
imgd1= cv.resize(img,None,fx=0.5,fy=0.5)
ancho1= imgd1.shape[1]
alto1= imgd1.shape[0]
print(ancho1, alto1)
cv.imshow('Imagen original',img)

imgd2 = cv.resize(imgd1, (200,200))
ancho2= imgd2.shape[1]
alto2= imgd2.shape[0]
print(ancho2, alto2)
cv.imshow('Imagen redimensionada',imgd2)
#cv.imshow('Imagen original',imgd2)

#-----------------------------------------------------------------------
#Recortar imagen
#        Desde pixel: Hasta pixel
crop = img[300:400,300:400]
cv.imshow('Imagen recortada',crop)
cv.imshow('Imagen original',img)
"""
#-----------------------------------------------------------------------

#Detectar bordes de una imagen
edge_img = cv.Canny(img,200,200)
cv.imshow('Imagen con bordes',edge_img)
"""
#------------------------------------------------------------------------
#Mostrar imagen 
cv.imshow('Imagen original',img)  #Mostrar imagen 
#cv.imshow('Imagen rotada',imgr)
#cv.imshow('Imagen dim1',imgd1)
#cv.imshow('Imagen dim2',imgd2)
#cv.imshow('Imagen recortada',crop)
cv.imshow('Imagen recortada',edge_img)

#------------------------------------------------------------------------
#Guardar imagen
#cv.imwrite("C:/Users/em/Desktop/imagen.png",imgr)   #Guardar una imagen
#-----------------------------------------------------------------------
"""
cv.waitKey(0)  #comando para detener la imagen
cv.destroyAllWindows()





