# MultiAxisSlicing

## Description ##
Simplification de la génération de trajectoires pour la fabrication additive sur un bras robot KUKA 6 axes à partir d'un modèle 3D.
Ce projet s'interface avec l'outil S^3 Slicer avec pour but de simplifier le pre et postprocessing.


## Guide d'installation ##


## Pre-processing ##
**dossier preprocessing**
  Concaténation de fichiers txt pour fusionner 2 objets ou 2 couches par exemple lors de l'affichage
- Conversion d'un fichier STL en fichier TET avec la fonction `preprocessing(stl_path,tet_path)`
- Génération d'un fichier TXT pour l'ajout au dossier selection_file de S^3 Slicer avec `handleNodes()` (nécessite d'avoir généré un fichier TET)


## Post-processing ###
**dossier parser**
  A partir du fichier G-Code généré par S^3 Slicer, un parseur permet de transformer les instructions de déplacement en commandes pour le robot.

### Fonctionnalités implémentées ###
- Fusion des fichiers générés (trajectoires au format X,Y,Z,I,J,K notamment) avec `fusion_fichier(liste fichiers,fichier fusionné)`
- Export des coordonnées de déplacement absolues en commande robot KUKA (fonction de déplacement linRel)

![image](https://github.com/user-attachments/assets/d12dcdc0-d846-4029-bf93-29f15cd45966)


## Visualisation ##
**dossier plot**
- Affichage dans un graphique 3D des trajectoires de l'outil (X,Y,Z) + vecteur d'orientation de l'outil (I,J,K) avec la fonction `affichage(vecteur,frameskip)`
Entrée : fichier txt contenant la liste des positions successives de l'outil (buse d'impression) au format xx.xx yy.yy zz.zz ii.ii jj.jj kk.kk
- Affichage dans un graphique 3D des trajectoires de l'outil avec la fonction `affichage2(vecteur,frameskip)`

![image](https://github.com/user-attachments/assets/f5f661f5-b6dc-4fa1-9021-f8b154ccb019)


## A faire ##

