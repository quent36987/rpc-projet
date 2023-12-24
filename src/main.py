from mip import Model

from truck import Truck
from product import Product
from parser import Parser
from solver import Solver
from milp import MilpSolver

input = 'test/input.sample'

m = Model()

# solver = Solver(input)
solver = MilpSolver(input)

# print(solver)

# solver.visualize()
solver.visualize3d()
