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
    print("Fusion fichiers terminee")


def listesIdentiques(liste1,liste2):
    ''' Fonction de comparaison de listes de nombre reels ou entiers
    liste 1 : 1ere liste a verifier
    liste 2 : 2eme liste a verifier
    return : false si les 2 listes ont au moins une case differente
    return : true si les 2 listes contiennent les memes elements '''
    identique = True
    for i in range(0,len(liste1)):
        if(liste1[i]!=liste2[i]):
            identique = False
            break
    return identique 