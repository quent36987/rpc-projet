from Truck import Truck
from produit import Produit
from parser import Parser

chemin_fichier = 'input.sample'
parser = Parser(chemin_fichier)
print(parser)

truck = Truck(parser.longueur_camion, parser.largeur_camion, parser.hauteur_camion)
truck.place_product(parser.liste_produits[0], 0, 0, 0, 1, 1, 1)
print(truck)




