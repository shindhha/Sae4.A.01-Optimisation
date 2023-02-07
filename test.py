

fichier = open('ressources/test.txt', "r")


tableau =[[],[]]

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
def covarience(x,y):
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
a = covarience(tableau[0],tableau[1])/variance(tableau[0])
b=odonneeOrigine(tableau[0],tableau[1])
print(b)
print(a)

#a refaire
# def derivéA(x,y,a,b):
#     sommeX=0
#     sommeXY=0
#     sommeXX=0
#     for i in range(len(x)):
#         sommeX=sommeX+x[i]
#         sommeXY=sommeXY+x[i]*y[i]
#         sommeXX=sommeXX+x[i]*x[i]
#     a=2*(sommeXX+b*sommeX-sommeXY)
#     return a

# def derivéB(x,y,a,b):
#     sommeX=0
#     sommeY=0
#     sommeXY=0
#     sommeXX=0
#     for i in range(len(x)):
#         sommeX=sommeX+x[i]
#         sommeY=sommeY+y[i]
#         sommeXY=sommeXY+x[i]*y[i]
#         sommeXX=sommeXX+x[i]*x[i]
#     be=2(a*sommeX+len(x)*b-sommeY)
#     return be

# def gradient(x,y,a,b):
#     for i in range(100):
#         a=a-0.0001*derivéA(x,y,a,b)
#         b=b-0.0001*derivéB(x,y,a,b)
#     return a,b

# a,b=gradient(tableau[0],tableau[1],1,2)
# print(a)
# print(b)
    





