from .visualize3d import *
import sys


class Truck:
    def __init__(self, id, length, width, height):
        self.id = id
        self.length = length  # == x
        self.width = width  # == y
        self.height = height  # == z
        self.matrix = [[[0 for _ in range(height)] for _ in range(width)] for _ in range(length)]
        self.products = []

    def place_product(self, product, x1, y1, z1, x2, y2, z2):
        """
            Places a product in the truck
            :param z2:
            :param y2:
            :param x2:
            :param z1:
            :param y1:
            :param x1:
            :param product: the product to place
            :return:  true if the product was placed, false otherwise
        """
        # Preconditions
        if x2 > self.length or y2 > self.width or z2 > self.height:
            print(f"Error: product {product.id} is out of bounds of the truck {self.id}", file=sys.stderr)
            return False
        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    if self.matrix[x][y][z] != 0:
                        print(
                            f"Error: product {product.id} overlaps with product "
                            f"{self.matrix[x][y][z]} in the truck {self.id}"),
                        return False

        # Actual placing
        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    self.matrix[x][y][z] = product.id
        self.products.append((product, [x1, y1, z1, x2, y2, z2]))
        return True

    def remove_product(self, product, coordinates):
        x1, y1, z1, x2, y2, z2 = coordinates
        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    self.matrix[x][y][z] = 0

        self.products.remove((product, [x1, y1, z1, x2, y2, z2]))

    def is_fitting_in(self, x1, y1, z1, x2, y2, z2):
        """
            Check if a product is fitting in a given spot
            :return:  true if the product fits in the given spot, false otherwise
        """
        # Preconditions
        if x2 > self.length or y2 > self.width or z2 > self.height:
            return False
        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    if self.matrix[x][y][z] != 0:
                        return False
        return True

    # return a list of possible placements for a product
    # return type [(x1, y1, z1, x2, y2, z2),...]
    # parcourir le niveau le plus au fond du camion (en 2D)
    # for un for sur x et y
    # pour toutes les cases libres, on tente de placer le colis dans tous les positions
    # si on trouve des positions libres on renvoie les resultats, sinon on avance d'un cran et on recommence
    def placements(self, product):
        placements = []
        for z in range(self.height):
            for x in range(self.length):
                for y in range(self.width):
                    if self.matrix[x][y][0] == 0:
                        po1 = (product.width, product.height, product.length)
                        po2 = (product.width, product.length, product.height)
                        po3 = (product.height, product.width, product.length)
                        po4 = (product.height, product.length, product.width)
                        po5 = (product.length, product.width, product.height)
                        po6 = (product.length, product.height, product.width)
                        pos = {po1, po2, po3, po4, po5, po6}
                        for po in pos:
                            if self.is_fitting_in(x, y, z, x + po[0], y + po[1], z + po[2]):
                                placements.append((x, y, z, x + po[0], y + po[1], z + po[2]))
            if len(placements) > 0:
                return placements

    def is_bigger_than_self(self, product):
        product_dimensions = [product.length, product.width, product.height]
        truck_dimensions = [self.length, self.width, self.height]

        for i in range(3):
            for j in range(3):
                if i != j:
                    if all(product_dimensions[k] <= truck_dimensions[k] for k in range(3)):
                        return True
                    product_dimensions[i], product_dimensions[j] = product_dimensions[j], product_dimensions[i]
        return False

    def output(self, output_path):
        for product, coordinates in self.products:
            output_path.write(f"{self.id} {' '.join(map(str, coordinates))}\n")

    '''
        @param product: Product
        @param x: int
        @param y: int
        @param z: int
        @return: bool
        Search for the first available place in the truck and place the product if it fits,
        otherwise keep searching and if there is no place return False
    '''

    def can_place_product(self, product):
        for x2 in range(0, self.width):
            for y2 in range(0, self.height):
                for z2 in range(0, self.length):
                    if self.matrix[x2][y2][z2] == 0:
                        if (x2 + product.width <= self.width and y2 + product.height <= self.height
                                and z2 + product.length <= self.length):
                            for x3 in range(x2, x2 + product.width):
                                for y3 in range(y2, y2 + product.height):
                                    for z3 in range(z2, z2 + product.length):
                                        if self.matrix[x3][y3][z3] != 0:
                                            break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break
                            else:
                                self.place_product(product, x2, y2, z2, x2 + product.width, y2 + product.height,
                                                   z2 + product.length)
                                return True
        return False

    def __str__(self):
        for z in range(self.height):
            for y in range(self.width):
                for x in range(self.length):
                    print(self.matrix[x][y][z], end=" ")
                print()
            print()
        return f"Truck({self.length}, {self.width}, {self.height})"

    def visualize(self):
        with open("../output.txt", 'w') as file:
            file.write("SAT\n")
            for product, coordinates in self.products:
                file.write(f"{self.id} {' '.join(map(str, coordinates))}\n")

    def visualize3D(self):
        visualize3d(self.matrix)

