from ..product import Product


class Parser:
    def __init__(self):
        self.truck_length = 0
        self.truck_width = 0
        self.truck_height = 0

        self.product_list = []

    def parse_file(self, file_path):
        with open(file_path, 'r') as file:
            truck_dimensions = list(map(int, file.readline().split()))
            self.truck_length, self.truck_width, self.truck_height = truck_dimensions

            num_products = int(file.readline())

            for i in range(num_products):
                product_dimensions = list(map(int, file.readline().split()))
                product = Product(i + 1, *product_dimensions)
                self.product_list.append(product)

        return self

    def __str__(self):
        return f"Truck : L={self.truck_length}, W={self.truck_width}, H={self.truck_height}\r\n Products: {', '.join(map(str, self.product_list))})"

    def __repr__(self):
        return f"Parser({self.truck_length}, {self.truck_width}, {self.truck_height}, [{', '.join(map(repr, self.product_list))}])"
