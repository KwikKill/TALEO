# Student project for TALEO classes

By Kwikkill / Ouisk / Zalen / Lepan

## Main goal :

Identify the more accurate document to show with a browser-style query

## Notes took during the project presentation :

Notes Projet Taleo

Indexation : On recherche à quel point un mot est caractéristique d'un fichier :
- TF : Term frequency -> Plus fréquent : plus de poids (Ex : "Zoo" / Contre exemple "le")
- IDF : Invers Term Frequency -> Moins fréquent moins de poids -> Moins présent en général = plus caractéristique

Création d'un fichier inversé

Doc 1 -> Mot1 : 0.5, Mot2 : 0.8 etc etc

Mot1 -> Doc1 : 0.5, Doc2 : 0.6 etc etc

But : Trouver un équilibre entre précision et rappel via la Fmesure (meilleur compromis) -> Script fourni pour ce calcul

Penser à mettre tous les noms au masculin singulier, tous les verbes a l'infinitif -> lématisation
Ca permets d'améliorer la répartition des mots ainsi que trouver si on cherche "zoo" les termes "zoos"

Attention : Si on cherche Jacques Chirac il faut trouver Jacques Chirac, et pas un fichier dans lequel il y aurait JacquesDupont, et Bernadette Chirac, sans Jacques Chirac !
-> Association de mots dans la même entité, Jacques et Chirac vont souvent de pair, à mettre en avant

On fait un produit scalaire normaliser (cosinus) afin de ne pas avantager les documents long par rapports au document court (ou l'inverse)

Langage au choix (python c'est pas mal quand même.)

Binome ou trinome

Chill en terme de code


Notation : Ce projet est noté, une partie de la note compte pour l'option (DS d'1h en Mai en plus)
Il y a un concours entre les algo qui compte pour une partie de la note du projet, le meilleur algo a la meilleure note etc etc
