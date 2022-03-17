import cv2
import numpy as np 
import matplotlib.pyplot as plt 
from PIL import Image
from io import BytesIO
dirImagen="3objetos.jpg"

"""
#   1
img = cv2.imread(dirImagen)
imgrey=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Imagen grises',imgrey)
cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()

#   2
fig = plt.figure()
img = cv2.imread(dirImagen)
plt.imshow(img, animated= True)
plt.show()

#   3
img = cv2.imread(dirImagen)
hist = cv2.calcHist([img], [0], None, [256], [0, 256])
fig = plt.figure()
plt.plot(hist, color='r')
plt.show()



#4
umbral= 255 # 0 - 255
img = cv2.imread(dirImagen)
t2, imgbin2 = cv2.threshold(img, umbral, 256, cv2.THRESH_BINARY) 
cv2.imshow('Imagen binarizada 2',imgbin2)
cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()
"""
#5



imagen= cv2.imread("imagen1.jpeg")                  #Se obtiene la imagen
imgrey=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)     #Se convierte a escala de grises
t2, imgbin = cv2.threshold(imgrey, 155, 255, cv2.THRESH_BINARY)  #Se binariza 
cv2.imshow('Imagen binarizada ',imgbin)

arreglo= np.asarray(imgbin)


# 1 0    -    1 1    +    1 0
# 0 0         1 0         0 1


n1=0
n2=0
n3=0

for fil,array in enumerate(arreglo):
	for col,a in enumerate(array):
		if a==255:
			#print(a,arreglo[fil,col+1],arreglo[fil+1,col],arreglo[fil+1,col+1])
			if col < len(array) and fil < len(arreglo):
				if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
					n1+=1
				if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
					n2+=1
				if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 255:
					n3+=1

print("Numero de objetos en la imagen (4)= ",abs(n1-n2+n3))

cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()
"""
#5  (2)


imagen= cv2.imread("3palitos2.jpg")                  #Se obtiene la imagen
imgrey=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)     #Se convierte a escala de grises
t2, imgbin = cv2.threshold(imgrey, 155, 255, cv2.THRESH_BINARY_INV)  #Se binariza 
cv2.imshow('Imagen binarizada ',imgbin)

arreglo= np.asarray(imgbin)


# 1 0    -    1 1    -    0 1
# 0 0         1 0         1 0


n1=0
n2=0
n3=0

for fil,array in enumerate(arreglo):
	for col,a in enumerate(array):
		if a==255:
			#print(a,arreglo[fil,col+1],arreglo[fil+1,col],arreglo[fil+1,col+1])
			if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:
				if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
					n1+=1
				if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
					n2+=1
				if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
					n3+=1
print(n1)
print(n2)
print(n3)

print("Numero de objetos en la imagen (8)= ",abs(n1-n2-n3))

cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()



# 6 y 7
umbral=160
imagen= cv2.imread("1hueco.jpg")                  #Se obtiene la imagen
imgrey=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)     #Se convierte a escala de grises
t2, imgbin = cv2.threshold(imgrey, umbral, 255, cv2.THRESH_BINARY_INV)  #Se binariza 
cv2.imshow('Imagen binarizada ',imgbin)

arreglo= np.asarray(imgbin)


#1-    1 0    -    1 1    +    1 0
#      0 0         1 0         0 1


n1=0
n2=0
n3=0

for fil,array in enumerate(arreglo):
	for col,a in enumerate(array):
		if a==255:
			#print(a,arreglo[fil,col+1],arreglo[fil+1,col],arreglo[fil+1,col+1])
			if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:
				if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
					n1+=1
				if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
					n2+=1
				if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
					n3+=1

print(n1)
print(n2)
print(n3)

print("Numero de huecos en la imagen = ",1-(n1-n2+n3))

cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()



"""
#8

umbral=80
imagenO= cv2.imread("3objetos.jpg")                  #Se obtiene la imagen
imagen= cv2.imread("3objetos.jpg")                  #Se obtiene la imagen
imgrey=cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)     #Se convierte a escala de grises
t2, imgbin = cv2.threshold(imgrey, umbral, 255, cv2.THRESH_BINARY_INV)  #Se binariza 
arreglo = np.asarray(imagen)
arregloBin = np.asarray(imgbin)

#1-    1 0    -    1 1    +    1 0
#      0 0         1 0         0 1

n1=0
n2=0
n3=0
#print(arreglo)
#print(arregloBin)


print(type(arreglo[0][0]))
for fil,array in enumerate(arregloBin):
	for col,a in enumerate(array):
		if a==255:
			if col < len(array)-1 and col > 0 and fil < len(arregloBin)-1 and fil > 0:
				if arregloBin[fil,col+1]==0:
					arreglo[fil][col+1][0]=0
					arreglo[fil][col+1][1]=240
					arreglo[fil][col+1][2]=255
				if arregloBin[fil,col-1]==0:
					arreglo[fil][col-1][0]=0
					arreglo[fil][col-1][1]=240
					arreglo[fil][col-1][2]=255
				if arregloBin[fil+1,col]==0:
					arreglo[fil+1][col][0]=0
					arreglo[fil+1][col][1]=240
					arreglo[fil+1][col][2]=255
				if arregloBin[fil-1,col]==0:
					arreglo[fil-1][col][0]=0
					arreglo[fil-1][col][1]=240
					arreglo[fil-1][col][2]=255
				#8 Conectado 
				if arregloBin[fil+1,col+1]==0:
					arreglo[fil+1][col+1][0]=0
					arreglo[fil+1][col+1][1]=240
					arreglo[fil+1][col+1][2]=255
				if arregloBin[fil-1,col-1]==0:
					arreglo[fil-1][col-1][0]=0
					arreglo[fil-1][col-1][1]=240
					arreglo[fil-1][col-1][2]=255
				if arregloBin[fil+1,col-1]==0:
					arreglo[fil+1][col-1][0]=0
					arreglo[fil+1][col-1][1]=240
					arreglo[fil+1][col-1][2]=255
				if arregloBin[fil-1,col+1]==0:
					arreglo[fil-1][col+1][0]=0
					arreglo[fil-1][col+1][1]=240
					arreglo[fil-1][col+1][2]=255
print("Numero de huecos en la imagen = ",1-(n1-n2+n3))
edge_img = cv2.Canny(imagenO,200,200)
cv2.imshow('Imagen con bordes',edge_img)
cv2.imshow('Imagen Original ',imagenO)
cv2.imshow('Imagen Binarizada ',arregloBin)
cv2.imshow('Imagen con Contorno ',arreglo)



cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()



#9 
# 
# 
# https://mccormickml.com/2013/02/26/image-derivative/
# https://es.acervolima.com/python-deteccion-de-bordes-usando-pillow/





