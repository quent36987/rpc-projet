from src.parser.parser import Parser
from src.solver.classicsolver import ClassicSolver
from src.solver.milp import MilpSolver
from src.solver.milp2 import MilpSolverV2
from src.solver.milpprio import MilpSolverPriority
from src.visualize3d import visualize3d
import time

INPUT_FILE = 'test/input.sample'

parser = Parser()
results = parser.parse_file(INPUT_FILE)

# CHOOSE YOUR SOLVER :
solver = ClassicSolver(results)
# solver = MilpSolverV2(results)

start = time.time()
trucks = solver.solve()
end = time.time()

if not solver.is_sat:
    exit(0)

print(f"Time: {round(end - start, 2)}s")
# Map content of a truc to list of volume
print(f"Total volume of trucks used: {len(trucks)}")
visualize3d([truck.matrix for truck in trucks])
