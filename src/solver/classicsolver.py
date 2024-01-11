from ..truck import Truck
import math
from ..visualize3d import *

"""
@param products: list of Product
@return: int
return the minimal amount of trucks needed to store all the products
"""


def get_minimal_amount_of_trucks(products, truckLength, truckWidth, truckHeight):
    total_volume = 0
    for product in products:
        total_volume += product.volume
    return math.ceil(total_volume / (truckLength * truckWidth * truckHeight))


class ClassicSolver:
    def __init__(self, parser_results):
        self.parser = parser_results
        self.trucks = []
        self.is_sat = False

    # old solver
    # def solve(self):
    #     self.trucks = [Truck(1, self.parser.truck_length, self.parser.truck_width, self.parser.truck_height)]
    #     self.parser.product_list.sort(key=lambda product: product.volume, reverse=True)
    #
    #     for product in self.parser.product_list:
    #         for truck in self.trucks:
    #             if not truck.is_bigger_than_self(product):
    #                 self.is_sat = False
    #                 return
    #
    #             if truck.can_place_product(product):
    #                 break
    #             if truck == self.trucks[-1]:
    #                 self.trucks.append(Truck(len(self.trucks) + 1, self.parser.truck_length, self.parser.truck_width,
    #                                          self.parser.truck_height))
    #                 self.trucks[-1].can_place_product(product)
    #                 break
    #     self.is_sat = True
    #
    #     return self.trucks

    def solve(self):
        minimal_trucks_count = get_minimal_amount_of_trucks(self.parser.product_list, self.parser.truck_length,
                                                            self.parser.truck_width, self.parser.truck_height)
        trucks = []

        for i in range(minimal_trucks_count):
            trucks.append(Truck(i + 1, self.parser.truck_length, self.parser.truck_width, self.parser.truck_height))

        products = self.parser.product_list
        products.sort(key=lambda product: product.volume, reverse=True)

        # for product in products:
        #     if trucks[-1].is_bigger_than_self(product):
        #         self.is_sat = False
        #         print("not sat: product is bigger than truck, product: ", product)
        #         return []

        res = self._solve(trucks, products, 0, minimal_trucks_count)
        self.is_sat = True

        return res

    def _solve(self, trucks, products, idx, min_trucks_count):
        if idx == len(products):
            return trucks

        for truck in trucks:
            placements = truck.placements(products[idx])

            for placement in placements:
                x1, y1, z1, x2, y2, z2 = placement
                truck.place_product(products[idx], x1, y1, z1, x2, y2, z2)
                visualize3d([truck.matrix for truck in trucks])
                res = self._solve(trucks, products, idx + 1, min_trucks_count)

                if len(res) == min_trucks_count:
                    return res

                truck.remove_product(products[idx], placement)

            if len(placements) > 0:
                return []

            if len(placements) == 0 and truck == trucks[-1]:
                return []

        return trucks

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
