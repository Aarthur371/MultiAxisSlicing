# Fichier contenant l'ensemble des fonctions pour afficher des trajectoires outils + orientation de l'outil dans un repère 3D


import re
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#----------------------VARIABLES-------------------------#

# Fichier d'entrée (coordonnées XYZIJK)
fichierIN = 'input\\layer0.txt'

#------------------- FONCTIONS ------------------------#


# FONCTIONS LECTURE/ECRITURE FICHIER

def extraire_coord_fichier(fichier):
    ''' Extrait les coordonnees successives de l'effecteur
    fichier : chemin du fichier d'entree
    coord : tableau des coordonnees au format [X,Y,Z,I,J,K] '''
    coord = []

    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        # Lire chaque ligne, découper par espaces, et convertir les éléments en float
        for ligne in f:
            coordString = ligne.strip().split()
            try:
                # Convertir les éléments en float
                coord.append([float(val) for val in coordString])
            except ValueError:
                print(f"Erreur de conversion dans la ligne : {ligne.strip()}")

    return coord

# FONCTIONS AFFICHAGE

# def configPlot(vect_deplacement, ax):
#     # Récupération des points de trajectoire dans l'espace
#     t = np.linspace(0, 5, 1000) #nb de points à afficher
#     x = [coord[0] for coord in vect_deplacement]
#     y = [coord[1] for coord in vect_deplacement]
#     z = [coord[2] for coord in vect_deplacement]
#     beta = [coord[4] for coord in vect_deplacement]
#     gamma = [coord[5] for coord in vect_deplacement]

#     # Configuration initiale : définir les limites et la ligne vide qui sera mise à jour
#     ax.set_xlim(0, 100)
#     ax.set_ylim(0, 100)
#     ax.set_zlim(0, 20)
#     line, = ax.plot([], [], [], lw=2)

#     # Plateau 70x85 (en noir) dans le plan z=0
#     x_rect = [0, 70, 70, 0, 0]  # Sommets du rectangle sur l'axe x
#     y_rect = [0, 0, 85, 85, 0]  # Sommets du rectangle sur l'axe y
#     z_rect = [0, 0, 0, 0, 0]          # Le rectangle est dans le plan z=0

#     ax.plot(x_rect, y_rect, z_rect, color='black')  # Tracer le rectangle
#     # Outil en rouge
#     tool, = ax.plot([], [], [], lw=3, color='red')  # Ligne verticale en rouge

#     return line,tool,x,y,z,t, beta,gamma

# # Fonction pour initialiser l'animation (ici on efface la ligne)
# def initPlot(line):
#     line.set_data([], [])
#     line.set_3d_properties([])
#     # tool.set_data([], [])
#     # tool.set_3d_properties([])
#     return line

# # Fonction de mise à jour de l'animation : tracer la trajectoire au fur et à mesure
# def updatePlot(num,line,x,y,z):
#     #Somme les déplacements depuis le début pour obtenir la position actuelle
#     x_rel = np.cumsum(x[:num])
#     y_rel = np.cumsum(y[:num])
#     z_rel = np.cumsum(z[:num])
#     line.set_data(x_rel,y_rel)
#     line.set_3d_properties(z_rel)

#      # Calculer la position de l'outil
#     # tool_x = x[num-1]
#     # tool_y = y[num-1]
#     # tool_z_start = z[num-1]+10
#     # tool_z_end = z[num-1]
#     # OUTIL :
#     # tool_x = np.cumsum(x[:num])
#     # tool_y = np.cumsum(y[:num])
#     # tool_z = np.cumsum(z[:num])
#     # tool.set_data(tool_x,tool_y)
#     # tool.set_3d_properties(tool_z)

#     # Appliquer les rotations
#     # Direction de la ligne verticale avant rotation
#     #direction = np.array([0, 0, 1])  # Ligne verticale de (0, 0, 0) à (0, 0, 1)

#     # # Récupération des angles 
#     # angleX = beta[num]
#     # angleY = gamma[num]

#     # # Matrices de rotation
#     # R_x = np.array([[1, 0, 0],
#     #                 [0, np.cos(angleX), -np.sin(angleX)],
#     #                 [0, np.sin(angleX), np.cos(angleX)]])
    
#     # R_y = np.array([[np.cos(angleY), 0, np.sin(angleY)],
#     #                 [0, 1, 0],
#     #                 [-np.sin(angleY), 0, np.cos(angleY)]])
    
#     # # Appliquer les rotations
#     # direction_rotated = R_y @ (R_x @ direction)  # Effectuer la multiplication de matrices

#     # Calculer les points de la ligne verticale après rotation
#     # tool_z_end_rotated = tool_z_start + direction_rotated[2] * (tool_z_end - tool_z_start)
#     # tool.set_data([tool_x, tool_x*direction_rotated[0]], [tool_y, tool_y*direction_rotated[1]])
#     # tool.set_3d_properties([tool_z_start, tool_z_end_rotated])

#     return line

    # def affichage(vect_deplacement):
    #     # Création de la figure 3D
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111, projection='3d')

    #     # Création de l'animation
    #     line,tool,x,y,z,t,beta,gamma = configPlot(vect_deplacement,ax)
    #     ani = FuncAnimation(fig, updatePlot, frames=len(t), fargs=(line, x, y, z), init_func=lambda: initPlot(line), blit=False, interval=5)

    #     # Affichage de l'animation
    #     plt.show()    


# ------------------ MAIN LOOP --------------------------#

# Récupération des positions de l'outil à partir du fichier txt
coord = extraire_coord_fichier(fichierIN)
for c in coord:
    print('coordonnees :',c)








