from ..truck import Truck
from ..visualize3d import *


class ClassicSolver:
    def __init__(self, parser_results):
        self.parser = parser_results
        self.trucks = []
        self.is_sat = False

    def solve(self):
        self.trucks = [Truck(1, self.parser.truck_length, self.parser.truck_width, self.parser.truck_height)]
        self.parser.product_list.sort(key=lambda product: product.volume, reverse=True)

        for product in self.parser.product_list:
            for truck in self.trucks:
                if not truck.is_bigger_than_self(product):
                    self.is_sat = False
                    return

                if truck.can_place_product(product):
                    break
                if truck == self.trucks[-1]:
                    self.trucks.append(Truck(len(self.trucks) + 1, self.parser.truck_length, self.parser.truck_width,
                                             self.parser.truck_height))
                    self.trucks[-1].can_place_product(product)
        self.is_sat = True

        return self.trucks

    def output(self, output_path="output.txt"):
        with open(output_path, 'w') as file:
            if self.is_sat:
                file.write("SAT\n")
                for truck in self.trucks:
                    truck.output(file)
            else:
                file.write("UNSAT\n")

    def visualize(self):
        self.output("../../output.txt")

    def visualize3d(self):
        visualize3d([truck.matrix for truck in self.trucks])

    def __str__(self):
        print(f"Solver({self.file_path})")
        print("SAT" if self.is_sat else "UNSAT")
        print("Trucks:")
        for truck in self.trucks:
            print(truck)
        return ""
