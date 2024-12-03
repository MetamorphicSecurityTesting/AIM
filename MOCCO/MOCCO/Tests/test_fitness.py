from MOCCO.Classes.class_input import Input
from MOCCO.Classes.class_individual import Individual
from MOCCO.Classes.class_misers import Misers


# inputId, cost, cover
inputA = Input('A', 4, {'a', 'b'})
inputB = Input('B', 5, {'b', 'c'})
inputC = Input('C', 6, {'b', 'c', 'd'})
inputD = Input('D', 6, {'a', 'b', 'c', 'd'})
inputE = Input('E', 3, {'e'})

initial_individual = Individual([inputA, inputB, inputC, inputD, inputE])
initial_inputCoverage = initial_individual.inputCoverage
objectives = list(initial_inputCoverage.keys())
objectives.sort()
misers = Misers(initial_inputCoverage, objectives)
fitness_miser = misers._init_miser([inputA, inputB])

fitness_groundTruth = [0.9, 0.0, 0.0, 0.0, 0.1, 1.0]
