# Projet RPC

## Description

Vous êtes responsable de la logistique au Service d′Acheminement National dédié au Trans-
port d′Articles de la Compagnie Logistique Aérienne Ultra Spéciale. Vous disposez de plusieurs
véhicules spécialisés (Technologies de Roulage Avancées, Innovantes et Novatrices pour En-
gins Autonomes Urbains) de capacités différentes et d′une liste d′articles à livrer à différentes
adresses. Votre objectif est d′optimiser la répartition des colis dans les véhicules pour minimiser
le nombre de véhicules utilisés tout en respectant les capacités de charge maximale de chaque
véhicules.

La description complète du projet est disponible sur
Moodle [sujet.pdf](https://moodle.epita.fr/mod/resource/view.php?id=41270).

## Utilisation des solveurs ?

### ETAPE 1 : les products ?

2 possibilités :
- remplir le fichier input.sample dans test/ avec les produits à livrer
- générer un fichier input.sample avec la fonction generate_products() dans test/generate.py

`````python
INPUT_FILE = 'test/input.sample'
`````

### ETAPE 2 : le solveur ?

Vous pouvez choisir le solver dans main.py, par défaut c'est le solver de base qui est utilisé. (recherche local)

`````python
# CHOOSE YOUR SOLVER :
solver = ClassicSolver(results)
# solver = MilpSolverV2(results)
`````

### ETAPE 3 : lets go !

Lancer le main.py et le tour est joué !
