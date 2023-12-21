from product import Product

class Parser:
    def __init__(self, file_path):
        self.file_path = file_path

        self.truck_length = 0
        self.truck_width = 0
        self.truck_height = 0

        self.product_list = []
        self.parse_file()

    def parse_file(self):
        with open(self.file_path, 'r') as file:
            truck_dimensions = list(map(int, file.readline().split()))
            self.truck_length, self.truck_width, self.truck_height = truck_dimensions

            num_products = int(file.readline())

            for i in range(num_products):
                product_dimensions = list(map(int, file.readline().split()))
                product = Product(i + 1,*product_dimensions)
                self.product_list.append(product)

    def __str__(self):
        print(f"Truck dimensions: {self.truck_length} x {self.truck_width} x {self.truck_height}")
        print("Product list:")
        for product in self.product_list:
            print(product)
        return ""
