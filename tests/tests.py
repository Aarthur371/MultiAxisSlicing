# Fichier contenant les tests de fonction effectu�s

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plot import extraire_coord_fichier  

# TEST 1 :R�cup�ration des positions de l'outil � partir du fichier txt
# Resultat : OK

# Fichier d'entr�e (coordonn�es XYZIJK)
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