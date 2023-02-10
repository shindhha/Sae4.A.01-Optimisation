fichier = open('ressources/test.txt', "r")


tableau =[[],[]]
a=1
b=1


def lire_fichier(fichier):
    global tableau
    for ligne in fichier:
        ligne = ligne.strip()
        tab=ligne.split("\t")
        compteur=0
        for i in range(len(tab)):
            
            if(len(tab)>2):
                raise Exception("Erreur de formatage du fichier de test")
            if(tab[i].isdigit()==False):
                if(tab[i].find(".")==-1):
                    for char in tab[i]:
                        if(char.isdigit()==False):
                            tab[i]=tab[i].replace(char,".")
            if(compteur==0):
                tableau[0].append(float(tab[i]))
                compteur=compteur+1
            else:
                tableau[1].append(float(tab[i]))
    
# calculer moyen des x*y
def moyenne_xy(x,y):
    moyenne_xy=0
    for i in range(len(x)):
        moyenne_xy=moyenne_xy+x[i]*y[i]
    moyenne_xy=moyenne_xy/len(x)
    return moyenne_xy

           

#calculer covarience de x et y 
def covariance(x,y):
    moyenne_x=0
    moyenne_y=0
    for i in range(len(x)):
        moyenne_x=moyenne_x+x[i]
        moyenne_y=moyenne_y+y[i]
    moyenne_x=moyenne_x/len(x)
    moyenne_y=moyenne_y/len(y)
    moyenneXY = moyenne_xy(x,y)
    covarience=moyenneXY-(moyenne_x*moyenne_y)        
    return covarience


#calculer variance de x
def variance(x):
    moyenne_x=0
    moyenne_xx=0
    for i in range(len(x)):
        moyenne_x=moyenne_x+x[i]
    moyenne_x=moyenne_x/len(x)
    for i in range(len(x)):
        moyenne_xx=moyenne_xx+x[i]*x[i]
    moyenne_xx=moyenne_xx/len(x)
    variance=moyenne_xx-moyenne_x*moyenne_x

    return variance

def odonneeOrigine(x,y):
    moyx=0
    moyy=0
    for i in range(len(x)):
        moyx=moyx+x[i]
        moyy=moyy+y[i]
    moyx=moyx/len(x)
    moyy=moyy/len(y)
    b=(moyy-a*moyx)
    return b

lire_fichier(fichier)
a = covariance(tableau[0],tableau[1])/variance(tableau[0])
b=odonneeOrigine(tableau[0],tableau[1])
print(a)
print(b)


def deriveePartielleA(a,b,x,y):
    sommeXX=0
    for i in range(len(x)):
        sommeXX=sommeXX+x[i]*x[i]
    sommeX=0
    for i in range(len(x)):
        sommeX=sommeX+x[i]
    sommeXY=0
    for i in range(len(x)):
        sommeXY=sommeXY+x[i]*y[i]
    resultat=0
    resultat=2*(a*sommeXX+b*sommeX-sommeXY)
    return resultat

def deriveePartielleB(a,b,x,y):
    sommeX=0
    for i in range(len(x)):
        sommeX=sommeX+x[i]
    sommeY=0
    for i in range(len(y)):
        sommeY=sommeY+y[i]
    resultat=0
    resultat=2*(a*sommeX+b*len(x)-sommeY)   
    return resultat
    
a=1
b=1
def gradient(a,b,x,y):
    notFini = True
    while(notFini):
        if(abs(deriveePartielleA(a,b,x,y))<=0.0001 and abs(deriveePartielleB(a,b,x,y)<=0.0001)):
            notFini = False
        
        res1=deriveePartielleA(a,b,x,y)
        res2=deriveePartielleB(a,b,x,y)
        a=a-res1*0.00001
        b=b-res2*0.00001


    return a,b
print("methode gradient")
print(gradient(a,b,tableau[0],tableau[1]))

    





