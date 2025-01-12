# MultiAxisParser

## Description ##
Simplification de la génération de trajectoires pour la fabrication additive sur un bras robot KUKA 6 axes à partir d'un modèle 3D.
Ce projet s'interface avec l'outil S^3 Slicer avec pour but de simplifier le pre et postprocessing.


## Guide d'installation ##


## Pre-processing ##
Concaténation de fichiers txt pour fusionner 2 objets ou 2 couches par exemple lors de l'affichage


## Post-processing ###
A partir du fichier G-Code généré par S^3 Slicer, un parseur permet de transformer les instructions de déplacement en commandes pour le robot.

### Fonctionnalités implémentées ###
- Passage des coordonnées absolues en coordonnées relatives
- Export des coordonnées de déplacement absolues en commande robot KUKA (fonction de déplacement linRel)

## Visualisation ##
- Affichage dans un graphique 3D des trajectoires de l'outil (X,Y,Z) + vecteur d'orientation de l'outil (I,J,K) 'affichage(vecteur,frameskip)'
Entrée : fichier txt contenant la liste des positions successives de l'outil (buse d'impression) au format xx.xx yy.yy zz.zz ii.ii jj.jj kk.kk
- Affichage dans un graphique 3D des trajectoires de l'outil 'affichage2(vecteur,frameskip)'

![image](https://github.com/user-attachments/assets/f5f661f5-b6dc-4fa1-9021-f8b154ccb019)


## A faire ##

