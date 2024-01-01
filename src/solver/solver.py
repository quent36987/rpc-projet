from src.parser.parser import Parser
from src.truck import Truck

Result = list[Truck] or None

class Solver:
    def __init__(self, inputs: Parser):
        self.inputs = inputs
        self.is_sat = False

    def solve(self, max_seconds=float('inf')) -> Result:
        """
        Solve the problem according to the given inputs
        :param max_seconds:  maximum time to spend on the problem. If the time is exceeded, the solver should return. Default to INF.
        :return: the list of trucks or None if no solution was found
        """
        pass
