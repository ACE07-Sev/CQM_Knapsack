import numpy as np
from dimod import ConstrainedQuadraticModel, BinaryQuadraticModel, QuadraticModel
from dwave.system import LeapHybridCQMSampler

# Objective: Maximize freight value (sum of values of the selected items).
# Constraint: Total freight weight (sum of
# weights of the selected items) must be less than or equal to the container's capacity.

num_of_items = 12
values = list(np.random.randint(1, 10, size=num_of_items))
weights = list(np.random.randint(1, 10, size=num_of_items))
weight_capacity = np.random.randint(12, 40)
print('values:', values)
print('weights:', weights)
print('weight_capacity:', weight_capacity)


def build_knapsack_cqm(costs, weights, max_weight):
    """Construct a CQM for the knapsack problem.
    Args:
        costs (array-like):
            Array of costs for the items.
        weights (array-like):
            Array of weights for the items.
        max_weight (int):
            Maximum allowable weight for the knapsack.
    Returns:
        Constrained quadratic model instance that represents the knapsack problem.
    """
    num_items = len(costs)
    print("\nBuilding a CQM for {} items.".format(str(num_items)))

    cqm = ConstrainedQuadraticModel()
    obj = BinaryQuadraticModel(vartype='BINARY')
    constraint = QuadraticModel()

    for i in range(num_items):
        # Objective is to maximize the total costs
        obj.add_variable(i)
        obj.set_linear(i, -costs[i])
        # Constraint is to keep the sum of items' weights under or equal capacity
        constraint.add_variable('BINARY', i)
        constraint.set_linear(i, weights[i])

    cqm.set_objective(obj)
    cqm.add_constraint(constraint, sense="<=", rhs=max_weight, label='capacity')

    return cqm


cqm = build_knapsack_cqm(values, weights, weight_capacity)
cqm_sampler = LeapHybridCQMSampler()
sampleset = cqm_sampler.sample_cqm(cqm, label='CQMAmirali', time_limit=6)
print(sampleset.filter(lambda d: d.is_feasible))
