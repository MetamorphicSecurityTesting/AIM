# example of a few inputs, with duplicates

from IMPRO.Classes.class_input import Input
from IMPRO.Classes.class_inputset import InputSet

# inputA
cost = 20
cover = set(['aa', 'bb', 'cc'])
inputA = Input('A', cost, cover)
    
# inputB
# inputE is a duplicate of inputB
cost = 42
cover = set(['aa', 'cc', 'dd'])
inputB = Input('B', cost, cover)
inputE = Input('E', cost, cover)
    
# inputC is locally dominated by inputB
# inputD is a duplicate of inputC
cost = 60
cover = set(['dd'])
inputC = Input('C', cost, cover)
inputD = Input('D', cost, cover)
    
# input set
inputSet1 = InputSet([inputA, inputB, inputC, inputD, inputE])

# expected results after reducing the problem
groundTruth1 = {
    'testName': "test1",
    'initial_inputs': ['A', 'B', 'C', 'D', 'E'],
    'necessary_inputs': {'A', 'B'},
    'removed_inputs': {'C', 'D', 'E'},
    'remaining_inputs': set(),
    'inputCoverage': {},
    'superposition': {'dd': 1},
    'redundancy': {'B': 0},
    'neighbors': {},
    'components': set(),
    'diagnostics': {
        'C': {'cause': 'dominated', 'inputs': ['B']},
        'D': {'cause': 'duplicate', 'inputs': ['C']},
        'E': {'cause': 'duplicate', 'inputs': ['B']},
    },
}
