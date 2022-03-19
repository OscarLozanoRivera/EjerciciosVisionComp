import tkinter
from tkinter.ttk import Button, Label, Radiobutton,Spinbox
from tkinter import Text,IntVar
from tkinter.constants import GROOVE, W
from tkinter import filedialog as fd
from cv2 import imread,cvtColor,imshow,waitKey,destroyAllWindows,putText,calcHist,threshold,Canny,COLOR_BGR2GRAY,FONT_HERSHEY_SIMPLEX,LINE_AA,THRESH_BINARY
import numpy as np 
import matplotlib.pyplot as plt 
from PIL import Image
from io import BytesIO

def interfaz():
    root = tkinter.Tk()
    # Icono Aplicación
    ancho_ventana = 400
    alto_ventana = 300
    x_ventana = root.winfo_screenwidth() // 2 - ancho_ventana // 2
    y_ventana = root.winfo_screenheight() // 2 - alto_ventana // 2
    posicion = str(ancho_ventana) + "x" + str(alto_ventana) + \
        "+" + str(x_ventana) + "+" + str(y_ventana)
    root.geometry(posicion)
    root.resizable(False, False)

    root.title("Tarea 1 RFVC")

    opciones = ['Imagen en Niveles de Gris', 
                'Identificar pixel', 
                'Histograma de imagen',
                'Imagen binaria con umbral manual', 
                'Número de objetos (sin huecos)', 
                'Número de huecos de un objeto', 
                'Simple o multiplemente conectado', 
                'Marcar contornos']
    opcion = IntVar()
    opcion.set(None)
    i = 0
    e=1

    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                #Se carga la imagen a memoria
        if opcion==1:                       #Opcion 1 seleccionada en la interfaz gráfica
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Convertir imagen de formato RGB a Escala de Grises
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            text="Altura : "+str(h)+" , Ancho: "+str(w)     #Texto sobre la información de la imagen
            composite_img = putText(img, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2, LINE_AA, False)    #Agregar características de la imagen como texto
            imshow('Imagen en escala de grises',composite_img)  #Mostrar imagen en una ventana nueva

    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                    #Se carga la imagen a memoria
        if opcion==2:                           #Opcion 2 seleccionada en la interfaz gráfica
            img_2 = img[:,:,[2,1,0]]            #Tomar todos los canales (R,G,B) de la imagen
            plt.imshow(img_2, animated= True)   #Dibujar en una ventana mediante la biblioteca matplotlib
            plt.show()                          #Mostrar la nueva ventana con matplotlib


    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                                #Se carga la imagen a memoria
        if opcion==3:                                       #Opcion 3 seleccionada en la interfaz gráfica
            fig,axes=plt.subplots(nrows=1, ncols=1)         #Definir el plano en el que se graficará con mathplotlib
            color = ('b','g','r')
            for i,col in enumerate(color):                  #Crear un histograma por cada color (R,G,B)
                histr = calcHist([imagen],[i],None,[256],[0,256])   #Calcular el histograma de la imagen según el color
                plt.plot(histr,color = col)                 #Dibujar el histograma en el plano asignado
                plt.xlim([0,256])                           #Definir el límite en el eje x del plano
            imshow("Imagen Original",img)                   #Mostra la imagen en una nueva ventana
            plt.show()                                      #Mostrar el histograma en una ventana con matplotlib

    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                                             #Se carga la imagen a memoria
        if opcion==4:                                                   #Opcion 4 seleccionada en la interfaz gráfica
            umbral= int(umbralSel.get())                                #Obtener umbral que seleccionó el usuario
            t2, imgbin = threshold(img, umbral, 256, THRESH_BINARY)    #Convertir imagen a binaria con el umbral seleccionado
            imshow('Imagen binarizada',imgbin)                       #Mostrar imagen en una ventana nueva
            waitKey(0)                                                  #Comando para detener la imagen
            destroyAllWindows()

    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                                            #Se carga la imagen a memoria
        if opcion==5:                                                   #Opcion 5 seleccionada en la interfaz gráfica
            umbral= int(umbralSel.get())                                #Obtener umbral que seleccionó el usuario
            imgrey=cvtColor(img, COLOR_BGR2GRAY)                        #Se convierte la imagen a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza la imagen      
            arreglo= np.asarray(imgbin)                                 #Convertir la información de la imagen a un arreglo numpy
            n1=0    
            n2=0
            n3=0
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            """Se recorre la imagen para buscar las máscaras
                |1 0|       |1 1|       |1 0|
                |0 0|       |1 0|       |0 1|
            """
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1: #Evitar buscar máscaras en los bordes
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1                                           #Contar mascara 1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1                                           #Contar mascara 2
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1                                           #Contar mascara 3

            text="Numero de objetos en la imagen = " + abs(n1-n2+n3)            #Texto sobre la información de la imagen
            composite_img = putText(imgbin, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 2, LINE_AA, False)                        #Agregar el número de objetos de la imagen como texto
            imshow('Imagen binarizada ',imgbin)                         #Mostrar imagen en una ventana nueva
            waitKey(0)                                                  #Comando para detener la imagen
            destroyAllWindows()


    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                            #Se carga la imagen a memoria
        if opcion==6:                                   #Opcion 6 seleccionada en la interfaz gráfica
            umbral=int(umbralSel.get())                 #Obtener umbral que seleccionó el usuario
            imgrey=cvtColor(img, COLOR_BGR2GRAY)        #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza la imagen
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles
            arreglo= np.asarray(imgbin)             #Convertir la información de la imagen a un arreglo numpy
            n1=0
            n2=0
            n3=0
            """Se recorre la imagen para buscar las máscaras
                |1 0|       |1 1|       |1 0|
                |0 0|       |1 0|       |0 1|
            """
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1: #Evitar buscar máscaras en los bordes
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1                               #Contar mascara 1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1                               #Contar mascara 2
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1                               #Contar mascara 3
            text="Numero de huecos en la imagen = " + str(abs(1-(n1-n2+n3)))           #Texto sobre la información de la imagen
            composite_img = putText(imgbin, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1, LINE_AA, False)                        #Agregar el número de objetos de la imagen como texto                                
            imshow('Imagen binarizada ',composite_img)                    #Mostrar imagen en una nueva ventana
            waitKey(0)                                                    #Comando para detener la imagen
            destroyAllWindows()



    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                        #Se carga la imagen a memoria
        if opcion==7:                               #Opcion 7 seleccionada en la interfaz gráfica
            umbral=int(umbralSel.get())             #Obtener umbral que seleccionó el usuario
            imgrey=cvtColor(img, COLOR_BGR2GRAY)    #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza 
            h = img.shape[0]                        #Obtener altura de la imagen en pixeles
            w = img.shape[1]                        #Obtener ancho de la imagen en pixeles  
            arreglo= np.asarray(imgbin)             #Convertir la información de la imagen a un arreglo numpy
            n1=0
            n2=0
            n3=0
            """Se recorre la imagen para buscar las máscaras
                |1 0|       |1 1|       |1 0|
                |0 0|       |1 0|       |0 1|
            """
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:#Evitar buscar máscaras en los bordes
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1                       #Contar mascara 1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1                       #Contar mascara 2
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1                       #Contar mascara 3
            if 1-(n1-n2+n3)!=0:
                text="La imagen es simplemente conectada" + str(abs(1-(n1-n2+n3)))           #Texto sobre la información de la imagen
            else:
                text="La imagen es multiplemente conectada" + str(abs(1-(n1-n2+n3)))         #Texto sobre la información de la imagen
            composite_img = putText(imgbin, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                0.6, (255, 255, 255), 1, LINE_AA, False)                        #Agregar el número de objetos de la imagen como texto                                
            imshow('Imagen binarizada ',composite_img)                  #Mostrar imagen en una nueva ventana
            waitKey(0)                                                  #Comando para detener la imagen
            destroyAllWindows()

    def realizarAccion(opcion,imagen):       
        img = imread(imagen)                        #Se carga la imagen a memoria
        if opcion==8:
            umbral=int(umbralSel.get())             #Obtener umbral que seleccionó el usuario
            imagenO= imread(imagen)                 #Se obtiene la imagen
            img= imread(imagen)                     #Se obtiene la imagen
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



    def select_file():
        filetypes = (
            ('All files', '*.*'),
            ('JPG', '*.jpg'),
            ('PNG', '*.jpg'),
            ('JPEG', '*.jpeg')
        )

        filename = fd.askopenfilename(
            title='Open a file',
            initialdir='',
            filetypes=filetypes )

        realizarAccion(opcion.get(),filename)

    Label(root, text="Selecciona una opción a realizar").grid(row=i, column=0, sticky=W, padx=15, pady=5)
    
    Button(root, text="Seleccionar archivo", command=select_file).grid(row=1, column=2, columnspan=2,padx=15, pady=5)   
    umbralSel=Spinbox(root,width=3,from_=0,to=255,increment=1)
    umbraltxt=Label(root,text="Umbral")
    def mostrarOpciones():
        umbralSel.grid_forget()
        umbraltxt.grid_forget()
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