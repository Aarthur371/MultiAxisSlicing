import re
from utils import utils

#---------------------------VARIABLES---------------------------#

inFolder = "inputs"
outFile = "outputs\\commandesRobot.txt"
repere = "/RPlateau"

#---------------------------FONCTIONS---------------------------#

def extraire_gcode(fichier):
    ''' Parcourt le fichier donne et recupere les valeurs des positions X,Y,Z,A,B,C et celle de l'extrudeur E
    Commandes traitees : G0,G1
    fichier : chemin relatif vers le fichier contenant le gcode
    return : liste des positions successives [X,Y,Z,A,B,C], elements = None si pas de deplacement dans une direction'''

    donnees = []
    lastPos = [0,0,0,0,0,0,0] #liste pour sauvegarder les derni�res positions sur chaque axe
    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        lignes = f.readlines()

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            # V�rifier si la ligne commence par G1 ou G0 = "linear move"
            if ligne.startswith(('G1','G0')):
                # Utiliser une regex pour trouver les valeurs X,Y,Z,A,B,C,E
                x = re.search(r'X([-\d.]+)', ligne)
                y = re.search(r'Y([-\d.]+)', ligne)
                z = re.search(r'Z([-\d.]+)', ligne)
                a = re.search(r'A([-\d.]+)', ligne)
                b = re.search(r'B([-\d.]+)', ligne)
                c = re.search(r'C([-\d.]+)', ligne)
                e = re.search(r'E([-\d.]+)', ligne)

                # Extraire les valeurs et les mettre dans une liste, mettre None si une valeur est manquante
                valeurs = [
                    float(x.group(1)) if x else lastPos[0],
                    float(y.group(1)) if y else lastPos[1],
                    float(z.group(1)) if z else lastPos[2],
                    float(a.group(1)) if a else lastPos[3],
                    float(b.group(1)) if b else lastPos[4],
                    float(c.group(1)) if c else lastPos[5],
                    float(e.group(1)) if e else lastPos[6]
                ]
                # V�rifie que l'on a au moins une instruction de d�placement diff�rente des pr�c�dentes (exclue les commandes Feedrate)
                if not utils.listesIdentiques(valeurs, lastPos):
                    # Ajouter cette ligne de valeurs � la liste de donn�es
                    donnees.append(valeurs)
                    lastPos = valeurs

    return donnees

def extraire_gcode_Open5x(fichier):
    ''' Parcourt le fichier gcode genere par le slicer open-5x et recupere les valeurs des positions x,y,z,u,v et celle de l'extrudeur E
    Commandes traitees : G0,G1
    fichier : chemin relatif vers le fichier contenant le gcode
    return : liste des positions successives [X,Y,Z,0,U,V,E], elements = None si pas de deplacement dans une direction'''

    donnees = []
    lastPos = [0,0,0,0,0,0,0] #liste pour sauvegarder les derni�res positions sur chaque axe
    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        lignes = f.readlines()

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            # V�rifier si la ligne commence par G1 ou G0 = "linear move"
            if ligne.__contains__('G1') or ligne.__contains__('G0'):
                # Utiliser une regex pour trouver les valeurs X,Y,Z,A,B,C,E
                x = re.search(r'x([-\d.]+)', ligne)
                y = re.search(r'y([-\d.]+)', ligne)
                z = re.search(r'z([-\d.]+)', ligne)
                u = re.search(r'u([-\d.]+)', ligne)
                v = re.search(r'v([-\d.]+)', ligne)
                e = re.search(r'E([-\d.]+)', ligne)

                # Extraire les valeurs et les mettre dans une liste, mettre None si une valeur est manquante
                valeurs = [
                    float(x.group(1)) if x else lastPos[0],
                    float(y.group(1)) if y else lastPos[1],
                    float(z.group(1)) if z else lastPos[2],
                    0,  # pas de rotation autour de z 
                    float(u.group(1)) if u else lastPos[4],
                    float(v.group(1)) if v else lastPos[5],
                    float(e.group(1)) if e else lastPos[6]
                ]
                print(valeurs)
                # V�rifie que l'on a au moins une instruction de d�placement diff�rente des pr�c�dentes (exclue les commandes Feedrate)
                if not utils.listesIdentiques(valeurs, lastPos):
                    # Ajouter cette ligne de valeurs � la liste de donn�es
                    donnees.append(valeurs)
                    lastPos = valeurs

    return donnees

def gcode_s3slicer(donnees):
    ''' Adapte le gcode recupere a partir de s3 slicer pour avoir les bonnes valeurs pour chaque parametre
   donnees : tableau [X,Y,Z,E,B,C,0] dans le cas de s3 slicer
   newDonnes : tableau [X,Y,Z,A,B,C,E] '''
    newDonnees = []
    for donnee in donnees:
        x = donnee[0]
        y = donnee[1]
        z = donnee[2]
        a = 0.0 # Pas de donn� de l'angle de rotation autour de Z (angle A) dans s3Slicer 
        b = donnee[4]
        c = donnee[5]
        e = donnee[3] # D�bit extrudeur donn� par A et non E dans s3Slicer
        newDonnees.append([x,y,z,a,b,c,e])
    return newDonnees


