from copy import deepcopy
import tkinter
from tkinter.ttk import Button, Label, Radiobutton,Spinbox, Combobox
from tkinter import StringVar, Text,IntVar
from tkinter.constants import GROOVE, W
from tkinter import filedialog as fd
from cv2 import DIST_L2, IMREAD_GRAYSCALE, MORPH_OPEN, NORM_MINMAX, dilate, distanceTransform, distanceTransformWithLabels, equalizeHist, erode, imread,cvtColor,imshow, log, morphologyEx, normalize,waitKey,destroyAllWindows,putText,calcHist,threshold,COLOR_BGR2GRAY,FONT_HERSHEY_SIMPLEX,LINE_AA,THRESH_BINARY
import cv2
import numpy as np 
import matplotlib.pyplot as plt 
import skimage
import math
import sympy
from sympy.abc import x


def interfaz():
    root = tkinter.Tk()         #Se inicia la ventana
    # Icono Aplicación
    ancho_ventana = 600         #Definir medidas de ventana
    alto_ventana = 300
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2  #Definir posición de laventana
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)    #La ventana no se puede alargar ni ensanchar

    root.title("Tarea 1 RFVC")      #Título de la ventana

    opciones = ['Agregar Ruido a imagen', 
                'Filtro espacial', 
                'Aplicar contrastado',
                'Determinar número de objetos', 
                'Aplicar operaciones morfológicas', 
                'Método de umbralado de Kapur', 
                'Histograma en escala de grises']
    opcion = IntVar()                   #Variable para guardar la opción que escoge el usuario
    opcion.set(None)
    i = 0
    e=1
    

    #Función para realizar la opción elegida por el usuario
    def realizarAccion(opcion,imagen):
        img = imread(imagen)                #Se carga la imagen a memoria

        if opcion==1:                       #Opcion 1 seleccionada en la interfaz gráfica
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            valor=float(valorRuido.get())
            titulo="Altura : " + str(h) + "       " + "Ancho: " + str(w) + "\n Tipo de Ruido:    "+ ruidoSeleccionado.get()
            titulo= titulo + "\nCantidad de ruido [0-1]:    " +  str(valor)
            plt.suptitle(titulo)
            
            if ruidoSeleccionado.get()=="Gaussiano":
                cruido = skimage.util.random_noise(img, mode="gaussian", var=valor)
            elif ruidoSeleccionado.get()=="Sal":
                cruido = skimage.util.random_noise(img, mode="salt", amount=valor)
            elif ruidoSeleccionado.get()=="Pimienta":
                cruido = skimage.util.random_noise(img, mode="pepper", amount=valor)
            elif ruidoSeleccionado.get()=="Sal y pimienta":
                cruido = skimage.util.random_noise(img, mode="s&p", amount=valor ,salt_vs_pepper=0.5)
            #plt.imsave("RuidoSyP.png",skimage.color.rgb2gray(cruido), cmap='gray')
            plt.imshow(skimage.color.rgb2gray(cruido), cmap='gray')   #Dibujar en una ventana mediante la biblioteca matplotlib
            plt.show() 
             
        if opcion==2:
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            titulo="Altura : " + str(h) + "       " + "Ancho: " + str(w) + "\n Tipo de Filtro:    "+ filtroSeleccionado.get()
            plt.suptitle(titulo)
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    
            valorKernel=int(valorFiltro.get())
            if filtroSeleccionado.get()=="Mediana":
                imFiltro= cv2.medianBlur(imgrey,valorKernel)
            if filtroSeleccionado.get()=="Gaussiano":
                imFiltro= cv2.GaussianBlur(imgrey,(valorKernel*3,valorKernel*3),0)
            if filtroSeleccionado.get()=="Promedio Aritmético":
                imFiltro= cv2.blur(imgrey,(valorKernel,valorKernel))
            imshow("Imagen sin filtro",img)   
            imshow("Imagen con filtro",imFiltro)   
            
        if opcion==3:
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            titulo="Altura : " + str(h) + "       " + "Ancho: " + str(w) + "\n Tipo de Contraste:    "+ contrasteSeleccionado.get()
            plt.suptitle(titulo)
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    

            if contrasteSeleccionado.get()=="Lineal":
                imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    
                arreglo= np.asarray(imgrey)
                #Obtener nivel máximo y mínimo de nivel de gris
                maximo=0
                minimo=255
                nuevoarreglo = deepcopy(arreglo)

                for fil,array in enumerate(nuevoarreglo):
                    for col,a in enumerate(array):
                        if a > maximo:
                            maximo = a

                for fil,array in enumerate(nuevoarreglo):
                    for col,a in enumerate(array):
                        if a < minimo:
                            minimo = a

                for fil,array in enumerate(nuevoarreglo):
                    for col,a in enumerate(array):
                        nuevoarreglo[fil,col]=int(a-minimo)*((255)/(maximo-minimo))
                        
                hist = calcHist([arreglo], [0] , None, [256], [0,256])
                hist2 = calcHist([nuevoarreglo], [0] , None, [256], [0,256])
                plt.subplot(121)
                plt.plot(hist)
                plt.subplot(122)
                plt.plot(hist2)
                imshow("Imagen Original",arreglo)
                imshow("Imagen Nueva",nuevoarreglo)
                plt.show()

            if contrasteSeleccionado.get()=="Equalizado":
                hist = calcHist([imgrey], [0] , None, [256], [0,256])
                imeq = equalizeHist(imgrey)
                histEq = calcHist([imeq], [0] , None, [256], [0,256])
                plt.subplot(121)
                plt.plot(hist)
                plt.subplot(122)
                plt.plot(histEq)
                imshow("Original", imgrey)
                imshow("Eq", imeq)
                plt.show()

        if opcion==4:
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises 
            t2, imgbin = threshold(imgrey, 128, 256, THRESH_BINARY)     #Convertir imagen a binaria 
            kernel = np.ones((7,7), np.uint8)
            dist = distanceTransform(imgbin, DIST_L2 , 3)
            normalize(dist, dist, 0, 1.0, NORM_MINMAX)
            t2, imgbin2 = threshold(dist, float(umbralSel.get())/256, 1, THRESH_BINARY)     #Convertir imagen a binaria
            imshow("Transformada Distancia", dist)
            imshow("Imagen Original", imgbin)
            imshow("Imagen A analizar", imgbin2)
            contarObjetos(imgbin2)

        if opcion==5:
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises 
            tamKer = int(kerSel.get())
            kernel = np.ones((tamKer,tamKer), np.uint8)
            if opSeleccionado.get()=="Filtrados":
                iteraciones = int(iterSel.get())
                erosion = erode(imgrey,kernel,iterations=iteraciones)
                dilatacion = dilate(erosion,kernel,iterations=iteraciones)
                dilatacion = dilate(dilatacion,kernel,iterations=iteraciones)
                erosion = erode(dilatacion,kernel,iterations=iteraciones)
                imshow("Original",img)
                imshow("Filtrada",erosion)
            if opSeleccionado.get()=="Detección de contornos":
                umbral = int(umbralSel.get())
                t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     #Convertir imagen a binaria 
                erosion = erode(imgbin,kernel,iterations=1)
                resta = cv2.subtract(imgbin,erosion)
                imshow("Original",imgbin)
                imshow("Restada",resta)
            if opSeleccionado.get()=="Conteo de objetos":
                umbral = int(umbralSel.get())
                t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     #Convertir imagen a binaria 
                numIteraciones = int(iterSel.get())
                erosion = erode(imgbin,kernel,iterations=numIteraciones)
                dilatacion = dilate(erosion,kernel,iterations=numIteraciones)
                contarObjetos(dilatacion)
                imshow("Erosion", erosion)
                imshow("Dilatacion", dilatacion)

        if opcion==7:   
            imgrey=imread(imagen, IMREAD_GRAYSCALE)       
            plt.hist(imgrey.ravel(),256,[0,256])
            plt.show()

        if opcion==6:
            img = imread(imagen,0)
            imgrey=imread(imagen, IMREAD_GRAYSCALE)    #Convertir imagen de formato RGB a Escala de Grises    
            hist = calcHist([img], [0] , None, [256], [0,256])
            
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            Nt=h*w                                  #Número total de pixelse
            Ht=[]
            for Pr in hist: 
                    Ht.append(float(Pr)/Nt)                    #Histograma normalizado por nivel de gris
            hc1= []
            hc2= []
            hc1.append(Ht[0])
            hc2.append(1-Ht[0])
            for i,a in enumerate(Ht[1:]):
                    hc1.append(hc1[i-1]+Ht[i])
                    hc2.append(1-hc1[i])
            umbral=0
            entropiaTotal = 0
            maxEntropia = 0
            for i,P in enumerate(hist):
                entropiaFondo = 0
                entropiaObjeto = 0
                for u in range(i):
                    if float(hist[u])!=0 and hc1[i]!=0:
                        A=log(Ht[u]/hc1[i])
                        entropiaFondo -= ((Ht[u]/hc1[i]) * A[0])
                for u in range(i+1,256):
                    if float(hist[u])!=0 and hc2[i]!=0:
                        #print("a",Ht[u]/hc2[i])
                        B=log(Ht[u]/hc2[i])
                        entropiaObjeto -= ((Ht[u]/hc2[i]) * B[0])

                entropiaTotal = entropiaFondo + entropiaObjeto
                if maxEntropia < entropiaTotal:
                    maxEntropia = entropiaTotal
                    umbral = i
            print()
            print(umbral)
            t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     #Convertir imagen a binaria 
            imshow("Kapur",imgbin)
            titulo="Umbral seleccionado por método Kapur: " + str(umbral) 
            fig, ax = plt.subplots()
            maximo = int(max(hist))
            ax.plot([x*umbral for x in np.ones(maximo)],np.arange(maximo))
            plt.title(titulo)
            plt.hist(imgrey.ravel(),256,[0,256])
            plt.show()

        waitKey(0)  #comando para detener la imagen
        destroyAllWindows()

    def contarObjetos(imagen):
        arreglo= np.asarray(imagen)             #Convertir la información de la imagen en un arreglo numpy
        n1=0
        n2=0
        n3=0
        #Se recorre la imagen para buscar las máscaras
        #    |1 0|       |1 1|       |1 0|
        #    |0 0|       |1 0|       |0 1|
        for fil,array in enumerate(arreglo):
            for col,a in enumerate(array):
                if a!= 0.0:
                    if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1: #Evitar buscar máscaras en los bordes
                        if arreglo[fil,col+1] == 0.0   and arreglo[fil+1,col] == 0.0   and arreglo[fil+1,col+1] == 0.0:
                            n1+=1                       #Contar mascara 1
                        if arreglo[fil,col+1] != 0.0 and arreglo[fil+1,col] != 0.0 and arreglo[fil+1,col+1] == 0.0:
                            n2+=1                       #Contar mascara 2
                        if arreglo[fil,col+1] == 0.0   and arreglo[fil+1,col] == 0.0   and arreglo[fil+1,col+1] != 0.0:
                            n3+=1                       #Contar mascara 3
        print(abs(n1-n2+n3))
        text="Numero de objetos en la imagen = " + str(abs(n1-n2+n3))           #Texto sobre la información de la imagen

    """
    #Función para realizar la opción elegida por el usuario
    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==1:                       #Opcion 1 seleccionada en la interfaz gráfica
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            text="Altura : "+str(h)+" , Ancho: "+str(w)      #Texto sobre la información de la imagen
            composite_img = putText(img, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2, LINE_AA, False)    #Agregar características de la imagen como texto
            plt.imshow(img_2, animated= True)   #Dibujar en una ventana mediante la biblioteca matplotlib
            plt.show()    


        if opcion==2:                           #Opcion 2 seleccionada en la interfaz gráfica
            img_2 = img[:,:,[2,1,0]]            #Tomar todos los canales (R,G,B) de la imagen
            plt.imshow(img_2, animated= True)   #Dibujar en una ventana mediante la biblioteca matplotlib
            plt.show()                          #Mostrar la nueva ventana con matplotlib

        if opcion==3:
            fig,axes=plt.subplots(nrows=1, ncols=1) #Definir el plano en el que se graficará con mathplotlib
            color = ('b','g','r')
            for i,col in enumerate(color):      #Crear un histograma por cada color (R,G,B)
                histr = calcHist([imagen],[i],None,[256],[0,256]) #Calcular el histograma de la imagen según el color
                plt.plot(histr,color = col)     #Dibujar el histograma en el plano asignado
                plt.xlim([0,256])               #Definir el límite en el eje x del plano
            imshow("Imagen Original",img)           #Mostra la imagen en una nueva ventana
            plt.show()                              #Mostrar el histograma en una ventana con matplotlib
            
            

        if opcion==4:           #Opcion 4 seleccionada en la interfaz gráfica
            umbral= int(umbralSel.get())            #Obtener umbral que seleccionó el usuario
            t2, imgbin = threshold(img, umbral, 256, THRESH_BINARY)     #Convertir imagen a binaria con el umbral seleccionado
            imshow('Imagen binarizada',imgbin)      #Mostrar imagen en una ventana nueva

        if opcion==5:                               #Opcion 5 seleccionada en la interfaz gráfica
            umbral= int(umbralSel.get())            #Obtener umbral que seleccionó el usuario
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza la imagen     
            arreglo= np.asarray(imgbin)             #Convertir la información de la imagen en un arreglo numpy
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            n1=0
            n2=0
            n3=0
            Se recorre la imagen para buscar las máscaras
                |1 0|       |1 1|       |1 0|
                |0 0|       |1 0|       |0 1|
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1: #Evitar buscar máscaras en los bordes
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1                       #Contar mascara 1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1                       #Contar mascara 2
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1                       #Contar mascara 3
            text="Numero de objetos en la imagen = " + str(abs(n1-n2+n3))           #Texto sobre la información de la imagen
            composite_img = putText(imgbin, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.4, (255, 255, 255), 1, LINE_AA, False)                        #Agregar el número de objetos de la imagen como texto
            imshow('Imagen binarizada ',composite_img)      #Mostrar imagen en una nueva ventana

        if opcion==6:
            umbral=int(umbralSel.get())             #Obtener umbral que seleccionó el usuario
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza la imagen
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            arreglo= np.asarray(imgbin)             #Convertir la información de la imagen en un arreglo numpy
            n1=0
            n2=0
            n3=0
            Se recorre la imagen para buscar las máscaras
                |1 0|       |1 1|       |1 0|
                |0 0|       |1 0|       |0 1|
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:     #Evitar buscar máscaras en los bordes
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1                   #Contar mascara 1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1                   #Contar mascara 2
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1                   #Contar mascara 3
            text="Numero de huecos en la imagen = " + str(abs(1-(n1-n2+n3)))           #Texto sobre la información de la imagen
            composite_img = putText(imgbin, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.25, (0, 0, 0), 1, LINE_AA, False)                         #Agregar el número de objetos de la imagen como texto                                
            imshow('Imagen binarizada ',composite_img)                      #Mostrar imagen en una nueva ventana

        if opcion==7:                               #Opcion 7 seleccionada en la interfaz gráfica
            umbral=int(umbralSel.get())             #Obtener umbral que seleccionó el usuario
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza la imagen
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles  
            arreglo= np.asarray(imgbin)             #Convertir la información de la imagen a un arreglo numpy
            n1=0
            n2=0
            n3=0
            Se recorre la imagen para buscar las máscaras
                |1 0|       |1 1|       |1 0|
                |0 0|       |1 0|       |0 1|
            
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1: #Evitar buscar máscaras en los bordes
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1               #Contar mascara 1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1               #Contar mascara 2
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1               #Contar mascara 3
            if 1-(n1-n2+n3)!=0:
                text="La imagen es simplemente conectada"            #Texto sobre la información de la imagen
            else:
                text="La imagen es multiplemente conectada"        #Texto sobre la información de la imagen
            composite_img = putText(imgbin, text, ( 0 , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.3, (255,255,255), 1, LINE_AA, False)                      #Agregar el número de objetos de la imagen como texto                                
            imshow('Imagen binarizada ',composite_img)                      #Mostrar imagen en una nueva ventana



        if opcion==8:                               #Opcion 7 seleccionada en la interfaz gráfica
            umbral=int(umbralSel.get())             #Obtener umbral que seleccionó el usuario
            imagenO= imread(imagen)                 #Se obtiene la imagen para mostrarla en una ventana
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza la imagen
            arreglo = np.asarray(img)               #Convertir la información de la imagen Original a un arreglo numpy
            arregloBin = np.asarray(imgbin)         #Convertir la información de la imagen Binarizada a un arreglo numpy
            n1=0
            n2=0
            n3=0
            #Buscar los pixeles que forman parte del objeto 
            for fil,array in enumerate(arregloBin):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and col > 0 and fil < len(arregloBin)-1 and fil > 0: #Evitar buscar fuera de los bordes
                            #Buscar si en la 4-vecindad hay algún bit que forme parte del fondo de la imagen  
                            if arregloBin[fil,col+1]==0 or arregloBin[fil,col-1]==0 or arregloBin[fil+1,col]==0 or arregloBin[fil-1,col]==0:    
                                #Cambiar el color del pixel en la imagen original
                                arreglo[fil][col][0]=0
                                arreglo[fil][col][1]=240
                                arreglo[fil][col][2]=255
                            #Buscar si en la 8-vecindad hay algún bit que forme parte del fondo de la imagen  
                            elif arregloBin[fil+1,col+1]==0 or arregloBin[fil+1,col-1]==0 or arregloBin[fil-1,col+1]==0 or arregloBin[fil-1,col-1]==0:   
                                #Cambiar el color del pixel en la imagen original
                                arreglo[fil][col][0]=0
                                arreglo[fil][col][1]=240
                                arreglo[fil][col][2]=255

            imshow('Imagen Original ',imagenO)      #Mostrar imagen original en una nueva ventana
            imshow('Imagen con Contorno ',arreglo)  #Mostrar imagen con contorno en una nueva ventana

        waitKey(0)  #comando para detener la imagen
        destroyAllWindows()
    """

    #Función para seleccionar archivo de imagen
    def select_file():
        filetypes = (
            ('All files', '*.*'),
            ('JPG', '*.jpg'),
            ('PNG', '*.jpg'),
            ('JPEG', '*.jpeg')
        )
        #Ventana 'Seleccion de archivo'
        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='',
            filetypes=filetypes )
        #Después de seleccionar la imagen se manda llamar la función
        realizarAccion(opcion.get(),filename)


    #Definición y posicionamiento de los elementos de la interfaz gráfica

    Label(root, text="Selecciona una opción a realizar").grid(row=i, column=0, sticky=W, padx=15, pady=5)
    
    Button(root, text="Seleccionar archivo", command=select_file).grid(row=1, column=2, columnspan=2,padx=15, pady=5)   
    umbralSel=Spinbox(root,width=3,from_=0,to=255,increment=1)
    umbraltxt=Label(root,text="Umbral")
    
    tipoRuido=["Gaussiano","Sal","Pimienta","Sal y pimienta"]
    ruidoSeleccionado= StringVar()
    lblRuido=Label(root,text="Ruido")
    lblRuido2=Label(root,text="Porcentaje Ruido")
    cbbRuido=Combobox(root,textvariable=ruidoSeleccionado)
    cbbRuido['values']=tipoRuido
    valorRuido=Spinbox(root,width=4,from_=0,to=1,increment=0.01)


    tipoFiltro=["Promedio Aritmético","Mediana","Gaussiano"]
    filtroSeleccionado= StringVar()
    lblFiltro=Label(root,text="Tipo Filtro")
    cbbFiltro=Combobox(root,textvariable=filtroSeleccionado)
    cbbFiltro['values']=tipoFiltro
    lblFiltro2=Label(root,text="Tamaño Matriz")
    valorFiltro=Spinbox(root,width=2,from_=1,to=9,increment=1)
    
    tipoContraste=["Lineal","Equalizado"]
    contrasteSeleccionado= StringVar()
    lblContraste=Label(root,text="Tipo Filtro")
    cbbContraste=Combobox(root,textvariable=contrasteSeleccionado)
    cbbContraste['values']=tipoContraste

    def mostrarCombobox(event):
        umbralSel.grid_forget()
        umbraltxt.grid_forget()
        iterSel.grid_forget()
        itertxt.grid_forget()
        kerSel.grid_forget()
        kertxt.grid_forget()
        if opSeleccionado.get()=="Filtrados" or opSeleccionado.get()=="Conteo de objetos":
            umbralSel.grid(row=3, column=3, padx=15, pady=5)
            umbraltxt.grid(row=3, column=2, padx=15, pady=5)
            iterSel.grid(row=4, column=3, padx=15, pady=5)
            itertxt.grid(row=4, column=2, padx=15, pady=5)
            kerSel.grid(row=5, column=3, padx=15, pady=5)
            kertxt.grid(row=5, column=2, padx=15, pady=5)
        if opSeleccionado.get()=="Detección de contornos":
            umbralSel.grid(row=3, column=3, padx=15, pady=5)
            umbraltxt.grid(row=3, column=2, padx=15, pady=5)
            kerSel.grid(row=4, column=3, padx=15, pady=5)
            kertxt.grid(row=4, column=2, padx=15, pady=5)

    opMorf=["Filtrados","Detección de contornos","Conteo de objetos"]
    opSeleccionado= StringVar()
    lblOpM=Label(root,text="Tipo Filtro")
    cbbOpM=Combobox(root,textvariable=opSeleccionado)
    cbbOpM['values']=opMorf
    cbbOpM.bind("<<ComboboxSelected>>",mostrarCombobox)

    iterSel=Spinbox(root,width=3,from_=0,to=100,increment=1)
    itertxt=Label(root,text="Iteraciones")
    
    kerSel=Spinbox(root,width=3,from_=0,to=100,increment=1)
    kertxt=Label(root,text="Tamaño Kernel")

    def mostrarOpciones():
        umbralSel.grid_forget()
        umbraltxt.grid_forget()

        lblRuido.grid_forget()
        cbbRuido.grid_forget()
        lblRuido2.grid_forget()
        valorRuido.grid_forget()

        lblFiltro.grid_forget()
        cbbFiltro.grid_forget()
        lblFiltro2.grid_forget()
        valorFiltro.grid_forget()

        lblContraste.grid_forget()
        cbbContraste.grid_forget()

        lblOpM.grid_forget()
        cbbOpM.grid_forget()

        iterSel.grid_forget()
        itertxt.grid_forget()
        kerSel.grid_forget()
        kertxt.grid_forget()

        if opcion.get()==1:
            lblRuido.grid(row=2, column=2, padx=15, pady=5)
            cbbRuido.grid(row=2, column=3, padx=15, pady=5)
            lblRuido2.grid(row=3, column=2, padx=15, pady=5)
            valorRuido.grid(row=3, column=3, padx=15, pady=5)
            
        if opcion.get()==2:
            lblFiltro.grid(row=2, column=2, padx=15, pady=5)
            cbbFiltro.grid(row=2, column=3, padx=15, pady=5)
            lblFiltro2.grid(row=3, column=2, padx=15, pady=5)
            valorFiltro.grid(row=3, column=3, padx=15, pady=5)

        if opcion.get()==3:
            lblContraste.grid(row=2, column=2, padx=15, pady=5)
            cbbContraste.grid(row=2, column=3, padx=15, pady=5)

        if  opcion.get()==4:
            umbraltxt.grid(row=2, column=2, padx=15, pady=5)
            umbralSel.grid(row=2, column=3, padx=15, pady=5)
        
        if  opcion.get()==5:
            lblOpM.grid(row=2, column=2, padx=15, pady=5)
            cbbOpM.grid(row=2, column=3, padx=15, pady=5)

            

    for i, op in enumerate(opciones):
        Radiobutton(root, text=op, variable=opcion, value=i+1, command=mostrarOpciones).grid(row=i+e, sticky=W, padx=15, pady=5)         

    labelDatos=Label(root)
    monitorDatos = Text(root, height=8, width=60, relief=GROOVE)
    
    root.mainloop()


if __name__ == "__main__":
    interfaz()