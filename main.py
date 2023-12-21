from camion import Camion
from produit import Produit

my_produit = Produit(2, 1, 3)

my_camion = Camion(4, 4, 4)

my_camion.placer_produit(my_produit, 0, 0, 0, 2, 1, 3)

print(my_camion)

