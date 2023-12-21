from Truck import Truck
from product import Product
from parser import Parser

chemin_fichier = 'input.sample'
parser = Parser(chemin_fichier)
# print(parser)

truck = Truck(1,parser.truck_length, parser.truck_width, parser.truck_height)
truck.place_product(parser.product_list[0], 0, 0, 0, 1, 2, 3)
print(truck)

truck.output()
truck.visualize()


