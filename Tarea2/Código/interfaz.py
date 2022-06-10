import tkinter
from tkinter.ttk import Button, Label, Radiobutton,Spinbox, Combobox
from tkinter import Image, StringVar, Text,IntVar
from tkinter.constants import GROOVE, W
from tkinter import filedialog as fd
from cv2 import equalizeHist, imread,cvtColor,imshow,waitKey,destroyAllWindows,putText,calcHist,threshold,COLOR_BGR2GRAY,FONT_HERSHEY_SIMPLEX,LINE_AA,THRESH_BINARY
import cv2
from matplotlib import image
from PIL import Image
import numpy as np 
import matplotlib.pyplot as plt 
import skimage

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
                'Método de umbralado de Kapur']
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
            titulo="Altura : " + str(h) + "       " + "Ancho: " + str(w) + "\n Tipo de Filtro:    "+ filtroSeleccionado.get()
            plt.suptitle(titulo)
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    

            if contrasteSeleccionado.get()=="Equalizado":
                hist = calcHist(imgrey, [0] , None, [256], [0,256])
                imeq = equalizeHist(imgrey)
                histEq = calcHist(imeq, [0] , None, [256], [0,256])
                plt.subplot(121)
                plt.plot(hist)
                plt.subplot(122)
                plt.plot(histEq)
                imshow("Original", imgrey)
                imshow("Eq", imeq)
                plt.show()
            if contrasteSeleccionado.get()=="Lineal":
                imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises    
                arreglo= np.asarray(imgrey)
                #Obtener nivel máximo y mínimo de nivel de gris
                maximo=0
                minimo=255
                nuevoarreglo=arreglo

                for fil,array in enumerate(arreglo):
                    for col,a in enumerate(array):
                        if a > maximo:
                            maximo = a
                            print(a, fil,col)

                for fil,array in enumerate(arreglo):
                    for col,a in enumerate(array):
                        if a < minimo:
                            minimo = a
                print( maximo, minimo)

                for fil,array in enumerate(nuevoarreglo):
                    for col,a in enumerate(array):
                        if a==maximo:
                            print((a-minimo)*((255)/(maximo-minimo)))
                        nuevoarreglo[fil,col]=(a-minimo)*((255)/(maximo-minimo))
                        if a==maximo:
                            print(nuevoarreglo[fil,col])

                hist2 = calcHist(nuevoarreglo, [0] , None, [256], [0,256])
                plt.subplot(121)
                plt.plot(hist2)
                plt.subplot(122)
                #plt.plot(hist2)
                #imshow("Original", arreglo)
                plt.imshow(nuevoarreglo, cmap="gray")
                plt.show()



            






        waitKey(0)  #comando para detener la imagen
        destroyAllWindows()

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
        
        if opcion.get()==4 or opcion.get()==5 or opcion.get()==6 or opcion.get()==7 or opcion.get()==8:
            umbraltxt.grid(row=2, column=2, padx=15, pady=5)
            umbralSel.grid(row=2, column=3, padx=15, pady=5)

    for i, op in enumerate(opciones):
        Radiobutton(root, text=op, variable=opcion, value=i+1, command=mostrarOpciones).grid(row=i+e, sticky=W, padx=15, pady=5)         

    labelDatos=Label(root)
    monitorDatos = Text(root, height=8, width=60, relief=GROOVE)
    
    root.mainloop()


if __name__ == "__main__":
    interfaz()