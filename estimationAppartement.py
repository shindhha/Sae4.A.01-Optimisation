import tkinter as tk
import numpy as np
import matplotlib as mpl
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, 
NavigationToolbar2Tk)
import math
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
def mediane(varList):
    millieu = len(varList) // 2
    if len(varList) % 2 == 0:
        mediane = varList[millieu] + varList[millieu + 1] / 2
    else:
        mediane = varList[millieu]
    return mediane
def etendue(varList):
    return max(varList) - min(varList)
def coef_correlation_lineaire(donnees):
    return covarience(donnees[0],donnees[1]) / (math.sqrt(variance(donnees[0])) * math.sqrt(variance(donnees[1])))
def moyenne(varList):
    return sum(varList) / len(varList)
def sommeProd(varList1,varList2):
    sommeProd = 0
    for i in range(len(varList1)):
        sommeProd += varList1[i] * varList2[i]
    return sommeProd
def moyenneProd(varList1,varList2):
    return sommeProd(varList1,varList2) / len(varList1)
def covarience(varList1,varList2):
    return moyenneProd(varList1,varList2) - (moyenne(varList1) * moyenne(varList2))
def variance(varList1):
    return moyenneProd(varList1,varList1) - moyenne(varList1) * moyenne(varList1)
def odonneeOrigine(a,varList1,varList2):
    return moyenne(varList2) - a * moyenne(varList1)
def deriveePartielleA(a,b,sommeProdXX,sommeProdXY,sumX):
    return 2 * (a * sommeProdXX + b * sumX - sommeProdXY)
def deriveePartielleB(a,b,sumX,sumY,length):
    return 2 * (a * sumX + b * length - sumY)
def cout(sommeProdYY,sommeProdXY,sommeProdXX,a,b,length,sumY,sumX):
    return sommeProdYY - 2 * a * sommeProdXY - 2 * b * sumY + a * a * sommeProdXX + 2 * a * b * sumX + length * b * b
"""
:param sumX: Somme des surfaces d'appartement
:param sumY: Somme des prix d'appartement
:param length: longueur des données
:param sommeProdXX: Somme des produits surfaces * surfaces
:param sommeProdXY: Somme des produits srufaces * prix
:param a: 'a' de départ
:param b: 'b' de départ
:param precision: précision souhaiter pour la condition d'arret
:param pas: vitesse d'apprentissage du modèles initiale
"""
def gradient(sumX,sumY,length,sommeProdXX,sommeProdXY,a = 1,b = 1,precision = 0.001,pas = 1):
    descenteFini = False
    nbIteration = 0
    maxIteration = 1e9
    devA = deriveePartielleA(a,b,sommeProdXX,sommeProdXY,sumX)
    devB = deriveePartielleB(a,b,sumX,sumY,length)
    while(not descenteFini and nbIteration < maxIteration):
        nbIteration += 1
        # Quand les dérivée arrivent en dessous de la précision souhaiter
        # On arrete la descente de gradient.
        if(abs(devA) <= precision and abs(devB) <= precision):
            descenteFini = True
        a -= devA * pas
        b -= devB * pas
        newDevA = deriveePartielleA(a,b,sommeProdXX,sommeProdXY,sumX)
        newDevB = deriveePartielleB(a,b,sumX,sumY,length)
        # Si la distance a 0 de la nouvelle dérivée est plus grande que l'ancienne.
        # Alors cela traduit une erreur dans le modèles.
        # Donc on réduit le pas.
        if (-10 > abs(devA) - abs(newDevA) or -10 > abs(devB) - abs(newDevB)):
            pas /= 100

        # On augmente le pas régulièrement pour accélérer la descente de gradient.
        if (nbIteration % 10 == 0):
            pas *= 3
        devA = newDevA
        devB = newDevB
    return a,b,nbIteration

def methodeAnalytique(tableau):
    a = covarience(tableau[0],tableau[1]) / variance(tableau[0])
    return a,odonneeOrigine(a,tableau[0],tableau[1])

