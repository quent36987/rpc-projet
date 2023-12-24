import visualize
from parser import Parser
from truck import Truck
from visualize3d import *
from mip import Model, BINARY, minimize, xsum, maximize, OptimizationStatus


class MilpSolver:
    def __init__(self, input_path):
        self.file_path = input_path
        self.parser = Parser(input_path)
        self.trucks = []
        self.is_sat = False
        self.solve()

    def solve(self):
        print("Solving...")

        ## Solver
        # Find the minimum number of trucks needed to deliver all products and group them
        # get trucks dimensions
        L, W, H = self.parser.truck_length, self.parser.truck_width, self.parser.truck_height
        n = len(self.parser.product_list)  # number of products
        # Map product list to lists of their lengths, list of their widths, list of their heights, list of their delivery_priority, list of volumes
        L2, W2, H2, D2, V2 = map(list, zip(*map(
            lambda product: [product.length, product.width, product.height, product.delivery_priority, product.volume],
            self.parser.product_list)))
        I = set(range(n))

        m = Model()

        # x[i][j] = 1 if product i is assigned to the same truck as product j
        x = [[m.add_var(var_type=BINARY) for _ in I] for _ in I]

        # The objective is to minimize the number of trucks used
        m.objective = maximize(xsum(x[i][j] for i in I for j in I))

        ## Constraints
        # Each item must be assigned to exactly one truck
        for i in I:
            m += xsum(x[i][j] for j in I) == 1

        # Each truck must be filled with items that fit in it
        for i in I:
            m += xsum(V2[j] * x[i][j] for j in I) <= L * W * H

        result = m.optimize()
        self.is_sat = result == OptimizationStatus.OPTIMAL

        # Create trucks by grouping products
        if not self.is_sat: return

        trucks = []
        for i in I:
            for j in I:
                if x[i][j].x >= 0.99:
                    # We have no trucks yet
                    if len(trucks) == 0:
                        trucks.append([i, j])

                    # Get the truck that contains product i and add j to it or vice versa
                    added = False
                    for truck in trucks:
                        if i in truck:
                            truck.append(j)
                            added = True
                            break
                        if j in truck:
                            truck.append(i)
                            added = True
                            break
                    if not added:  # Create a new truck if product i and j are not in any truck
                        trucks.append([i, j])

        print(f"Found {len(trucks)} trucks")
        # Now we have our trucks groups, we can create truck objects
        for truck in trucks:
            truck_products = [self.parser.product_list[i] for i in truck]
            self.trucks.append(Truck(len(self.trucks) + 1, L, W, H))
            for product in truck_products:
                self.trucks[-1].can_place_product(product)
        # End solver

    def output(self, output_path="output.txt"):
        with open(output_path, 'w') as file:
            if self.is_sat:
                file.write("SAT\n")
                for truck in self.trucks:
                    truck.output(file)
            else:
                file.write("UNSAT\n")

    def visualize(self):
        self.output("../output.txt")
        with open("../output.txt", 'r') as file:
            visualize.visualizeTruck(file, 1)

    def visualize3d(self):
        visualize3d([truck.matrix for truck in self.trucks])

    def __str__(self):
        print(f"Solver({self.file_path})")
        print("SAT" if self.is_sat else "UNSAT")
        print("Trucks:")
        for truck in self.trucks:
            print(truck)
        return ""
