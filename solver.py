import visualize
from product import Product
from parser import Parser
from Truck import Truck
from visualize import visualize


class Solver:
    def __init__(self, input_path):
        self.file_path = input_path
        self.parser = Parser(input_path)
        self.trucks = [Truck(1, self.parser.truck_length, self.parser.truck_width, self.parser.truck_height)]
        self.is_sat = False
        self.solve()

    def solve(self):
        # FIXME: tres moche
        self.parser.product_list.sort(key=lambda product: product.volume, reverse=True)

        for product in self.parser.product_list:
            for truck in self.trucks:
                if not truck.is_bigger_than(product):
                    self.is_sat = False
                    return

                if truck.can_place_product(product):
                    break

            self.trucks.append(Truck(len(self.trucks) + 1, self.parser.truck_length, self.parser.truck_width,
                                     self.parser.truck_height))
            self.trucks[-1].can_place_product(product)
        self.is_sat = True

    def output(self, output_path="output.txt"):
        with open(output_path, 'w') as file:
            if self.is_sat:
                file.write("SAT\n")
                for truck in self.trucks:
                    # FIXME: truck.output(file)
                    truck.output(output_path)
            else:
                file.write("UNSAT\n")

    def visualize(self):
        self.output("output.txt")
        visualize.visualize("output.txt")

    def __str__(self):
        print(f"Solver({self.file_path})")
        print("SAT" if self.is_sat else "UNSAT")
        print("Trucks:")
        for truck in self.trucks:
            print(truck)
        return ""
