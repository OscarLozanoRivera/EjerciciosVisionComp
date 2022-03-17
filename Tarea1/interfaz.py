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

    root.title("Sistema de Archivos Distribuidos")

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
        img = imread(imagen)
        if opcion==1:
            imgrey=cvtColor(img, COLOR_BGR2GRAY)
            h = img.shape[0]
            w = img.shape[1]
            text="Altura : "+str(h)+" , Ancho: "+str(w)
            composite_img = putText(img, text, ( int(w/10) , int(h-(h/10)) ), FONT_HERSHEY_SIMPLEX,
                1.0, (255, 255, 255), 2, LINE_AA, False)
            imshow('Imagen en escala de grises',composite_img)


        if opcion==2:
            fig = plt.figure()
            img = imread(imagen)
            img_2 = img[:,:,[2,1,0]]
            plt.imshow(img_2, animated= True)
            plt.show()

        if opcion==3:
            img = imread(imagen,0)
            hist = calcHist([img], [0], None, [256], [0, 256])
            fig = plt.figure()
            plt.plot(hist, color='r')
            plt.show()

        if opcion==4:
            umbral= int(umbralSel.get())
            t2, imgbin2 = threshold(img, umbral, 256, THRESH_BINARY) 
            imshow('Imagen binarizada 2',imgbin2)

        if opcion==5:
            umbral= int(umbralSel.get())
            imgrey=cvtColor(img, COLOR_BGR2GRAY)     #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza       
            arreglo= np.asarray(imgbin)
            n1=0
            n2=0
            n3=0
            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1

            print("Numero de objetos en la imagen = ",abs(n1-n2+n3))
            imshow('Imagen binarizada ',imgbin)

        if opcion==6:
            umbral=int(umbralSel.get())
            imgrey=cvtColor(img, COLOR_BGR2GRAY)     #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza 
            imshow('Imagen binarizada ',imgbin)

            arreglo= np.asarray(imgbin)

            n1=0
            n2=0
            n3=0

            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1

            print("Numero de huecos en la imagen = ",1-(n1-n2+n3))

        if opcion==7:
            umbral=int(umbralSel.get())
            imgrey=cvtColor(img, COLOR_BGR2GRAY)     #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza 
            imshow('Imagen binarizada ',imgbin)

            arreglo= np.asarray(imgbin)

            n1=0
            n2=0
            n3=0

            for fil,array in enumerate(arreglo):
                for col,a in enumerate(array):
                    if a==255:
                        if col < len(array)-1 and fil < len(arreglo)-1 and col>1 and fil>1:
                            if arreglo[fil,col+1] == 0   and arreglo[fil+1,col] == 0   and arreglo[fil+1,col+1] == 0:
                                n1+=1
                            if arreglo[fil,col+1] == 255 and arreglo[fil+1,col] == 255 and arreglo[fil+1,col+1] == 0:
                                n2+=1
                            if arreglo[fil,col-1] == 0   and arreglo[fil+1,col-1] == 255   and arreglo[fil+1,col] == 0:
                                n3+=1

            print("Numero de huecos en la imagen = ",abs(1-(n1-n2+n3)))

        if opcion==8:
            umbral=int(umbralSel.get())
            imagenO= imread(imagen)                  #Se obtiene la imagen
            img= imread(imagen)                  #Se obtiene la imagen
            imgrey=cvtColor(img, COLOR_BGR2GRAY)     #Se convierte a escala de grises
            t2, imgbin = threshold(imgrey, umbral, 255, THRESH_BINARY)  #Se binariza 
            arreglo = np.asarray(img)
            arregloBin = np.asarray(imgbin)
            edge_img = Canny(imagenO,200,200)

            n1=0
            n2=0
            n3=0

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
            imshow('Imagen con bordes',edge_img)
            imshow('Imagen Original ',imagenO)
            imshow('Imagen Binarizada ',arregloBin)
            imshow('Imagen con Contorno ',arreglo)

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