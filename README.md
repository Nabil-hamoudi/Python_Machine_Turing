## Prérequis

Python Version: 3.11, avec module Tkinter

# Fonctionnement Projet machine turing

Pour lancer une nouvelle instance de machine de turing il suffit de lancer le fichier python `interface_graphique.py`, d'ici vous pouvez importer votre
machine de turing préalablement écrite suivant les régles d'écriture `(section: Formatage fichier)` en appuyant sur le bouton 'import a machine'
et entrée un mot dans l'espace a gauche du bouton start.
Au moment du lancement de `interface_graphique.py` vous pouvez spécifier `--opti` suivi de True ou False pour activer les optimisation de machine de turing tel que:

    `python3.11 interface_graphique --opti {True, False}`

Il est aussi possible de lancer une instance a partir du code python `turing_machine.py` avec une commande sous la forme:

    `python3.11 turing_machine.py example.txt mot_entree [OPTIONAL: --opti {True, False}]`

## Formatage fichier machine turing

Un fichier machine de turing est un fichier texte suivant les normes de formatage du site `https://turingmachinesimulator.com/`
avec des ajout des importation de machine de turing pour plus de détail referez vous au fichier `EXEMPLE_SEARCH.txt` qui donne
une description complete de ceux ci.
