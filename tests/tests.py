# Fichier contenant les tests de fonction effectués

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plot import extraire_coord_fichier  

# TEST 1 :Récupération des positions de l'outil à partir du fichier txt
# Resultat : OK

# Fichier d'entrée (coordonnées XYZIJK)
fichierIN = 'input\\layer0.txt'
coord = extraire_coord_fichier(fichierIN)
for c in coord:
    print('coordonnees :',c)


# TEST 2 :
# Resultat :

# TEST 3 :
# Resultat :

# TEST 4 :
# Resultat :