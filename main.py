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

if not solver.is_sat:
    exit(0)

# Map content of a truc to list of volume
print(f"Total volume of boxes used: {sum([map(lambda p: p.volume, truck.products) for truck in trucks])}")
visualize3d([truck.matrix for truck in trucks])
