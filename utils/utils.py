# Fichier contenant des méthodes utilitaires utilisées par le programme principal

import os

def fusion_fichiers(fichiers, sortie):
    '''Fusionne plusieurs fichiers txt en un seul en ajoutant leur contenu a la suite
    fichiers : liste des chemins des fichiers a fusionner
    sortie : chemin du fichier fusionne '''
    with open(sortie, 'w') as f_sortie:
        for fichier in fichiers:
            with open(fichier, 'r') as f_entree:
                # Lire le contenu du fichier et l'écrire dans le fichier de sortie
                f_sortie.write(f_entree.read())
                f_sortie.write("\n")  # Ajoute une nouvelle ligne entre chaque fichier (facultatif)
    print("Fusion fichiers terminee")
