# example of a few inputs with several overlapping components

from IMPRO.Classes.class_input import Input
from IMPRO.Classes.class_inputset import InputSet

# first component
cost = 12
cover = set(['aa', 'bb'])
inputA = Input('A', cost, cover)

cost = 13
cover = set(['bb', 'cc'])
inputB = Input('B', cost, cover)

cost = 14
cover = set(['aa', 'cc'])
inputC = Input('C', cost, cover)

# second component
cost = 12
cover = set(['dd', 'ee'])
inputD = Input('D', cost, cover)

cost = 13
cover = set(['ee', 'ff'])
inputE = Input('E', cost, cover)

cost = 14
cover = set(['ff', 'gg'])
inputF = Input('F', cost, cover)

cost = 15
cover = set(['dd', 'gg'])
inputG = Input('G', cost, cover)

# necessary input
cost = 12
cover = set(['hh'])
inputH = Input('H', cost, cover)
inputI = Input('I', cost, cover)# is a duplicate

# inputJ is locally-dominated by inputA and inputH
cost = 60
cover = set(['aa', 'hh'])
inputJ = Input('J', cost, cover)

# input set
inputSet3 = InputSet([inputA, inputB, inputC, inputD, inputE, inputF, inputG, inputH, inputI, inputJ])

# expected results after reducing the problem
groundTruth3 = {
    'testName': "test3",
    'initial_inputs': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'],
    'necessary_inputs': {'H'},
    'removed_inputs': {'I', 'J'},
    'remaining_inputs': {'A', 'B', 'C', 'D', 'E', 'F', 'G'},
    'inputCoverage': {'aa': ['A', 'C'], 'bb': ['A', 'B'], 'cc': ['B', 'C'], 'dd': ['D', 'G'], 'ee': ['D', 'E'], 'ff': ['E', 'F'], 'gg': ['F', 'G']},
    'superposition': {'aa': 2, 'bb': 2, 'cc': 2, 'dd': 2, 'ee': 2, 'ff': 2, 'gg': 2, 'hh': 1},
    'redundancy': {'A': 1, 'B': 1, 'C': 1, 'D': 1, 'E': 1, 'F': 1, 'G': 1, 'H': 0},
    'neighbors': {'A': {'B', 'C'}, 'B': {'A', 'C'}, 'C': {'A', 'B'}, 'D': {'G', 'E'}, 'E': {'F', 'D'}, 'F': {'G', 'E'}, 'G': {'F', 'D'}},
    'components': {frozenset({'A', 'B', 'C'}), frozenset({'D', 'E', 'F', 'G'})},
    'diagnostics': {
        'I': {'cause': 'duplicate', 'inputs': ['H']},
        'J': {'cause': 'dominated', 'inputs': ['A', 'H']},
    },
}
