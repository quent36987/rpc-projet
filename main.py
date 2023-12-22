from Truck import Truck
from product import Product
from parser import Parser

chemin_fichier = 'input.sample'
parser = Parser(chemin_fichier)
# print(parser)

truck = Truck(1,parser.truck_length, parser.truck_width, parser.truck_height)
print("avalaible space :")
print(truck.available_space())

print("biggest spot available :")
print(truck.biggest_available_space())

print("place first product :")
print(truck.can_place_product(parser.product_list[0]))
print(truck)

print("can place product : (second product)")
print(truck.can_place_product(parser.product_list[1]))
#
print("can place product : (third product)")
print(truck.can_place_product(parser.product_list[2]))

print("can place product : (forth product)")
print(truck.can_place_product(parser.product_list[3]))

print("can place product : (fifth product)")
print(truck.can_place_product(parser.product_list[4]))

print("can place product : (sixth product)")
print(truck.can_place_product(parser.product_list[5]))

print("can place product : (seventh product)")
print(truck.can_place_product(parser.product_list[6]))

print("can place product : (eighth product)")
print(truck.can_place_product(parser.product_list[7]))



#truck.place_product(parser.product_list[0], 0, 0, 0, 1, 2, 3)
print(truck)

truck.output()
truck.visualize()


