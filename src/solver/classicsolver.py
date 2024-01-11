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
                    break
        self.is_sat = True

        return self.trucks

    def solverV2(self):
        trucks = [Truck(1, self.parser.truck_length, self.parser.truck_width, self.parser.truck_height)]
        products = self.parser.product_list
        products.sort(key=lambda product: product.volume, reverse=True)

        # FIXME verify if a product is bigger than the truck

    

        res = self._solverV2(trucks, products, 0, len(products))
        print("count", len(res),res)
        self.is_sat = True
        return res

    def _solverV2(self, trucks, products, idx, min_trucks_count):
        # on cherche tt les position pour placer le produit dans le premier camion


        print(idx)
        if len(trucks) > min_trucks_count:
            print("return to big :( ", len(trucks), min_trucks_count)
            return trucks
        solve_count = min_trucks_count
        res = []
        if idx == len(products):
            return trucks

        for truck in trucks:
            placements = truck.placements(products[idx])
            print("product", products[idx], "nb placements", len(placements), "nb trucks", len(trucks), placements)

            for placement in placements:
                x1, y1, z1, x2, y2, z2 = placement
                truck.place_product(products[idx], x1, y1, z1, x2, y2, z2)
                visualize3d([truck.matrix for truck in trucks])
                res = self._solverV2(trucks, products, idx + 1, solve_count)
                if len(res) < solve_count:
                    solve_count = len(res)
                    res = trucks

                print("solve_count", solve_count)
                truck.remove_product(products[idx], placement)

            if len(placement) > 0:
                break


            if truck == trucks[-1]:
                trucks.append(Truck(len(trucks) + 1, self.parser.truck_length, self.parser.truck_width,
                                    self.parser.truck_height))

                placements = trucks[-1].placements(products[idx])
                for placement in placements:
                    x1, y1, z1, x2, y2, z2 = placement
                    trucks[-1].place_product(products[idx], x1, y1, z1, x2, y2, z2)
                    res = self._solverV2(trucks, products, idx + 1)
                    if len(res) < solve_count:
                        solve_count = len(res)
                        res = trucks


                    trucks[-1].remove_product(products[idx], placement)
                break

        return res

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
