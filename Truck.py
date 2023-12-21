class Truck:
    def __init__(self, length, width, height):
        self.length = length
        self.width = width
        self.height = height
        self.matrix = [[[0 for _ in range(height)] for _ in range(width)] for _ in range(length)]
        self.products = []

    def place_product(self, product, x1, y1, z1, x2, y2, z2):
        length = len(self.products) + 1
        for x in range(x1, x2):
            for y in range(y1, y2):
                for z in range(z1, z2):
                    self.matrix[x][y][z] = length
        self.products.append(product)

    def is_bigger_than(self, product):
        product_dimensions = [product.length, product.width, product.height]
        truck_dimensions = [self.length, self.width, self.height]

        for i in range(3):
            for j in range(3):
                if i != j:
                    if all(product_dimensions[k] <= truck_dimensions[k] for k in range(3)):
                        return True
                    product_dimensions[i], product_dimensions[j] = product_dimensions[j], product_dimensions[i]
        return False

    def __str__(self):
        for z in range(self.height):
            for y in range(self.width):
                for x in range(self.length):
                    print(self.matrix[x][y][z], end=" ")
                print()
            print()
        return f"Truck({self.length}, {self.width}, {self.height})"
