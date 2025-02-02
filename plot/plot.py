# Fichier contenant l'ensemble des fonctions pour afficher des trajectoires outils + orientation de l'outil dans un rep�re 3D


import re
import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

#----------------------VARIABLES-------------------------#

# Fichier d'entr�e (coordonn�es XYZIJK)
fichierIN = 'plot\\input\\layer0.txt'

# Animation du plot : variable globale
ani = None

#------------------- FONCTIONS ------------------------#


# FONCTIONS LECTURE/ECRITURE FICHIER

def extraire_coord_fichier(fichier):
    ''' Extrait les coordonnees successives de l'effecteur
    fichier : chemin du fichier d'entree
    coord : tableau des coordonnees au format [X,Y,Z,I,J,K] '''
    coord = []

    # Ouvrir le fichier pour la lecture
    with open(fichier, 'r') as f:
        # Lire chaque ligne, d�couper par espaces, et convertir les �l�ments en float
        for ligne in f:
            coordString = ligne.strip().split()
            try:
                # Convertir les �l�ments en float
                coord.append([float(val) for val in coordString])
            except ValueError:
                print(f"Erreur de conversion dans la ligne : {ligne.strip()}")

    return coord

# FONCTIONS AFFICHAGE

def configPlot(coordonnees, ax):
    # R�cup�ration du nombre de coordonn�es � afficher
    size = len(coordonnees)
    # R�cup�ration des points de trajectoire dans l'espace
    t = np.linspace(0,100,size)  # Nombre de points � afficher
    x = [coord[0] for coord in coordonnees]
    y = [coord[1] for coord in coordonnees]
    z = [coord[2] for coord in coordonnees]
    i = [coord[3] for coord in coordonnees]
    j = [coord[4] for coord in coordonnees]
    k = [coord[5] for coord in coordonnees]

    # Configuration initiale des limites (ajust�es aux donn�es)
    # offset de +/- 2 pour que le vecteur directeur de l'outil soit dans le plot
    # ax.set_xlim(min(x)-2, max(x)+2)
    # ax.set_ylim(min(y)-2, max(y)+2)
    # ax.set_zlim(min(z)-2, max(z)+2) 
    # Conservation des proportions
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100) 

    # Configuration l�gende
    ax.set_title("Trajectoire et orientation outil")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Ligne pour la trajectoire
    line, = ax.plot([], [], [], lw=2)
    # Vecteur pour la direction de l'outil
    tool = ax.quiver([], [], [], [], [], [], color='blue')

    return line, tool, x, y, z, i, j, k, t

# Fonction pour initialiser l'animation
def initPlot(line,tool):
    line.set_data([], [])
    line.set_3d_properties([])
    return line,tool

# Fonction de mise � jour de l'animation
def updatePlot(num, line, tool, ax, x, y, z, i, j, k, frames_skip):
    # Mise � jour de la trajectoire
    line.set_data(x[:num], y[:num])
    line.set_3d_properties(z[:num])

    # Ajouter un nouveau vecteur quiver pour chaque frame
    tool = ax.quiver(x[num], y[num], z[num], i[num], j[num], k[num], color='blue')

    # Condition pour arr�ter l'animation apr�s l'affichage de la derni�re frame
    if num == (len(x)/frames_skip) - 1:
        print("Fin de trace de la trajectoire")
        ani.event_source.stop()


    return line,

def affichage(coordonnees,frames_skip):
    ''' Affichage des trajectoires XYZ et de l'orientation de l'outil IJK dans un graphique matplotlib
    coordonnees : vecteur [x,y,z,i,j,k]
    frames_skip : nombre de frames a sauter lors de l'affichage (plus rapide) '''
    # Cr�ation de la figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Configuration initiale
    line, tool, x, y, z, i, j, k, t = configPlot(coordonnees, ax)

    # Cr�ation de l'animation
    ani = FuncAnimation(
        fig, 
        updatePlot, 
        frames = range(0, len(t), frames_skip), 
        fargs=(line, tool, ax, x, y, z, i, j, k, frames_skip), 
        init_func=lambda: initPlot(line,tool), 
        blit=False, 
        interval=10,
        repeat=False
    ) 
    # frames range(start,stop,frames_skip) avec frames_skip=2 : 1 frame sur 2 affich�e
    #interval : intervalle de rafraichissment de la figure en ms
    #repeat : permet de rejouer ou non l'animation une fois qu'elle est termin�e

    # Affichage de l'animation
    plt.show()

# FONCTIONS AFFICHAGE MESH

def plot_nodes_from_file(node_file,fig_num):
    """ Lit un fichier .node et affiche les noeuds dans un graphique 3D.

    Args:
        node_file (str): Chemin vers le fichier .node. """
    # Extraire le nom du fichier sans extension pour le titre
    file_title = os.path.splitext(os.path.basename(node_file))[0]

    # Lire les donn�es du fichier
    nodes = []
    with open(node_file, 'r') as file:
        lines = file.readlines()

        # Ignorer la premi�re ligne qui contient les m�tadonn�es
        for line in lines[1:]:
            parts = line.split()
            if len(parts) >= 4:  # Assurer qu'il y a au moins ID, x, y, z
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    nodes.append((x, y, z))
                except ValueError:
                    continue  # Ignorer les lignes mal format�es
    # V�rifier si des n�uds ont �t� extraits
    if not nodes:
        print("Aucun noeud valide trouve dans le fichier.")
        return

    # Convertir les coordonn�es en listes
    x_coords, y_coords, z_coords = zip(*nodes)

    # Cr�er le graphique 3D
    fig = plt.figure(fig_num)
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x_coords, y_coords, z_coords, c='b', marker='o', label='Nodes')

    # Ajouter les labels et le titre
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(f"3D Plot des noeuds: {file_title}")

    ax.legend()
    # plot dans fonction principale pour affichage plots multiples
    #plt.show(block=False) #Affiche tout en continuant l'execution



