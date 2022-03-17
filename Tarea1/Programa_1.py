
import numpy as np
import cv2

print("Version NumPy: " + np.__version__)
print("Version OpenCV: " + cv2.__version__)

img1=255*np.ones ((500,500),np.uint8)
for i in range(30,121):
    for j in range(30,61):
        img1[i,j]=0

for i in range(30,61):
    for j in range(10,31):
        img1[i,j]=0
    for k in range(60,81):
        img1[i,k]=0

for i in range(100,171):
    for j in range (40,61):
        img1[j,i]=0

for i in range(90,181):
    for j in range(80,101):
        img1[j,i]=0
    
for i in range(110,161):
    for j in range(100,121):
        img1[j,i]=0

for i in range(100,121):
    for j in range(60,81):
        img1[j,i]=0

for i in range(150,171):
    for j in range(60,81):
        img1[j,i]=0


cv2.imshow('imagen 1',img1)  #Mostrar imagen 
cv2.imwrite("imagen1.jpeg",img1)   #Guardar una imagen
cv2.waitKey(0)  #comando para detener la imagen
cv2.destroyAllWindows()
