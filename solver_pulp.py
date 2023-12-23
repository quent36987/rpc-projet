from pulp import *

# parameters
truck_size = (4, 4, 4)
objects = [(4, 2, 1), (4, 2, 1), (1, 4, 1), (3, 4, 1)]

prob = LpProblem("Optimisation_Place_Problem", LpMinimize)

# Variables
num_trucks = LpVariable("num_trucks", lowBound=0, cat=LpInteger)  # Nombre de camions utilisés

# Ajout de la contrainte pour minimiser le nombre de camions
prob += num_trucks, "Minimize_truck_count"



# Ajout d'autres contraintes et fonction objective ici...


prob.solve()

print(f"Nombre minimal de camions nécessaires : {value(num_trucks)}")
