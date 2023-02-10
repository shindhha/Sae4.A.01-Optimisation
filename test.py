
tableau =[[],[]]
a=1
b=1


def lire_fichier(path):
    fichier = open(path,"r")
    global tableau
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

def odonneeOrigine(varList1,varList2):
    return moyenne(varList2) - a * moyenne(varList1)

def deriveePartielleA(a,b,varList1,varList2):
    return 2 * (a * sommeProd(varList1,varList1) + b * sum(varList1) - sommeProd(varList1,varList2))

def deriveePartielleB(a,b,varList1,varList2):
    return 2 * (a * sum(varList1) + b * len(varList1) - sum(varList2))

def gradient(varList1,varList2):
    a = 1
    b = 1
    while(deriveePartielleA(a,b,varList1,varList2)<=0.00001 and deriveePartielleB(a,b,varList1,varList2)<=0.0001):
        res1=deriveePartielleA(a,b,varList1,varList2)
        res2=deriveePartielleB(a,b,varList1,varList2)
        a = a-res1*0.0001
        b=b-res2*0.0001
    return a,b





    

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
try:
    lire_fichier('ressources/test.txt')
    a = covarience(tableau[0],tableau[1]) / variance(tableau[0])
    b = odonneeOrigine(tableau[0],tableau[1])
    print(a)
    print(b)
    a=1
    b=1
    print("methode gradient")
    print(gradient(a,b,tableau[0],tableau[1]))
except Exception as e:
    print(e)

