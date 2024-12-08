# Fichier contenant les tests de fonction effectu�s

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plot.plot import extraire_coord_fichier, affichage
from utils.utils import fusion_fichiers

# TEST 1 :R�cup�ration des positions de l'outil � partir du fichier txt
# Resultat : OK

# # Fichier d'entr�e (coordonn�es XYZIJK)
# fichierIN = 'plot\\input\\layer0.txt'
# coord = extraire_coord_fichier(fichierIN)
# for c in coord:
#     print('coordonnees :',c)


# TEST 2 : Affichage des positions et orientations de l'outil
# Resultat : OK 
# Test pour 2 fichiers diff�rents (Attention au param�tre frames configur� pour sauter certaines frames)
# Update : test plus valable car ajour d'un argument � fonction affichage

# fichierIN = 'plot\\input\\layer0.txt'
# #fichierIN = 'input\\carre_3axes.txt'
# coord = extraire_coord_fichier(fichierIN)
# affichage(coord)

# # TEST 3 : Utils/fusion_fichiers pour fusionner les fichiers contenant les coordonnees de l'outil pour chaque couche d'une piece
# # Resultat : OK
# directory = 'plot\\'
# fichiers = [directory + f'input\\{i}.txt' for i in range(10)]
# fichier_fusionne = directory + 'output\\layers0to9.txt'
# fusion_fichiers(fichiers,fichier_fusionne)

# # TEST 4 : Combinaison Test 2 + 3 pour afficher la trajectoire sur l'impression d'une pyramide en 9 couches
# # Resultat : OK, tr�s long si beaucoup de frames, utiliser frames_skip pour en sauter quelque unes
# fichierIN = 'plot\\output\\layers0to9.txt'
# coord = extraire_coord_fichier(fichierIN)
# frames_skip = 50
# affichage(coord,frames_skip)