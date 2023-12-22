from truck import Truck
from product import Product
from parser import Parser
from solver import Solver

input = 'input.sample'

solver = Solver(input)

print(solver)

solver.visualize()
solver.visualize3d()


