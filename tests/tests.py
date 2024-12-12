# Fichier contenant les tests de fonction effectués

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plot.plot import extraire_coord_fichier, affichage
from utils.utils import fusion_fichiers
from preprocessing.STLtoTET import mesh_to_tet, stl_to_node_ele, stl_to_off

# TEST 1 :Récupération des positions de l'outil à partir du fichier txt
# Resultat : OK

# # Fichier d'entrée (coordonnées XYZIJK)
# fichierIN = 'plot\\input\\layer0.txt'
# coord = extraire_coord_fichier(fichierIN)
# for c in coord:
#     print('coordonnees :',c)


# TEST 2 : Affichage des positions et orientations de l'outil
# Resultat : OK 
# Test pour 2 fichiers différents (Attention au paramètre frames configuré pour sauter certaines frames)
# Update : test plus valable car ajour d'un argument à fonction affichage

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
# # Resultat : OK, très long si beaucoup de frames, utiliser frames_skip pour en sauter quelque unes
# fichierIN = 'plot\\output\\layers0to9.txt'
# coord = extraire_coord_fichier(fichierIN)
# frames_skip = 50
# affichage(coord,frames_skip)

# # TEST 5 : Conversion d'un fichier STL en fichier OFF
# # Resultat : ok
# input_file = "preprocessing//input//pyramide1.stl"
# out_file = "preprocessing//output//pyramide1.off"
# stl_to_off(input_file,out_file)


# TEST 6 : Conversion des ele et node en fichier TET
# Resultat : 
stl = "preprocessing//input//pyramide1.stl"
ele = "preprocessing//input//ImageToStl.com_pyramide1.1.ele"
nodes = "preprocessing//input//ImageToStl.com_pyramide1.1.node"
out_file = "preprocessing//output//pyramide1.tet"
stl_to_node_ele(stl,nodes,ele)
mesh_to_tet(nodes,ele,out_file)

# TEST 7 :
# Resultat : 