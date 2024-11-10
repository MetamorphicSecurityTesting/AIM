# example of a few inputs, with an input removed because it does not cover redundant objectives, and some locally dominated inputs

from IMPRO.Classes.class_input import Input
from IMPRO.Classes.class_inputset import InputSet

# input necessary for 'aa'
cost = 42
cover = set(['aa', 'bb'])
inputA = Input('A', cost, cover)

# redundant input which does not cover an objective not covered by necessary sequences
cost = 42
cover = set(['bb'])
inputB = Input('B', cost, cover)

# inputC is locally dominated by inputD and inputE
cost = 99
cover = set(['bb', 'cc', 'dd', 'ee'])
inputC = Input('C', cost, cover)

cost = 10
cover = set(['cc', 'ee'])
inputD = Input('D', cost, cover)

cost = 12
cover = set(['dd', 'ee'])
inputE = Input('E', cost, cover)

# because 'bb' is already covered by inputA, inputG locally-dominates inputF
cost = 42
cover = set(['bb', 'ff'])
inputF = Input('F', cost, cover)

cost = 12
cover = set(['ff'])
inputG = Input('G', cost, cover)

# inputH is a duplicate of inputF when considering only the coverage objective of the redundant inputs
cost = 42
cover = set(['ff'])
inputH = Input('H', cost, cover)

# input set
inputSet2 = InputSet([inputA, inputB, inputC, inputD, inputE, inputF, inputG, inputH])

# expected results after reducing the problem
groundTruth2 = {
    'testName': "test2",
    'initial_inputs': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'],
    'necessary_inputs': {'A', 'D', 'E', 'G'},
    'removed_inputs': {'B', 'H', 'F', 'C'},
    'remaining_inputs': set(),
    'inputCoverage': {},
    'superposition': {'cc': 1, 'dd': 1, 'ee': 2, 'ff': 1},
    'redundancy': {'D': 0, 'E': 0, 'G': 0},
    'neighbors': {},
    'components': set(),
    'diagnostics': {
        'B': {'cause': 'objectives', 'inputs': ['A']},
        'C': {'cause': 'dominated', 'inputs': ['D', 'E']},
        'F': {'cause': 'dominated', 'inputs': ['G']},
        'H': {'cause': 'duplicate', 'inputs': ['F']},
    },
}