class Application(tk.Frame):
    def __init__(self):
        self.master = tk.Tk()
        super().__init__(self.master)
        menubar = tk.Menu(self.master)
        self.master.config(menu=menubar)
        self.squelette()
        self.initMenu(menubar)

    def initMenu(self,menubar):
        file_menu = tk.Menu(menubar)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Nouveau", command=self.new_file)
        file_menu.add_command(label="Ouvrir", command=self.open_file)
        file_menu.add_command(label="Enregistrer", command=self.save_file)
        
    def initStat(self,tableau):
        self.sommeProdXX = sommeProd(tableau[0],tableau[0])
        self.sommeProdXY = sommeProd(tableau[0],tableau[1])
        self.sumX = sum(tableau[0])
        self.sumY = sum(tableau[1])
        self.length = len(tableau[0])
        varSurface = variance(tableau[0])
        varPrix = variance(tableau[1])
        self.tabStat = [
        ("Moyenne :",moyenne(tableau[0]),moyenne(tableau[1])),
        ("Variance :",varSurface,varPrix),
        ("Ecart-Type : ",math.sqrt(varSurface),math.sqrt(varPrix)),
        ("Mediane :",mediane(tableau[0]),mediane(tableau[1])),
        ("Etendue :",etendue(tableau[0]),etendue(tableau[1]))
        ]
        self.covarience = covarience(tableau[0],tableau[1])
        self.coef = coef_correlation_lineaire(tableau)

    def squelette(self):
        self.left_column = tk.Frame(self.master, width = 100, height = 500)
        self.middle_column = tk.Frame(self.master, width = 200, height = 500)
        self.left_column.grid(row=0, column=0)
        self.middle_column.grid(row=0, column=1)
        self.text = tk.Text(self.middle_column, undo=True)
        self.text.pack(fill=tk.BOTH,expand=True)
        self.create_widgets(self.left_column)

    def create_widgets(self,parentFrame):
        self.calc = self.createBtn("Calculer",self.calculer,parentFrame,"disabled")
        self.stat = self.createBtn("Afficher les statistique",self.afficherFenetreStatistique,parentFrame,"disabled")
        self.quitter = self.createBtn("QUIT",self.master.destroy,parentFrame,"normal")
        self.estime = self.createBtn("Estimer un appartement",self.afficherFenetreEstimation,parentFrame,"disabled")
        errEntry = tk.Entry(parentFrame,text="Erreur autoriser : ")
        pas = tk.Entry(parentFrame,text="Vitesse d'apprentissage (pas) : ")

        
    def afficherFenetreEstimation(self):
        estime = tk.Tk()
        surface = tk.Text(estime,undo=True)
        analytique = self.createLabel("Estimation analytique : " ,estime)
        gradient = self.createLabel("Estimation gradient : " ,estime)
        surfaceEntree = tk.Entry(estime,text="Surface : ")
        surfaceEntree.pack()
        self.createBtn("Estimer",lambda: self.estimer(analytique,gradient,surfaceEntree.get()),estime)

    def estimer(self,analytique,gradient,surface):
        (a,b) = self.getAnalytique()
        analytique["text"] = "Estimation analytique : " + str(a * int(surface) + b)
        (a,b,i) = self.getGradient()
        gradient["text"] = "Estimation gradient : " + str(a * int(surface) + b)

    def createLabel(self,title,parentFrame):
        label = tk.Label(parentFrame)
        label["text"] = title
        label.pack()
        return label

    def createBtn(self,title,command,parentFrame,state):
        btn = tk.Button(parentFrame)
        btn["text"] = title
        btn["command"] = command
        btn["state"] = state
        btn.pack()
        return btn
    def calculer(self):
        (self.aAnalytique,self.bAnalytique) = methodeAnalytique(self.tableau)     
        print(self.aAnalytique,self.bAnalytique)
        (self.aGradient,self.bGradient,self.nbIteration) = gradient(self.sumX,self.sumY,self.length,self.sommeProdXX,self.sommeProdXY)
        self.calc["state"] = "disabled"
        self.stat["state"] = "normal"

    def afficherFenetreStatistique(self):
        secondFrame = tk.Tk()
        left_column = tk.Frame(secondFrame, width = 100, height = 500)
        (aGradient,bGradient,nbIteration) = self.getGradient()
        (aAnalytique,bAnalytique) = self.getAnalytique()
        self.createLabel("Methode descente de gradient :",left_column)
        self.createLabel("Valeur de a : " + str(aGradient) + " b : " + str(bGradient),left_column)
        self.createLabel("Methode analytique :",left_column)
        self.createLabel("Valeur de a : " + str(aAnalytique) + " b : " + str(bAnalytique),left_column)
        self.setTableStat(left_column)
        self.createLabel("Covariance : " + str(self.covarience),left_column)
        self.createLabel("Coefficien de corrélation linéaire :" + str(self.coef),left_column)
        self.createLabel("Nombre d'iteration de la methode par descente de gradient : " + str(nbIteration),left_column)
        left_column.grid(row=0, column=0)
        self.afficherGraphique(secondFrame)


    def setTableStat(self,parentFrame):
        frame = tk.Frame(parentFrame)
        self.e = tk.Entry(frame)
        self.e.grid(row=0,column=1)
        self.e.insert(tk.END,"Surface")
        self.e["state"] = "disabled"
        self.e["disabledbackground"] = "white"
        self.e["disabledforeground"] = "black"
        self.e = tk.Entry(frame)
        self.e.grid(row=0,column=2)
        self.e.insert(tk.END,"Prix")
        self.e["state"] = "disabled"
        self.e["disabledbackground"] = "white"
        self.e["disabledforeground"] = "black"
        for i in range(1,len(self.tabStat)):
            for j in range(len(self.tabStat[0])):
                 
                self.e = tk.Entry(frame)
                self.e.grid(row=i, column=j)
                self.e.insert(tk.END, self.tabStat[i][j])
                self.e["state"] = "disabled"
                self.e["disabledbackground"] = "white"
                self.e["disabledforeground"] = "black" 
        frame.pack()

        

    def getDonneesGraphique(self):
        axeX = np.arange(1,max(self.tableau[0]))
        (a,b,i) = self.getGradient()
        axeYGradient = a * axeX + b
        (a,b) = self.getAnalytique()
        axeYAnalytique = a * axeX + b
        return axeX,axeYGradient,axeYAnalytique


    def afficherGraphique(self,parentFrame) :
        (axeX,axeYGradient,axeYAnalytique) = self.getDonneesGraphique()
        middle_column = tk.Frame(parentFrame, width = 200, height = 500)
        middle_column.grid(row=0, column=1)        
        fig = Figure()
        plot1 = fig.add_subplot(111)
        plot1.scatter(self.tableau[0],self.tableau[1])
        plot1.plot(axeX,axeYGradient,color='red')
        plot1.plot(axeX,axeYAnalytique,color='green')
        canvas = FigureCanvasTkAgg(fig,master=middle_column)  
        canvas.draw()
        canvas.get_tk_widget().pack()

    def new_file(self):
        self.text.delete("1.0", tk.END)

    def open_file(self):
        file = tk.filedialog.askopenfile(mode="r")
        if file is not None:
            content = file.read()
            self.text.delete("1.0","end")
            self.text.insert(tk.END, content)
            file.close()
            try:
                self.tableau = lire_fichier(file.name)
                self.initStat(self.tableau)
                self.calc["state"] = tk.NORMAL
                self.estime["state"] = tk.NORMAL
                self.stat["state"]= tk.DISABLED
            except Exception as e:
                self.calc["state"] = tk.DISABLED
                self.stat["state"] = tk.DISABLED
                self.estime["state"] = tk.DISABLED
            

    def save_file(self):
        file = tk.filedialog.asksaveasfile(mode="w")
        if file is not None:
            content = self.text.get("1.0", tk.END)
            file.write(content)
            file.close()

    def getGradient(self):
        return self.aGradient,self.bGradient,self.nbIteration

    def getAnalytique(self):
        return self.aAnalytique,self.bAnalytique


try:
    app = Application()
    app.mainloop()

except Exception as e:
    print(e)


