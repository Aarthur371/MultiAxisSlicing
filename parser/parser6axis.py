import re
from utils import utils

#---------------------------VARIABLES---------------------------#

inFolder = "inputs"
outFile = "outputs\\commandesRobot.txt"
repere = "/RPlateau"

#---------------------------FONCTIONS---------------------------#

def extraire_gcode(fichier):
    ''' Parcourt le fichier donne et recupere les valeurs des positions X,Y,Z,A,B,C et celle de l'extrudeur E
    Commandes traitees : G0,G1,G28
    fichier : chemin relatif vers le fichier contenant le gcode
    return : liste des positions successives [X,Y,Z,A,B,C], elements = None si pas de deplacement dans une direction'''

    donnees = []
    lastPos = [0,0,0,0,0,0,0] #liste pour sauvegarder les derni�res positions sur chaque axe
    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        lignes = f.readlines()

        # Parcourir chaque ligne du fichier
        for ligne in lignes:
            # Traduit la commande G28 = "home all axis" en une position [0,0,0]
            if ligne.startswith('G28'):
                donnees.append([0.0,0.0,0.0,0.0,0.0,0.0,lastPos[3]])
            # V�rifier si la ligne commence par G1 ou G0 = "linear move"
            elif ligne.startswith(('G1','G0')):
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


def calculDirectionDepl(donnees):
    '''Creation du vecteur contenant les valeurs de deplacement en X,Y,Z entre 2 positions
    donnees : liste des positions absolues [X,Y,Z]
    return : liste des deplacement relatifs [X,Y,Z] '''

    directions = []
    for i in range (1,len(donnees)):
        # Calcule les d�placements relatifs dans chaque direction (arrondis � 5 digits)
        diffX = round(donnees[i][0] - donnees[i-1][0],5)
        diffY = round(donnees[i][1] - donnees[i-1][1],5)
        diffZ = round(donnees[i][2] - donnees[i-1][2],5)
        diffE = round(donnees[i][3] - donnees[i-1][3],5)
        directions.append([diffX,diffY,diffZ,diffE])
    return directions

def export_commandes_robot(fichier,vecteurs,repere,vit_lin):
    '''Genere les instructions de deplacement du robot en langage KUKA a partir de la liste des deplacements relatifs
    fichier : chemin vers le fichier .txt dans lequel generer les commandes robot
    vecteurs : liste des vecteurs deplacement [X,Y,Z,E]
    repere : nom du repere pour le deplacement du robot ["/NomRepere"]
    vit_lin : vitesse lineaire lors des translations [mm/s]
    return : None'''

    # Cr�� une sous liste sans les infos en E (derni�re colonne)
    xyzPos = [vect[:3] for vect in vecteurs]
    # Ouvrir un fichier en mode �criture
    with open(fichier, "w") as f:
        # Parcourir chaque ligne du tableau
        for pos in xyzPos:
            # Si c'est un d�placement lin�aire en X, Y ou Z
            if (pos[0]!=0 or pos[1]!=0 or pos[2]!=0):
                # Ecrit la commande robot pour les d�placements donn�s dans le fichier 
                f.write("linRel(Transformation.ofDeg(" + ",".join(map(str, pos)) + ",0.0,0.0,0.0),getApplicationData().getFrame(" + "\"" + repere + "\")).setCartVelocity(" + str(vit_lin) + ")," + "\n") 
