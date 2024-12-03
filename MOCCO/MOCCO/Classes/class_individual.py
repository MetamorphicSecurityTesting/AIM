from typing import List, Set, Dict, Tuple, Optional, Any
from MOCCO.Functions.selection import select
from .class_input import Input, InputId, CoverId

# This class defines attributes and methods for individuals that can be either in the roofer or the miser population.
class Individual:

    # ---- INITIALIZATION AND REPRESENTATION ----
    
    def __init__(self, inputs: List[Input], verbose: Optional[bool] = False):
        self.verbose = verbose
        if self.verbose:
            print("initialize individual")
        # check that each input identifier is unique
        self._check_inputs(inputs)
        self.inputs = inputs
        # compute input coverage
        self.inputCoverage = self._init_inputCoverage()
    
    def __repr__(self):
        repr = f"<Individual (id {id(self)}): "
        # inputs
        inputs = [input.inputId for input in self.inputs]
        repr += f"inputs = {inputs}"
#        # coverage
#        inputCoverage = {}
#        for coverId, inputs in self.inputCoverage.items():
#            inputCoverage[coverId] = [input.inputId for input in inputs]
#        repr += f", inputCoverage = {inputCoverage}"
        # end of representation
        repr += f">"
        return repr
    
    # check that each input identifier is unique
    def _check_inputs(self, inputs: List[Input]):
        inputIds = []
        for input in inputs:
            inputId = input.inputId
            if inputId in inputIds:
                raise ValueError("An input identifier should be unique.")
            else:
                inputIds.append(inputId)
        if self.verbose:
            print("_check_inputs passed")
    
    # inputCoverage is a dictionary: CoverId -> List[Input] mapping each objective to the inputs covering this objective
    def _init_inputCoverage(self) -> Dict[CoverId, List[Input]]:
        inputCoverage = {}
        for input in self.inputs:
            for coverId in input.cover:
                if coverId not in inputCoverage:
                    inputCoverage[coverId] = []
                # each input is appended only once
                inputCoverage[coverId].append(input)
        return inputCoverage

    # ---- NEIGHBORS ----
        
    # return neighbors if they were already computed, otherwise compute then return them
    def get_neighbors(self):
        try:
            return self.neighbors
        except AttributeError:
            self.neighbors = self._init_neighbors()
            return self.neighbors
                
    # neighbors is a dictionary mapping each input ID to the list of its neighbors, according to the overlapping relation: two inputs overlap if and only if they cover at least one objective in common
    def _init_neighbors(self) -> Dict[InputId, List[Input]]:
        neighbors = {}
        # initialize keys with empty neighborhood
        for input in self.inputs:
            neighbors[input.inputId] = []
        # fill neighborhoods, based on coverage
        for coverId, covering_inputs in self.inputCoverage.items():
            for i in range(0, len(covering_inputs)):
                input1 = covering_inputs[i]
                for j in range(i + 1, len(covering_inputs)):
                    input2 = covering_inputs[j]
                    # input1 and input2 are distinct
                    neighbors[input1.inputId].append(input2)
                    neighbors[input2.inputId].append(input1)
        return neighbors

    # ---- REDUCE INDIVIDUAL ----
    
    # leverage the reduce method to focus on inputs around a given input
    # ensure each considered input is in self.inputs
    def reduce_neighborhood(self, input: Input) -> Tuple[Any, int]:# should be Tuple[Self, int], available from Python 3.11
        # determine considered inputs
        if input in self.inputs:
            neighbors = self.get_neighbors()
            considered_inputs = [input] + neighbors[input.inputId]
        else:
            considered_inputs = []
        # reduction
        individual, gain = self.reduce(considered_inputs)
        return individual, gain
    
    # leverage the reduce method to focus on inputs around a given edge
    # ensure each considered input is in self.inputs
    def reduce_edge(self, edge: Set[Input]) -> Tuple[Any, int]:# should be Tuple[Self, int], available from Python 3.11
        # determine considered inputs
        self_edge = edge & set(self.inputs)
        if len(self_edge) > 0:
            neighbors = self.get_neighbors()
        considered_inputs = set(self_edge)# copy
        for input in self_edge:
            considered_inputs |= set(neighbors[input.inputId])
        # for the reduce method, the considered inputs are in a list
        considered_inputs = list(considered_inputs)
        individual, gain = self.reduce(considered_inputs)
        return individual, gain
        
    # self_considered_inputs is a list of inputs in self.inputs, it is used for the sake of performance to restrict the computations to some and not all inputs
    # compute the reduced individual, after removal steps, and the corresponding gain
    # assume each considered input is in self.inputs
    def reduce(self, self_considered_inputs: List[Input]) -> Tuple[Any, int]:# should be Tuple[Self, int], available from Python 3.11
        # we save intermediate computations in a tuple to not compute them again
        # each candidate is represented by a tuple (removal_steps, current_individual, considered_inputs, redundant_inputs, gain), where
        #   - removal_steps is the list of the inputs which were removed so far
        #   - current_individual is the individual obtained after these removal steps
        #   - considered_inputs is the list of the considered inputs, minus the inputs that were removed so far
        #   - redundant_inputs is the list of the inputs that are still redundant in this individual
        #   - gain is the sum of the cost of the inputs that were removed so far
        # initialize candidates
        self_redundant_inputs = self._get_redundant_inputs(self_considered_inputs)
        candidates = [([], self, self_considered_inputs, self_redundant_inputs, 0)]
        best_gain = 0
        # compute candidates using canonical order
        for removal_input in self_redundant_inputs:
            new_candidates = []
            for removal_steps, current_individual, considered_inputs, redundant_inputs, gain in candidates:
                if removal_input in redundant_inputs:
                    # remove input
                    new_removal_steps = removal_steps + [removal_input]
                    individual_inputs = current_individual.inputs[:]# copy
                    individual_inputs.remove(removal_input)
                    new_considered_inputs = considered_inputs[:]# copy
                    new_considered_inputs.remove(removal_input)
                    new_gain = gain + removal_input.cost
                    # generate individual and determine its redundant inputs
                    new_individual = Individual(individual_inputs)
                    new_redundant_inputs = new_individual._get_redundant_inputs(new_considered_inputs)
                    # generate new candidate
                    new_candidate = (new_removal_steps, new_individual, new_considered_inputs, new_redundant_inputs, new_gain)
                    new_candidates.append(new_candidate)
                    # update best gain encountered so far
                    best_gain = max(best_gain, new_gain)
            candidates += new_candidates
        # select candidate(s) with largest gain
        best_candidates = [current_individual for removal_steps, current_individual, considered_inputs, redundant_inputs, gain in candidates if gain == best_gain]
        if len(best_candidates) == 0:
            raise ValueError("No best candidate, this is unexpected.")
        elif len(best_candidates) == 1:
            selected_candidate = best_candidates[0]
        else:# random, with uniform distribution
            selected_candidate = select(best_candidates)
        return selected_candidate, best_gain
    
    # compute inputs, amongst the considered ones, that are redundant
    # ensure that redundant inputs are in self.inputs
    def _get_redundant_inputs(self, considered_inputs: List[Input]) -> List[Input]:
        self_considered_inputs = [input for input in considered_inputs if input in self.inputs]
        considered_coverage = {coverId for input in self_considered_inputs for coverId in input.cover}
        superposition = self._get_superposition_map(considered_coverage)
        redundancy = self._get_redundancy_map(self_considered_inputs, superposition)
        redundant_inputs = [input for input in self_considered_inputs if redundancy[input.inputId] >= 1]
        return redundant_inputs
    
    # require self.inputCoverage
    # compute superposition, which is a dictionary: coverId -> int providing the superposition value for a given coverId
    def _get_superposition_map(self, considered_coverage: Set[CoverId]) -> Dict[CoverId, int]:
        superposition = {}
        for coverId in considered_coverage:
            superposition[coverId] = len(self.inputCoverage[coverId])
        return superposition
    
    # compute the redundancy of an input for a given superposition map
    def _get_redundancy_value(self, input: Input, superposition: Dict[CoverId, int]) -> int:
        redundancy_value = min([superposition[coverId] for coverId in input.cover]) - 1
        return redundancy_value
            
    # redundancy is a dictionary: InputId -> int which provides the redundancy value for a given input ID
    def _get_redundancy_map(self, considered_inputs: List[Input], superposition: Dict[CoverId, int]) -> Dict[InputId, int]:
        redundancy = {}
        for input in considered_inputs:
            redundancy[input.inputId] = self._get_redundancy_value(input, superposition)
        return redundancy

    # ---- COST ----
        
    # return cost if it was already computed, otherwise compute then return it
    def get_cost(self) -> int:
        try:
            return self.cost
        except AttributeError:
            self.cost = self._init_cost()
            return self.cost
                
    def _init_cost(self) -> int:
        cost = 0
        for input in self.inputs:
            cost += input.cost
        return cost
