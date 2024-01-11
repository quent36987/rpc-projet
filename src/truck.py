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
                        print(f"Error: product {product.id} overlaps with product {self.matrix[x][y][z]} in the truck {self.id}"),
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


    # return a list of possible placements for a product
    # return type [(x1, y1, z1, x2, y2, z2),...]
    def placements(self, product):
        placements = []
        for x1 in range(0, self.length):
            for y1 in range(0, self.width):
                for z1 in range(0, self.height):
                    if self.matrix[x1][y1][z1] == 0:
                        if x1 + product.width <= self.length and y1 + product.height <= self.width and z1 + product.length <= self.height:
                            for x2 in range(x1, x1 + product.width):
                                for y2 in range(y1, y1 + product.height):
                                    for z2 in range(z1, z1 + product.length):
                                        if self.matrix[x2][y2][z2] != 0:
                                            break
                                    else:
                                        continue
                                    break
                                else:
                                    continue
                                break
                            else:
                                placements.append((x1, y1, z1, x1 + product.width, y1 + product.height, z1 + product.length))
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
        Search for the first available place in the truck and place the product if it fits, otherwise keep searching and if there is no place return False
    '''

    def can_place_product(self, product):
        for x2 in range(0, self.width):
            for y2 in range(0, self.height):
                for z2 in range(0, self.length):
                    if self.matrix[x2][y2][z2] == 0:
                        if x2 + product.width <= self.width and y2 + product.height <= self.height and z2 + product.length <= self.length:
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
