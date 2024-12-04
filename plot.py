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

def configPlot(coordonnees, ax):
    # Récupération des points de trajectoire dans l'espace
    t = np.linspace(0, 5, 12)  # Nombre de points à afficher
    x = [coord[0] for coord in coordonnees]
    y = [coord[1] for coord in coordonnees]
    z = [coord[2] for coord in coordonnees]
    i = [coord[3] for coord in coordonnees]
    j = [coord[4] for coord in coordonnees]
    k = [coord[5] for coord in coordonnees]

    # Configuration initiale des limites (ajustées aux données)
    # offset de +/- 2 pour que le vecteur directeur de l'outil soit dans le plot
    ax.set_xlim(min(x)-2, max(x)+2)
    ax.set_ylim(min(y)-2, max(y)+2)
    ax.set_zlim(min(z)-2, max(z)+2) 

    # Ligne pour la trajectoire
    line, = ax.plot([], [], [], lw=2)

    return line, x, y, z, i, j, k, t

# Fonction pour initialiser l'animation
def initPlot(line):
    line.set_data([], [])
    line.set_3d_properties([])
    return line,

# Fonction de mise à jour de l'animation
def updatePlot(num, line, ax, x, y, z, i, j, k):
    # Mise à jour de la trajectoire
    line.set_data(x[:num], y[:num])
    line.set_3d_properties(z[:num])

    # Ajouter un nouveau vecteur quiver pour chaque frame
    ax.quiver(x[num], y[num], z[num], i[num], j[num], k[num], color='blue')

    return line,

def affichage(coordonnees):
    # Création de la figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Configuration initiale
    line, x, y, z, i, j, k, t = configPlot(coordonnees, ax)

    # Création de l'animation
    ani = FuncAnimation(
        fig, 
        updatePlot, 
        frames=len(t), 
        fargs=(line, ax, x, y, z, i, j, k), 
        init_func=lambda: initPlot(line), 
        blit=False, 
        interval=5
    )

    # Affichage de l'animation
    plt.show()


# ------------------ MAIN LOOP --------------------------#









