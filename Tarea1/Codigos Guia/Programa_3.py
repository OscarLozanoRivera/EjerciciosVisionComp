import cv2
import numpy as np

#Insertar imagen
img = cv2.imread("3 objetos.jpg")
""" 
#--------------------------------------------------------------------
#Convertir imagen a escala de grises
imgrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Escala de grises',imgrey)

"""
#-----------------------------------------------------------------------
#Binarizar una imagen
#t, imgbin1 = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_TRIANGLE)   

t2, imgbin2 = cv2.threshold(img, 75, 255, cv2.THRESH_BINARY) 

print(t2)
cv2.imshow('Imagen binarizada 2',imgbin2)

"""
#------------------------------------------------------------------------
#Mostrar imagen 
cv2.imshow('Imagen original',img)  #Mostrar imagen 
cv2.imshow('Imagen grises',imgrey)
cv2.imshow('Imagen binarizada',imgbin1)
cv2.imshow('Imagen binarizada 2',imgbin2)


#-----------------------------------------------------------------------
"""
cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()