from MOCCO.Classes.class_input import Input
from MOCCO.Classes.class_individual import Individual


# inputId, cost, cover
inputA = Input('A', 42, {'a', 'b'})# not considered
inputB = Input('B', 98, {'b', 'c'})# neighbor with high cost
inputC = Input('C', 10, {'c', 'd'})# added
inputD = Input('D', 99, {'d', 'e'})# neighbor with high cost
inputE = Input('E', 33, {'e', 'f'})# not considered
reduce_individual = Individual([inputA, inputB, inputC, inputD, inputE])
                
neighbors = reduce_individual.get_neighbors()
reduce_considered_inputs = [inputC] + neighbors[inputC.inputId]

# inputB and inputD are removed
gain = 98 + 99
reduce_groundTruth = ([inputA, inputC, inputE], gain)
