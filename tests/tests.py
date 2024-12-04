# Fichier contenant les tests de fonction effectués

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '/utils')))
from plot import extraire_coord_fichier, affichage
from utils.utils import fusion_fichiers

# TEST 1 :Récupération des positions de l'outil à partir du fichier txt
# Resultat : OK

# Fichier d'entrée (coordonnées XYZIJK)
# fichierIN = 'input\\layer0.txt'
# coord = extraire_coord_fichier(fichierIN)
# for c in coord:
#     print('coordonnees :',c)


# TEST 2 : Affichage des positions et orientations de l'outil
# Resultat : OK 
# Test pour 2 fichiers différents (Attention au paramètre frames configuré pour sauter certaines frames)

# fichierIN = 'input\\layer0.txt'
# #fichierIN = 'input\\carre_3axes.txt'
# coord = extraire_coord_fichier(fichierIN)
# affichage(coord)

# TEST 3 : Utils/fusion_fichiers pour fusionner les fichiers contenant les coordonnees de l'outil pour chaque couche d'une piece
# Resultat : OK
fichiers = ['input\\0.txt','input\\1.txt','input\\2.txt','input\\3.txt','input\\4.txt','input\\5.txt'
,'input\\6.txt','input\\7.txt','input\\8.txt','input\\9.txt']
fichier_fusionne = 'output\\layers0to9.txt'
fusion_fichiers(fichiers,fichier_fusionne)

# TEST 4 :
# Resultat :