def calculDirectionDepl(donnees):
    '''Creation du vecteur contenant les valeurs de deplacement en X,Y,Z et A,B,C entre 2 positions
    donnees : liste des positions/orientations absolues [X,Y,Z,A,B,C]
    return : liste des deplacement/orientations relatifs [X,Y,Z,A,B,C] '''

    directions = []
    for i in range (1,len(donnees)):
        # Calcule les d�placements relatifs dans chaque direction (arrondis � 5 digits)
        diffX = round(donnees[i][0] - donnees[i-1][0],5)
        diffY = round(donnees[i][1] - donnees[i-1][1],5)
        diffZ = round(donnees[i][2] - donnees[i-1][2],5)
        diffA = round(donnees[i][3] - donnees[i-1][3],5)
        diffB = round(donnees[i][4] - donnees[i-1][4],5)
        diffC = round(donnees[i][5] - donnees[i-1][5],5)
        diffE = round(donnees[i][6] - donnees[i-1][6],5)
        directions.append([diffX,diffY,diffZ,diffA,diffB,diffC,diffE])
    return directions

def export_commandes_robot(fichier,vecteurs,repere,vit_lin,vit_ang):
    '''Genere les instructions de deplacement du robot en langage KUKA a partir de la liste des deplacements relatifs
    fichier : chemin vers le fichier .txt dans lequel generer les commandes robot
    vecteurs : liste des vecteurs deplacement [X,Y,Z,A,B,C,E]
    repere : nom du repere pour le deplacement du robot ["/NomRepere"]
    vit_lin : vitesse lineaire lors des translations [mm/s]
    vit_ang : vitesse angulaire lors de rotations [rad/s]
    return : None'''
    # Arrondi la vitesse angulaire � 3 d�cimales
    vit_ang = round(vit_ang,3)

    # Cr�� une sous liste sans les infos en E (derni�re colonne)
    pose = [vect[:6] for vect in vecteurs]
    # Ouvrir un fichier en mode �criture
    with open(fichier, "w") as f:
        # Parcourir chaque ligne du tableau
        for p in pose:
            # Pas de d�composition des mvmts en rotation + translation
            f.write("linRel(Transformation.ofDeg(" + ",".join(map(str, p)) + "),getApplicationData().getFrame(" + "\"" + repere + "\")).setCartVelocity(" + str(vit_lin) + ").setOrientationVelocity(" + str(vit_ang) + ")," + "\n") 
            

def export_commandes_robot_split(fichier,vecteurs,repere,vit_lin,vit_ang):
    '''Genere les instructions de deplacement du robot en langage KUKA a partir de la liste des deplacements relatifs
    fichier : chemin vers le fichier .txt dans lequel generer les commandes robot
    vecteurs : liste des vecteurs deplacement [X,Y,Z,A,B,C,E]
    repere : nom du repere pour le deplacement du robot ["/NomRepere"]
    vit_lin : vitesse lineaire lors des translations [mm/s]
    vit_ang : vitesse angulaire lors de rotations [rad/s]
    return : None'''

    oldE = 0
    i = 1 #num�ro du motionbatch
    j = 1
    resetLigne = 0
    # Ouvrir un fichier en mode ecriture
    with open(fichier, "w") as f:
        #Ajout d'une ligne initiale pour la creation de methode JAVA motionbatch
        f.write("public void mb1(){" + "\n")
        f.write("double blend = 4;" + "\n" )
        f.write("MotionBatch mb191 = new MotionBatch(" + "\n")
        # Parcourir chaque ligne du tableau
        for pos in vecteurs:
            if (pos[6]>0 and oldE==0): #Si E positif, on clos le motionbatch et on active l'extrusion puis on ouvre le motionbatch_suivant
                f.write("\n" + ").setBlendingCart(blend);" + "\n")
                f.write("_lbr.move(mb191);" + "\n")
                f.write("}" + "\n" + "\n")
                i = i + 1
                resetLigne = 0
                f.write("public void mb"+ str(i) + "(){" + "\n")
                f.write("double blend = 4;" + "\n" )
                f.write("MotionBatch mb191 = new MotionBatch(" + "\n")
                oldE = 1
            if (pos[6]<0 and oldE==1): #Si E negatif, on d�sactive l'extrusion
                f.write("\n" + ").setBlendingCart(blend);" + "\n")
                f.write("_lbr.move(mb191);" + "\n")
                f.write("}" + "\n" + "\n")
                i = i + 1
                resetLigne = 0
                f.write("public void mb"+ str(i) + "(){" + "\n")
                f.write("double blend = 4;" + "\n" ) # Param�tre de blending appliqu� pour ce Motion Batch
                f.write("MotionBatch mb191 = new MotionBatch(" + "\n") # Appelle le MotionBatch qui vient d'�tre d�fini, pour qu'il soit execut�
                oldE = 0   
                # Ecrit la commande robot pour les deplacements donnes dans le fichier 
            if (resetLigne==1):
                f.write("linRel(Transformation.ofDeg(" + ",".join(map(str, pos[:6])) + "),getApplicationData().getFrame(" + "\"" + repere + "\")).setCartVelocity(" + str(vit_lin) + ").setOrientationVelocity(" + str(vit_ang) + ")," + "\n") 
            if (resetLigne==0):
                f.write("linRel(Transformation.ofDeg(" + ",".join(map(str, pos[:6])) + "),getApplicationData().getFrame(" + "\"" + repere + "\")).setCartVelocity(" + str(vit_lin) + ").setOrientationVelocity(" + str(vit_ang) + ")," + "\n") 
                resetLigne = 1

        f.write(").setBlendingCart(blend);" + "\n")
        f.write("_lbr.move(mb191);" + "\n")
        f.write("}" + "\n" + "\n")
        f.write("Appel de methode a mettre dans le run " + "\n")
        while i > 0 :
            f.write("mb"+str(j)+"();"+"\n")
            i = i - 1
            j = j + 1