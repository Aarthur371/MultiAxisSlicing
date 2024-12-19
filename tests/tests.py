# Fichier contenant les tests de fonction effectués

import sys
import os
import matplotlib.pyplot as plt

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from plot.plot import extraire_coord_fichier, affichage, plot_nodes_from_file, plot_triangles_from_files
from utils.utils import fusion_fichiers
from preprocessing.STLtoTET import get_vertices_count, handleNodes, mesh_to_tet, off_to_node_ele, stl_to_off, preprocessing

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
# # Resultat : pareil que convertisseur en ligne (manque juste couleur des noeuds mais pas important)
# input_file = "preprocessing//input//calotte_spherique_R200.stl"
# out_file = "preprocessing//output//calotte_spherique.off"
# stl_to_off(input_file,out_file)


# # TEST 6 : Conversion des ele et node en fichier TET
# # Resultat : 
# ele = "preprocessing//output//calotte_spherique_R200.1.ele"
# nodes = "preprocessing//output//calotte_spherique_R200.1.node"
# out_file = "preprocessing//output//calotte_spherique_R200.1.tet"
# mesh_to_tet(nodes,ele,out_file)

# TEST 7 : Conversion de OFF en ele et node
# Resultat : 
# off_file = "preprocessing//output//calotte_spherique.off"
# ele = "preprocessing//output//calotte_spherique.ele"
# nodes = "preprocessing//output//calotte_spherique.node"
#  # Configuration d'options (cf. doc TetGen)
# off_to_node_ele(off_file,nodes,ele)

# # TEST 8 : représentation graphique d'un fichier node
# # Resultat  : ok
# nodes = "preprocessing//output//calotte_spherique.node"
# plot_nodes_from_file(nodes,1)
# nodes2 = "preprocessing//output//calotte_spherique_R200.1.node"
# plot_nodes_from_file(nodes2,2)
# plt.show()

# TEST 9 : représentation graphique des triangles (node + ele)
# Resultat : ok
# nodes = "preprocessing//output//calotte_spherique.node"
# ele = "preprocessing//output//calotte_spherique.ele"
# plot_triangles_from_files(nodes,ele)
# nodes = "preprocessing//output//calotte_spherique_R200.1.node"
# ele = "preprocessing//output//calotte_spherique_R200.1.ele"
# plot_triangles_from_files(nodes,ele)
# plt.show()

# # TEST 10 : chaine de traitement globale
# # Resultat 
# stl = "preprocessing//input//pyramide1.stl"
# tet = "preprocessing//output//pyramide1.tet"
# preprocessing(stl,tet)

# TEST 11 : creation d'un txt minimal pour ajouter a selection_file dans S3 Slicer
# Resultat : 
tet = "preprocessing//output//calotte_spherique.tet"
out = "preprocessing//output//calotte_spherique.txt"
nb_vertices = get_vertices_count(tet)
handleNodes(nb_vertices,out)

# TEST 12 : 
# Resultat : 

# TEST 13 : 
# Resultat : 

# TEST 14 : 
# Resultat : 