# MultiAxisParser
Simplification du passage d'un slicing non planaire à la commande d'un robot KUKA 6 axes

## Fonctionnalités implémentées ##

Entrée : fichier txt contenant la liste des positions successives de l'outil (buse d'impression) au format xx.xx yy.yy zz.zz ii.ii jj.jj kk.kk

Affichage dans un graphique 3D des trajectoires de l'outil (X,Y,Z) + vecteur d'orientation de l'outil (I,J,K)
Concaténation de fichiers txt pour fusionner 2 objets ou 2 couches par exemple lors de l'affichage

## A faire ##

Passage des coordonnées absolues en coordonnées relatives
Export des coordonnées de déplacement absolues en commande robot KUKA
