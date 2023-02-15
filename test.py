import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
from test2 import TextEditor

def lire_fichier(path):
    fichier = open(path,"r")
    tableau =[[],[]]
    for ligne in fichier:
        ligne = ligne.strip()
        tab=ligne.split("\t")
        if(len(tab)>2):
            raise Exception("Erreur de formatage du fichier de test")
        compteur=0
        for digit in tab:
            if(not digit.isdigit()):
                for char in digit:
                    if(char.isalpha()):
                        raise Exception("Erreur de formatage du fichier de test")
                    if(char == "," or char == ";"):
                        digit = digit.replace(char,".")
                        
            if(compteur == 0):
                tableau[0].append(float(digit))
                compteur += 1
            else:
                tableau[1].append(float(digit))
    return tableau


def moyenne(varList):
    return sum(varList) / len(varList)

def sommeProd(varList1,varList2):
    sommeProd = 0
    for i in range(len(varList1)):
        sommeProd += varList1[i] * varList2[i]
    return sommeProd

# Calcule la moyenne du pro
def moyenneProd(varList1,varList2):
    return sommeProd(varList1,varList2) / len(varList1)

#calculer covarience de x et y 
def covarience(varList1,varList2):
    return moyenneProd(varList1,varList2) - (moyenne(varList1) * moyenne(varList2))


#calculer variance de x
def variance(varList1):
    return moyenneProd(varList1,varList1) - moyenne(varList1) * moyenne(varList1)

def odonneeOrigine(a,varList1,varList2):
    return moyenne(varList2) - a * moyenne(varList1)

def deriveePartielleA(a,b,varList1,varList2):
    return 2 * (a * sommeProd(varList1,varList1) + b * sum(varList1) - sommeProd(varList1,varList2))

def deriveePartielleB(a,b,varList1,varList2):
    return 2 * (a * sum(varList1) + b * len(varList1) - sum(varList2))    

def gradient(x,y):
    a = 1
    b = 1
    notFini = True
    while(notFini):
        if(abs(deriveePartielleA(a,b,x,y))<=0.0001 and abs(deriveePartielleB(a,b,x,y)<=0.0001)):
            notFini = False
        
        res1=deriveePartielleA(a,b,x,y)
        res2=deriveePartielleB(a,b,x,y)
        a=a-res1*0.00001    
        b=b-res2*0.00001
    return a,b

def methodeAnalytique():
    a = covarience(tableau[0],tableau[1]) / variance(tableau[0])
    return a,odonneeOrigine(a,tableau[0],tableau[1])

class Application(tk.Frame):
    aGradient = 0
    bGradient = 0
    aAnalytique = 0
    bAnalytique = 0

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.menubar = tk.Menu(self.master)
        self.master.config(menu=self.menubar)
        self.squelette()
        self.create_widgets()
        self.afficherGraphique()

        self.editor()
        

    def squelette(self):
        self.left_column = tk.Frame(self.master, width=300, height=500)
        self.middle_column = tk.Frame(self.master, width=500, height=500)
        self.right_column = tk.Frame(self.master, width=500, height=500)
        self.left_column.grid(row=0, column=0)
        self.middle_column.grid(row=0, column=1)
        self.right_column.grid(row=0, column=2)

    def create_widgets(self):

        self.createBtn("Methode Gradient",self.setGradient)
        self.createBtn("Methode Analytique",self.setAnalytique)
        self.createBtn("QUIT",self.master.destroy)

        self.gradient = tk.Label(self)
        self.gradient["text"] = "Valeur de a : " + str(self.aGradient) + " b : " + str(self.bGradient)
        self.gradient.pack(side="right")

        self.analytique = tk.Label(self)
        self.analytique["text"] = "Valeur de a : " + str(self.aAnalytique) + " b : " + str(self.bAnalytique)
        self.analytique.pack(side="right")

    def createBtn(self,title,command):
        btn = tk.Button(self.left_column)
        btn["text"] = title
        btn["command"] = command
        btn.pack()

    def setGradient(self):
        (self.aGradient,self.bGradient) = gradient(tableau[0],tableau[1])
        self.gradient["text"] = "Valeur de a : " + str(self.aGradient) + " b : " + str(self.bGradient)
        self.gradient.pack(side="top")


    def setAnalytique(self):
        (self.aAnalytique,self.bAnalytique) = methodeAnalytique()
        self.analytique["text"] = "Valeur de a : " + str(self.aAnalytique) + " b : " + str(self.bAnalytique)
        self.analytique.pack(side="top")

    def afficherGraphique(self):
        (slope,intercept) = gradient(tableau[0],tableau[1])
        x = np.arange(1,160)
        y = slope * x + intercept
        fig = Figure()
        plot1 = fig.add_subplot(111)
        plot1.scatter(tableau[0],tableau[1])
        plot1.plot(x,y)
        canvas = FigureCanvasTkAgg(fig,master=self.right_column)  
        canvas.draw()
        canvas.get_tk_widget().pack()

    def editor(self):
        TextEditor(self.middle_column,self.menubar)
        
        #TODO Simulation jeu de données
        #TODO Calcul indicateur
        #TODO Estimation prix appartement



try:
    tableau = lire_fichier('ressources/test.txt')
    root = tk.Tk()
    app = Application(master=root)
    app.mainloop()
except Exception as e:
    print(e)


