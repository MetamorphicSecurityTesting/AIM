from typing import Dict, Any
from IMPRO.Classes.class_inputset import InputSet

# test the output of the reduce_problem method, by comparing with values contained in the groundTruth dictionary
# if the output matches the ground truth, then the verdict is false, otherwise the failing part of the test is indicated
def run_test(inputSet: InputSet, groundTruth: Dict[str, Any], verbose = True) -> bool:
    testName = groundTruth['testName']
    # test initial inputs
    initial_inputs = [input.inputId for input in inputSet.initialInput.values()]
    if initial_inputs == groundTruth['initial_inputs']:
        verdict_initial = True
    else:
        verdict_initial = False
    # test necessary inputs
    necessary_inputs = {input.inputId for input in inputSet.necessary_inputs}
    if necessary_inputs == groundTruth['necessary_inputs']:
        verdict_necessary = True
    else:
        verdict_necessary = False
    # test removed inputs
    removed_inputs = {input.inputId for input in inputSet.removed_inputs}
    if removed_inputs == groundTruth['removed_inputs']:
        verdict_removed = True
    else:
        verdict_removed = False
    # test remaining inputs
    remaining_inputs = {input.inputId for input in inputSet.remaining_inputs}
    if remaining_inputs == groundTruth['remaining_inputs']:
        verdict_remaining = True
    else:
        verdict_remaining = False
    # test input coverage
    inputCoverage = {}
    for coverId, inputs in inputSet.inputCoverage.items():
        inputCoverage[coverId] = [input.inputId for input in inputs]
    if inputCoverage == groundTruth['inputCoverage']:
        verdict_coverage = True
    else:
        verdict_coverage = False
    # test superposition
    superposition = inputSet.superposition
    if superposition == groundTruth['superposition']:
        verdict_superposition = True
    else:
        verdict_superposition = False
    # test redundancy
    redundancy = inputSet.redundancy
    if redundancy == groundTruth['redundancy']:
        verdict_redundancy = True
    else:
        verdict_redundancy = False
    # test neighbors
    neighbors = {}
    for inputId, inputs in inputSet.neighbors.items():
        neighbors[inputId] = {input.inputId for input in inputs}
    if neighbors == groundTruth['neighbors']:
        verdict_neighbors = True
    else:
        verdict_neighbors = False
    # test components
    components = {frozenset({input.inputId for input in component}) for component in inputSet.components}
    if components == groundTruth['components']:
        verdict_components = True
    else:
        verdict_components = False
    # test diagnostics
    if inputSet.diagnostics == groundTruth['diagnostics']:
        verdict_diagnostics = True
    else:
        verdict_diagnostics = False
    # final verdict and verbose
    verdict_final = verdict_initial and verdict_necessary and verdict_removed and verdict_remaining and verdict_coverage and verdict_superposition and verdict_redundancy and verdict_neighbors and verdict_components and verdict_diagnostics
    if verbose == True:
        if verdict_initial == False:
            print(testName, "failed because of initial inputs")
        if verdict_necessary == False:
            print(testName, "failed because of necessary inputs")
        if verdict_removed == False:
            print(testName, "failed because of removed inputs")
        if verdict_remaining == False:
            print(testName, "failed because of remaining inputs")
        if verdict_coverage == False:
            print(testName, "failed because of input coverage")
        if verdict_superposition == False:
            print(testName, "failed because of superposition")
        if verdict_redundancy == False:
            print(testName, "failed because of redundancy")
        if verdict_neighbors == False:
            print(testName, "failed because of neighbors")
        if verdict_components == False:
            print(testName, "failed because of components")
        if verdict_diagnostics == False:
            print(testName, "failed because of diagnostics")
        if verdict_final == True:
            print(testName, "passed")
    return verdict_final