def plot_triangles_from_files(node_file, ele_file):
    """
    Lit les fichiers .node et .ele pour afficher les triangles dans un graphique 3D.

    Args:
        node_file (str): Chemin vers le fichier .node.
        ele_file (str): Chemin vers le fichier .ele.
    """
    # Lire les n�uds depuis le fichier .node
    nodes = []
    with open(node_file, 'r') as file:
        lines = file.readlines()

        for line in lines[1:]:  # Ignorer la premi�re ligne qui contient les m�tadonn�es
            parts = line.split()
            if len(parts) >= 4:
                try:
                    x, y, z = float(parts[1]), float(parts[2]), float(parts[3])
                    nodes.append((x, y, z))
                except ValueError:
                    continue

    # Lire les triangles depuis le fichier .ele
    triangles = []
    with open(ele_file, 'r') as file:
        lines = file.readlines()

        for line in lines[1:]:  # Ignorer la premi�re ligne qui contient les m�tadonn�es
                parts = line.split()
                if len(parts) >= 4:
                    try:
                        # Les trois derniers nombres sont les indices des n�uds
                        v1, v2, v3 = int(parts[1]), int(parts[2]), int(parts[3])
                        triangles.append((v1, v2, v3))
                    except ValueError:
                        continue

    # Cr�er le graphique 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Afficher les triangles
    for triangle in triangles:
        x = [nodes[triangle[0]][0], nodes[triangle[1]][0], nodes[triangle[2]][0], nodes[triangle[0]][0]]
        y = [nodes[triangle[0]][1], nodes[triangle[1]][1], nodes[triangle[2]][1], nodes[triangle[0]][1]]
        z = [nodes[triangle[0]][2], nodes[triangle[1]][2], nodes[triangle[2]][2], nodes[triangle[0]][2]]
        ax.plot(x, y, z, c='r')

    # Ajouter les labels et le titre
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title("3D Plot des triangles")


# FONCTIONS AFFICHAGE XYZ

def configPlot2(coordonnees, ax):
    # R�cup�ration du nombre de coordonn�es � afficher
    size = len(coordonnees)
    # R�cup�ration des points de trajectoire dans l'espace
    t = np.linspace(0,100,size)  # Nombre de points � afficher
    x = [coord[0] for coord in coordonnees]
    y = [coord[1] for coord in coordonnees]
    z = [coord[2] for coord in coordonnees]
    e = [coord[6] for coord in coordonnees] #ajout info sur E

    # Configuration initiale des limites (ajust�es aux donn�es)
    # offset de +/- 2 pour que le vecteur directeur de l'outil soit dans le plot
    # ax.set_xlim(min(x)-2, max(x)+2)
    # ax.set_ylim(min(y)-2, max(y)+2)
    # ax.set_zlim(min(z)-2, max(z)+2) 
    # Conservation des proportions
    ax.set_xlim(-100, 100)
    ax.set_ylim(-100, 100)
    ax.set_zlim(-100, 100) 

    # Configuration l�gende
    ax.set_title("Trajectoire issue du G-code")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # Ligne pour la trajectoire
    line, = ax.plot([], [], [], lw=2)

    return line, x, y, z, t

# Fonction pour initialiser l'animation
def initPlot2(line):
    line.set_data([], [])
    line.set_3d_properties([])
    return line

# Fonction de mise � jour de l'animation
def updatePlot2(num, line, ax, x, y, z, frames_skip):
    # Somme les d�placements depuis le d�but pour obtenir la position actuelle
    x_abs = np.cumsum(x[:num])
    y_abs = np.cumsum(y[:num])
    z_abs = np.cumsum(z[:num])
    # Mise � jour de la trajectoire
    line.set_data(x_abs[:num], y_abs[:num])
    line.set_3d_properties(z_abs[:num])

    # Condition pour arr�ter l'animation apr�s l'affichage de la derni�re frame
    if num == (len(x)/frames_skip) - 1:
        print("Fin de trace de la trajectoire")
        ani.event_source.stop()


    return line,

def affichage2(coordonnees,frames_skip):
    ''' Affichage des trajectoires XYZ dans un graphique matplotlib
    coordonnees : vecteur [x,y,z]
    frames_skip : nombre de frames a sauter lors de l'affichage (plus rapide) '''
    # Cr�ation de la figure 3D
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    # Configuration initiale
    line, x, y, z, t = configPlot2(coordonnees, ax)

    # Cr�ation de l'animation
    ani = FuncAnimation(
        fig, 
        updatePlot2, 
        frames = range(0, len(t), frames_skip), 
        fargs=(line, ax, x, y, z, frames_skip), 
        init_func=lambda: initPlot2(line), 
        blit=False, 
        interval=10,
        repeat=False
    ) 
    # frames range(start,stop,frames_skip) avec frames_skip=2 : 1 frame sur 2 affich�e
    #interval : intervalle de rafraichissment de la figure en ms
    #repeat : permet de rejouer ou non l'animation une fois qu'elle est termin�e

    # Affichage de l'animation
    plt.show()








