# example of an empty input set

from IMPRO.Classes.class_input import Input
from IMPRO.Classes.class_inputset import InputSet
    
# input set
inputSet0 = InputSet([])

# expected results after reducing the problem
groundTruth0 = {
    'testName': "test0",
    'initial_inputs': [],
    'necessary_inputs': set(),
    'removed_inputs': set(),
    'remaining_inputs': set(),
    'inputCoverage': {},
    'superposition': {},
    'redundancy': {},
    'neighbors': {},
    'components': set(),
    'diagnostics': {},
}
