from src.parser.parser import Parser
from src.solver.classicsolver import ClassicSolver
from src.solver.milp import MilpSolver
from src.solver.milp2 import MilpSolverV2
from src.visualize3d import visualize3d

INPUT_FILE = 'test/input.sample'

parser = Parser()
results = parser.parse_file(INPUT_FILE)

# solver = ClassicSolver(results)

solver = MilpSolverV2(results)
trucks = solver.solve()

if solver.is_sat:
    visualize3d([truck.matrix for truck in trucks])
