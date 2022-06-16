from copy import deepcopy
import tkinter
from tkinter.ttk import Button, Label, Radiobutton,Spinbox, Combobox
from tkinter import StringVar, Text,IntVar
from tkinter.constants import GROOVE, W
from tkinter import filedialog as fd
from turtle import st
from cv2 import DIST_L2, IMREAD_GRAYSCALE, NORM_MINMAX, dilate, distanceTransform, equalizeHist, erode, imread,cvtColor,imshow, log, normalize,waitKey,destroyAllWindows,calcHist,threshold,COLOR_BGR2GRAY,THRESH_BINARY
import cv2
import numpy as np 
import matplotlib.pyplot as plt 
import skimage
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

    root.title("Tarea 2 RFVC")      #Título de la ventana

    opciones = ['Agregar Ruido a imagen', 
                'Filtro espacial', 
                'Aplicar contrastado',
                'Determinar número de objetos', 
                'Aplicar operaciones morfológicas', 
                'Método de umbralado de Kapur', 
                'Método de umbralado de Cheng']
    opcion = IntVar()                   #Variable para guardar la opción que escoge el usuario
    opcion.set(None)
    

    #Función para realizar la opción elegida por el usuario
    def realizarAccion(opcion,imagen):
        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==1:                       #Opcion 1 seleccionada en la interfaz gráfica
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            valor=float(valorRuido.get())           #Valor de ruido a aplicar
            if ruidoSeleccionado.get()=="Gaussiano":                #Opcion Ruido Gaussiano
                cruido = skimage.util.random_noise(img, mode="gaussian", var=valor)
            elif ruidoSeleccionado.get()=="Sal":                    #Opcion Ruido Tipo Sal
                cruido = skimage.util.random_noise(img, mode="salt", amount=valor)
            elif ruidoSeleccionado.get()=="Pimienta":               #Opcion Ruido Tipo Pimienta
                cruido = skimage.util.random_noise(img, mode="pepper", amount=valor)
            elif ruidoSeleccionado.get()=="Sal y pimienta":         #Opcion Ruido Tipo Sal y Pimienta
                cruido = skimage.util.random_noise(img, mode="s&p", amount=valor ,salt_vs_pepper=0.5)
            #plt.imsave("ImagenConRuido.png",skimage.color.rgb2gray(cruido), cmap='gray') #Guardar imagen con Ruido
            fig = plt.figure()
            fig.tight_layout()
            ax1= fig.add_subplot(1,2,1)             
            ax2= fig.add_subplot(1,2,2)
            titulo="Altura : " + str(h) + "       " + "Ancho: " + str(w) + "\n Tipo de Ruido:    "+ ruidoSeleccionado.get()
            titulo= titulo + "\nCantidad de ruido [0-1]:    " +  str(valor)
            fig.suptitle(titulo)                                      #Título
            ax1.imshow(skimage.color.rgb2gray(img), cmap='gray')      #Dibujar imagen seleccionada
            ax1.set_title("Imagen Seleccionada")
            ax2.imshow(skimage.color.rgb2gray(cruido), cmap='gray')   #Dibujar imagen con ruido
            ax2.set_title("Imagen con Ruido")
            fig.show()

        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==2:                       #Opcion 2 seleccionada en la interfaz gráfica
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    
            valorKernel=int(valorFiltro.get())      #Obtener tamño de kernel
            if filtroSeleccionado.get()=="Mediana":         #Opcion Filtro Tipo Mediana
                imFiltro= cv2.medianBlur(imgrey,valorKernel)
            if filtroSeleccionado.get()=="Gaussiano":       #Opcion Filtro Gaussiano
                imFiltro= cv2.GaussianBlur(imgrey,(valorKernel*3,valorKernel*3),0)
            if filtroSeleccionado.get()=="Promedio Aritmético":         #Opcion Filtro Tipo Promedio Aritmético
                imFiltro= cv2.blur(imgrey,(valorKernel,valorKernel))
            fig = plt.figure()
            fig.tight_layout()
            ax1= fig.add_subplot(1,2,1)             
            ax2= fig.add_subplot(1,2,2)
            titulo="Altura : " + str(h) + "       " + "Ancho: " + str(w) + "\n Tipo de Filtro:    "+ filtroSeleccionado.get()
            titulo= titulo + "\nTamaño Matriz Kernel:    " +  str(valorKernel)
            fig.suptitle(titulo)                                      #Título
            ax1.imshow(imgrey, cmap='gray')            #Dibujar imagen seleccionada
            ax1.set_title("Imagen Seleccionada")
            ax2.imshow(imFiltro, cmap='gray')       #Dibujar imagen con filtro aplicado
            ax2.set_title("Imagen con Ruido")
            fig.show()
        
        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==3:                       #Opcion 3 seleccionada en la interfaz gráfica
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    
            if contrasteSeleccionado.get()=="Lineal":
                imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    
                arreglo= np.asarray(imgrey)
                #Obtener nivel máximo y mínimo de nivel de gris
                maximo=0
                minimo=255
                nuevo = deepcopy(arreglo)

                for fil,array in enumerate(nuevo):
                    for col,a in enumerate(array):
                        if a > maximo:
                            maximo = a

                for fil,array in enumerate(nuevo):
                    for col,a in enumerate(array):
                        if a < minimo:
                            minimo = a
                #Ajustar los valores del histograma para realizar un contraste lineal
                for fil,array in enumerate(nuevo):
                    for col,a in enumerate(array):
                        nuevo[fil,col]=int(a-minimo)*((255)/(maximo-minimo))

            if contrasteSeleccionado.get()=="Equalizado":
                nuevo = equalizeHist(imgrey)     #Funcion para equalizar el histograma
            
            hist = calcHist([imgrey], [0] , None, [256], [0,256]) #Calcular histograma de imagen seleccionada
            hist2 = calcHist([nuevo], [0] , None, [256], [0,256])   #Calcular histograma de imagen contrastada

            fig, axs = plt.subplots(2)
            fig.tight_layout()
            ax1= axs[0]
            ax2= axs[1]
            titulo="Tipo de Contraste: "+ contrasteSeleccionado.get()
            fig.suptitle(titulo)                                      #Título
            ax1.plot(hist)                               #Dibujar histograma imagen seleccionada
            ax1.set_title("Histograma Imagen Seleccionada")
            ax2.plot(hist2)                              #Dibujar histograma imagen contrastada
            ax2.set_title("Histograma Imagen Contrastada")
            fig.show()
            imshow("Imagen Original",imgrey)
            imshow("Imagen Contrastada",nuevo)

        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==4:                        #Opcion 4 seleccionada en la interfaz gráfica
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises 
            t2, imgbin = threshold(imgrey, 128, 256, THRESH_BINARY)     #Convertir imagen a binaria 
            dist = distanceTransform(imgbin, DIST_L2 , 3)       #Función cálculo de la transformada distancia
            normalize(dist, dist, 0, 1.0, NORM_MINMAX)          #Normalizar la imagen resultante
            t2, imgbin2 = threshold(dist, float(umbralSel.get())/256, 1, THRESH_BINARY)     #Convertir imagen a binaria con el umbral seleccionado
            numObjetos = contarObjetos(imgbin2)                 #Contar objetos usando el método basado en vecindades

            fig, axs = plt.subplots(1,3)
            fig.tight_layout()
            ax1= axs[0]
            ax2= axs[1]
            ax3= axs[2]
            titulo="Objetos contados: " + str(numObjetos) + "\nUmbral: " + str(umbralSel.get())
            fig.suptitle(titulo)                                      #Título
            ax1.imshow(imgbin, cmap='gray')                      #Dibujar imagen seleccionada
            ax1.set_title("Imagen Seleccionada")
            ax2.imshow(dist, cmap='gray')                        #Dibujar imagen con el cálculo transformada distancia
            ax2.set_title("Calculo Transformada Distancia")
            ax3.imshow(imgbin2, cmap='gray')                     #Dibujar imagen umbralizada para analizar núm objetos
            ax3.set_title("Imagen Umbralizada para analizar")
            fig.show()

        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==5:                       #Opcion 5 seleccionada en la interfaz gráfica
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises 
            tamKer = int(kerSel.get())              
            kernel = np.ones((tamKer,tamKer), np.uint8)     #Crear el kernel según el tamaño seleccionado
            if opSeleccionado.get()=="Filtrados":                    #Opcion Filtro
                iteraciones = int(iterSel.get())
                erosion = erode(imgrey,kernel,iterations=iteraciones)               #Erosionar y dilatar para eliminar ruido
                convertida = dilate(erosion,kernel,iterations=iteraciones)
                titulo = "Filtrado de imagen \n Iteraciones: "+ str(iteraciones) + "\n Tamaño de Kernel:  Matriz de " + str(tamKer) + "*" + str(tamKer)
            if opSeleccionado.get()=="Detección de contornos":       #Opcion Detección de contornos
                umbral = int(umbralSel.get())
                t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     #Convertir imagen a binaria 
                erosion = erode(imgbin,kernel,iterations=1)             #Erosionar 
                convertida = cv2.subtract(imgbin,erosion)          #Restar la imagen original a la erosionada para detectar contorno
                titulo = "Detección de contornos +\n Umbral: " +str(umbral) + "\n Tamaño de Kernel:  Matriz de " + str(tamKer) + "*" + str(tamKer)
            if opSeleccionado.get()=="Conteo de objetos":               #Opcion Conteo de objetoss
                umbral = int(umbralSel.get())
                t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     #Convertir imagen a binaria 
                iteraciones = int(iterSel.get())
                erosion = erode(imgbin,kernel,iterations=iteraciones)                #Erosionar la imagen para separar uniones en caso de que haya
                convertida = dilate(erosion,kernel,iterations=int(iteraciones/2))    #Dilatar para crear separaciones en un solo objeto
                numObjetos=contarObjetos(convertida)                                    #Contar objetos usando el método basado en vecindades
                titulo = "Conteo de objetos+\nIteraciones: "+str(iteraciones)+"\nTam Kernel:"+str(tamKer)+" \n Objetos Contados: " + str(numObjetos)

            fig, axs = plt.subplots(2)
            ax1 = axs[0]
            ax2 = axs[1]
            fig.tight_layout()
            fig.suptitle(titulo)                                      #Título
            ax1.imshow(imgrey, cmap='gray')            #Dibujar imagen seleccionada
            ax1.set_title("Imagen Seleccionada")
            ax2.imshow(convertida, cmap='gray')       #Dibujar imagen con operaciones aplicadas
            ax2.set_title("Imagen Resultante")
            fig.show()

        img = imread(imagen,0)                #Se carga la imagen a memoria
        if opcion==6:                       #Opcion 6 seleccionada en la interfaz gráfica
            imgrey=imread(imagen, IMREAD_GRAYSCALE)    #Convertir imagen de formato RGB a Escala de Grises    
            hist = calcHist([img], [0] , None, [256], [0,256])  #Calcular histograma en escala de grises
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
            for i,a in enumerate(Ht[1:]):                   #Se calculan las entropias para cada nivel de umbral posible
                    hc1.append(hc1[i-1]+Ht[i])
                    hc2.append(1-hc1[i])
            umbral=0
            entropiaTotal = 0
            maxEntropia = 0
            for i,P in enumerate(hist):                 #Se encuentra en que umbral la entropía tiene su valor máximo
                entropiaFondo = 0
                entropiaObjeto = 0
                for u in range(i):                              #Se calcula la entropia de ambas clases, objeto y fondo
                    if float(hist[u])!=0 and hc1[i]!=0:         # se suman para encontrar la entropía total y
                        A=log(Ht[u]/hc1[i])                     # definir en qué umbral la entropía es mayor
                        entropiaFondo -= ((Ht[u]/hc1[i]) * A[0])
                for u in range(i+1,256):
                    if float(hist[u])!=0 and hc2[i]!=0:         #No se toman los valores donde el histograma no tenga incidencias
                        #print("a",Ht[u]/hc2[i])
                        B=log(Ht[u]/hc2[i])
                        entropiaObjeto -= ((Ht[u]/hc2[i]) * B[0])

                entropiaTotal = entropiaFondo + entropiaObjeto
                if maxEntropia < entropiaTotal:
                    maxEntropia = entropiaTotal
                    umbral = i
                            #Convertir imagen a binaria según el umbral encontrado
            t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     
            maximo = int(max(hist))                                         
            fig, axs = plt.subplots(1,3)
            fig.tight_layout()
            ax1= axs[0]
            ax2= axs[1]
            ax3= axs[2]
            titulo="Umbral seleccionado por método Kapur: " + str(umbral) 
            fig.suptitle(titulo)                                      #Título
            ax1.imshow(imgrey, cmap='gray')            #Dibujar imagen seleccionada
            ax1.set_title("Imagen original")
            ax2.imshow(imgbin, cmap='gray')            #Dibujar imagen binarizada con el umbral encontrado
            ax2.set_title("Método Kapur")
            ax3.plot([x*umbral for x in np.ones(maximo)],np.arange(maximo))     #Se dibuja el umbral encontrado
            ax3.hist(imgrey.ravel(),256,[0,256])       #Dibujar histograma de la imagen en escala de grises
            ax3.set_title("Histograma con umbral")
            fig.show()

        img = imread(imagen,0)                #Se carga la imagen a memoria
        if opcion ==7:
            imgrey=imread(imagen, IMREAD_GRAYSCALE)    #Convertir imagen de formato RGB a Escala de Grises    
            hist = calcHist([img], [0] , None, [256], [0,256])  #Calcular histograma en escala de grises
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            Nt=h*w                                  #Número total de pixelse
            Ht=[]
            for Pr in hist: 
                    Ht.append(float(Pr)/Nt)   
            hc1= []
            hc2= []
            hc1.append(Ht[0])
            hc2.append(1-Ht[0])
            for i,a in enumerate(Ht[1:]):                   #Se calculan las distribuciones de probabilidad para 
                    hc1.append(hc1[i-1]+Ht[i])              # cada nivel de umbral posible
                    hc2.append(1-hc1[i])
            umbral=0
            entropiaTotal = 0
            maxEntropia = 0
            for i,P in enumerate(hist):                 #Se encuentra en que umbral la correlación tiene su valor máximo
                entropiaFondo = 0
                entropiaObjeto = 0
                for u in range(i):                              #Se calcula la correlación de ambas clases, objeto y fondo
                    if float(hist[u])!=0 and hc1[i]!=0:         # se suman para encontrar la correlación total y
                        A=pow(hist[u]/hc1[i],2)                     # definir en qué umbral la correlación es mayor
                        entropiaFondo -= log(A)[0]
                for u in range(i+1,256):
                    if float(hist[u])!=0 and hc2[i]!=0:         #No se toman los valores donde el histograma 
                        #print("a",Ht[u]/hc2[i])                # no tenga incidencias
                        B=pow(hist[u]/hc2[i],2)                     # definir en qué umbral la correlación es mayor
                        entropiaObjeto -= log(B)[0]
                
                entropiaTotal = entropiaFondo + entropiaObjeto
                if maxEntropia > entropiaTotal:
                    maxEntropia = entropiaTotal
                    umbral = i
                            #Convertir imagen a binaria según el umbral encontrado
            t2, imgbin = threshold(imgrey, umbral, 256, THRESH_BINARY)     
            maximo = int(max(hist))                                         
            fig, axs = plt.subplots(1,3)
            fig.tight_layout()
            ax1= axs[0]
            ax2= axs[1]
            ax3= axs[2]
            titulo="Umbral seleccionado por método Cheng: " + str(umbral) 
            fig.suptitle(titulo)                                      #Título
            ax1.imshow(imgrey, cmap='gray')            #Dibujar imagen seleccionada
            ax1.set_title("Imagen original")
            ax2.imshow(imgbin, cmap='gray')            #Dibujar imagen binarizada con el umbral encontrado
            ax2.set_title("Método Cheng")
            ax3.plot([x*umbral for x in np.ones(maximo)],np.arange(maximo))     #Se dibuja el umbral encontrado
            ax3.hist(imgrey.ravel(),256,[0,256])       #Dibujar histograma de la imagen en escala de grises
            ax3.set_title("Histograma con umbral")
            fig.show()
        if opcion==8:   
            imgrey=imread(imagen, IMREAD_GRAYSCALE)       
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
        return abs(n1-n2+n3)

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

    i=0

    Label(root, text="Selecciona una opción a realizar").grid(row=i, column=0, sticky=W, padx=15, pady=5)
    
    Button(root, text="Seleccionar archivo", command=select_file).grid(row=1, column=2, columnspan=2,padx=15, pady=5)   
    umbralSel=Spinbox(root,width=3,from_=0,to=255,increment=1)
    umbraltxt=Label(root,text="Umbral")
    
    #Elementos Opcion 1
    tipoRuido=["Gaussiano","Sal","Pimienta","Sal y pimienta"]
    ruidoSeleccionado= StringVar()
    lblRuido=Label(root,text="Ruido")
    lblRuido2=Label(root,text="Porcentaje Ruido")
    cbbRuido=Combobox(root,textvariable=ruidoSeleccionado)
    cbbRuido['values']=tipoRuido
    valorRuido=Spinbox(root,width=4,from_=0,to=1,increment=0.01)

    #Elementos Opcion 2
    tipoFiltro=["Promedio Aritmético","Mediana","Gaussiano"]
    filtroSeleccionado= StringVar()
    lblFiltro=Label(root,text="Tipo Filtro")
    cbbFiltro=Combobox(root,textvariable=filtroSeleccionado)
    cbbFiltro['values']=tipoFiltro
    lblFiltro2=Label(root,text="Tamaño Matriz")
    valorFiltro=Spinbox(root,width=2,from_=1,to=9,increment=1)
    
    #Elementos Opcion 3
    tipoContraste=["Lineal","Equalizado"]
    contrasteSeleccionado= StringVar()
    lblContraste=Label(root,text="Tipo Filtro")
    cbbContraste=Combobox(root,textvariable=contrasteSeleccionado)
    cbbContraste['values']=tipoContraste

    #Combobox
    def mostrarCombobox(event):
        umbralSel.grid_forget()
        umbraltxt.grid_forget()
        iterSel.grid_forget()
        itertxt.grid_forget()
        kerSel.grid_forget()
        kertxt.grid_forget()
        if opSeleccionado.get()=="Filtrados":
            iterSel.grid(row=3, column=3, padx=15, pady=5)
            itertxt.grid(row=3, column=2, padx=15, pady=5)
            kerSel.grid(row=4, column=3, padx=15, pady=5)
            kertxt.grid(row=4, column=2, padx=15, pady=5)
        elif opSeleccionado.get()=="Detección de contornos":
            umbralSel.grid(row=3, column=3, padx=15, pady=5)
            umbraltxt.grid(row=3, column=2, padx=15, pady=5)
            kerSel.grid(row=4, column=3, padx=15, pady=5)
            kertxt.grid(row=4, column=2, padx=15, pady=5)
        else:
            umbralSel.grid(row=3, column=3, padx=15, pady=5)
            umbraltxt.grid(row=3, column=2, padx=15, pady=5)
            iterSel.grid(row=4, column=3, padx=15, pady=5)
            itertxt.grid(row=4, column=2, padx=15, pady=5)
            kerSel.grid(row=5, column=3, padx=15, pady=5)
            kertxt.grid(row=5, column=2, padx=15, pady=5)

    #Elementos Opcion 5
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

    e=1
    for i, op in enumerate(opciones):
        Radiobutton(root, text=op, variable=opcion, value=i+1, command=mostrarOpciones).grid(row=i+e, sticky=W, padx=15, pady=5)         

    root.mainloop()


if __name__ == "__main__":
    interfaz()