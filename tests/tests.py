# Fichier contenant les tests de fonction effectu�s

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plot import extraire_coord_fichier, affichage

# TEST 1 :R�cup�ration des positions de l'outil � partir du fichier txt
# Resultat : OK

# Fichier d'entr�e (coordonn�es XYZIJK)
# fichierIN = 'input\\layer0.txt'
# coord = extraire_coord_fichier(fichierIN)
# for c in coord:
#     print('coordonnees :',c)


# TEST 2 : Affichage des positions et orientations de l'outil
# Resultat : OK 
# Test pour 2 fichiers diff�rents (Attention � adapter la variable t au nombre de positions � tracer t<=nb pos)

# fichierIN = 'input\\layer0.txt'
fichierIN = 'input\\carre_3axes.txt'
coord = extraire_coord_fichier(fichierIN)
affichage(coord)

# TEST 3 :
# Resultat :

# TEST 4 :
# Resultat :