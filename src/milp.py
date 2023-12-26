import visualize
from parser import Parser
from truck import Truck
from visualize3d import *
from mip import Model, BINARY, minimize, xsum, maximize, OptimizationStatus, INTEGER, CONTINUOUS, MINIMIZE


class MilpSolver:
    def __init__(self, input_path):
        self.file_path = input_path
        self.parser = Parser(input_path)
        self.trucks = []
        self.is_sat = False
        self.solve

    @property
    def solve(self):
        print("Solving...")

        ## Solver
        # get trucks dimensions
        L, W, H = self.parser.truck_length, self.parser.truck_width, self.parser.truck_height

        # Find the minimum number of trucks needed to deliver all products and group them
        N = len(self.parser.product_list)  # Total number of products
        m = N  # Total number of trucks available (worst case), todo: needed ?
        M = 100000  # A arbitrary large number

        model = Model(sense=MINIMIZE)
        model.emphasis = 2  # focus on feasibility

        # s[i][j] = 1 if product i is assigned to the truck j, 0 otherwise
        s = [[model.add_var(var_type=BINARY) for _ in range(m)] for _ in range(N)]
        # n[j] = 1 if truck j is used, 0 otherwise
        n = [model.add_var(var_type=BINARY) for _ in range(m)]
        # p[i],q[i],r[i] = product i dimensions (length, width, height)
        p, q, r = map(list, zip(*map(lambda product: [product.length, product.width, product.height],
                                     self.parser.product_list)))

        # x[i], y[i], z[i] = product i coordinates of the bottom left corner
        x = [model.add_var(var_type=INTEGER, lb=0) for _ in range(N)]
        y = [model.add_var(var_type=INTEGER, lb=0) for _ in range(N)]
        z = [model.add_var(var_type=INTEGER, lb=0) for _ in range(N)]

        # lx[i], ly[i], lz[i] = binary variables indicating whether the length of carton i is parallel to the X-, Y-, or Z-axis.
        lx = [model.add_var(var_type=BINARY) for _ in range(N)]
        ly = [model.add_var(var_type=BINARY) for _ in range(N)]
        lz = [model.add_var(var_type=BINARY) for _ in range(N)]
        # For example, the value of l[x][i] is equal to 1 if the length of carton i is parallel to the X-axis; otherwise it is equal to 0.
        # wx[i], wy[i], wz[i] = binary variables indicating whether the width of carton i is parallel to the X-, Y-, or Z-axis.
        wx = [model.add_var(var_type=BINARY) for _ in range(N)]
        wy = [model.add_var(var_type=BINARY) for _ in range(N)]
        wz = [model.add_var(var_type=BINARY) for _ in range(N)]
        # hx[i], hy[i], hz[i] = binary variables indicating whether the height of carton i is parallel to the X-, Y-, or Z-axis.
        hx = [model.add_var(var_type=BINARY) for _ in range(N)]
        hy = [model.add_var(var_type=BINARY) for _ in range(N)]
        hz = [model.add_var(var_type=BINARY) for _ in range(N)]

        # a[i][k], b[i][k], c[i][k], d[i][k], e[i][k], f[i][k] = defined to indicate the placement of cartons relative to each other.
        # The a[i][k] is equal to 1 if box i is on the left side of carton k. Similarly, the variables b[i][k], c[i][k], d[i][k], e[i][k], f[i][k]
        # represent whether carton i is on the right of, behind, in front of, below, or above carton k, respectively.
        # These variables are needed and defined only when i < k.
        def create_list():
            list = [[0 for _ in range(N)] for _ in range(N)]
            for i in range(N):
                for k in range(N):
                    if i < k:
                        list[i][k] = model.add_var(var_type=BINARY)
            return list

        a = create_list()
        b = create_list()
        c = create_list()
        d = create_list()
        e = create_list()
        f = create_list()

        ## Objective
        # minimizes the total empty space inside the used containers
        model.objective = minimize(
            xsum(L * W * H * n[j] for j in range(m)) - xsum(p[i] * q[i] * r[i] for i in range(N)))

        ## Constraints
        # The constraints (1)-(6) ensure that cartons do not overlap each other.
        for i in range(N):
            for k in range(N):
                if i < k:
                    model += x[i] + p[i] * lx[i] + q[i] * wx[i] + r[i] * hx[i] <= x[k] + (1 - a[i][k]) * M
                    model += x[k] + p[k] * lx[k] + q[k] * wx[k] + r[k] * hx[k] <= x[i] + (1 - b[i][k]) * M
                    model += y[i] + q[i] * wy[i] + p[i] * ly[i] + r[i] * hy[i] <= y[k] + (1 - c[i][k]) * M
                    model += y[k] + q[k] * wy[k] + p[k] * ly[k] + r[k] * hy[k] <= y[i] + (1 - d[i][k]) * M
                    model += z[i] + r[i] * hz[i] + q[i] * wz[i] + p[i] * lz[i] <= z[k] + (1 - e[i][k]) * M
                    model += z[k] + r[k] * hz[k] + q[k] * wz[k] + p[k] * lz[k] <= z[i] + (1 - f[i][k]) * M

        # This check for overlap is necessary only if a pair of cartons are placed in the same truck. This is taken care of by constraint (7)
        for i in range(N):
            for k in range(N):
                for j in range(m):
                    if i >= k:
                        continue
                    model += a[i][k] + b[i][k] + c[i][k] + d[i][k] + e[i][k] + f[i][k] >= s[i][j] + s[k][j] - 1

        # Constraint (8) guarantees that each carton will be placed in exactly one truck.
        for i in range(N):
            model += xsum(s[i][j] for j in range(m)) == 1, f"constraint 8 {i}"

        # If any carton is assigned to a truck, the truck is considered used. This requirement is handled by constraint (9).
        # n[j] must be equal to 1 if a least on carton is assigned to truck j.
        for j in range(m):
            model += xsum(s[i][j] for i in range(N)) <= M * n[j], f"constraint 9 {j}"

        # Constraints (10)-(12) ensure that all the cartons placed in a truck fit within the physical dimensions of the truck.
        for i in range(N):
            for j in range(m):
                model += x[i] + p[i] * lx[i] + q[i] * wx[i] + r[i] * hx[i] <= L + (1 - s[i][j]) * M
                model += y[i] + p[i] * ly[i] + q[i] * wy[i] + r[i] * hy[i] <= W + (1 - s[i][j]) * M
                model += z[i] + p[i] * lz[i] + q[i] * wz[i] + r[i] * hz[i] <= H + (1 - s[i][j]) * M

        # box rotations are permitted, each dimension of box i must be parallel to exactly one axis (X, Y or Z) of the container within which it is placed
        # todo: optimize the model constraints because lx, ly, lz, wx, wy, wz, hx, hy, hz are dependents => we can optimize the model
        for i in range(N):
            model += lx[i] + ly[i] + lz[i] == 1
            model += wx[i] + wy[i] + wz[i] == 1
            model += hx[i] + hy[i] + hz[i] == 1
            model += lx[i] + wx[i] + hx[i] == 1
            model += ly[i] + wy[i] + hy[i] == 1
            model += lz[i] + wz[i] + hz[i] == 1

        ## Results
        result = model.optimize(max_seconds=min(N * 10, 300))  # 10 seconds per box or 300s
        self.is_sat = result == OptimizationStatus.OPTIMAL or result == OptimizationStatus.FEASIBLE

        # Create trucks by grouping products
        if not self.is_sat: return

        # Get the number of trucks used
        for j in range(m):
            if n[j].x >= 0.99:
                self.trucks.append(Truck(len(self.trucks) + 1, L, W, H))
                for i in range(N):
                    if s[i][j].x >= 0.99:
                        # todo, extract coordinate from x, y, z using lx, ly, lz, wx, wy, wz, hx, hy, hz !!
                        x0, y0, z0 = int(x[i].x), int(y[i].x), int(z[i].x)
                        x1 = x0 + int(p[i] * lx[i].x + q[i] * wx[i].x + r[i] * hx[i].x)
                        y1 = y0 + int(p[i] * ly[i].x + q[i] * wy[i].x + r[i] * hy[i].x)
                        z1 = z0 + int(p[i] * lz[i].x + q[i] * wz[i].x + r[i] * hz[i].x)
                        test = self.trucks[-1].place_product(self.parser.product_list[i], x0, y0, z0, x1, y1, z1)

                        # test = self.trucks[-1].place_product(self.parser.product_list[i], int(x[i].x), int(y[i].x), int(z[i].x), int(x[i].x + p[i]*), int(y[i].x + q[i]), int(z[i].x + r[i]))
                        print(
                            f"Placing product {self.parser.product_list[i].id} in truck {self.trucks[-1].id} : ({x0}, {y0}, {z0}) -> ({x1}, {y1}, {z1})")
                        if not test:
                            print("Error while placing product")
                            exit(1)
        print(f"Total trucks used: {len(self.trucks)}")

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