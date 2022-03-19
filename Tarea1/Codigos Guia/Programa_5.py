import cv2
import numpy as np 

#Insertar imagen
img = cv2.imread("Fresas.jpg")

#--------------------------------------------------------------------
#Convertir imagen a escala de grises
imgrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print(imgrey)

#Obtener los canales de una imagen
#-----------------------------------------------------------------------
b,g,r=cv2.split(img)

#Unir los canales de la imagen
img_u=cv2.merge([b,g,r])
#------------------------------------------------------------------------
#Mostrar imagen 
cv2.imshow('Imagen original',img)  #Mostrar imagen 
cv2.imshow('Imagen grises',imgrey)
cv2.imshow('Blue',b)
cv2.imshow('Green',g)
cv2.imshow('Red',r)
cv2.imshow('union',img_u)

#-----------------------------------------------------------------------
cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()