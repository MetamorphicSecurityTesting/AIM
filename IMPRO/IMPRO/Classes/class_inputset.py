from typing import List, Set, Dict, Tuple, Union, Any, Optional
from .class_input import Input, InputId, CoverId


# ---- INPUT SET CLASS ----

class InputSet:

    # ---- INITIALIZATION AND REPRESENTATION ----
    
    def __init__(self, inputs: List[Input], verbose: Optional[bool] = False):
        self.verbose = verbose
        if self.verbose:
            print("init input set")
        # check that each input identifier is unique
        self._check_inputs(inputs)
        self.remaining_inputs = inputs# updated during the problem reduction
        self.initialInput = self._init_initialInput(inputs)# dictionary storing the initial input
        # initialize other attributes
        self.necessary_inputs = []# initial inputs that should appear in the final solution
        self.removed_inputs = []# initial inputs removed during the whole process
        self.inputCoverage = self._init_inputCoverage()
    
    def __repr__(self):
        repr = f"<InputSet (id {id(self)}):\n"
        # initial inputs
        initial_inputs = [input.inputId for input in self.initialInput.values()]
        repr += f"   - initial_inputs = {initial_inputs}"
        # necessary inputs
        if hasattr(self, 'necessary_inputs'):
            necessary_inputs = [input.inputId for input in self.necessary_inputs]
            repr += f",\n   - necessary_inputs = {necessary_inputs}"
        # removed inputs
        if hasattr(self, 'removed_inputs'):
            removed_inputs = [input.inputId for input in self.removed_inputs]
            repr += f",\n   - removed_inputs = {removed_inputs}"
        # inputs
        remaining_inputs = [input.inputId for input in self.remaining_inputs]
        repr += f"\n   - remaining_inputs = {remaining_inputs}"
        # input coverage
        if hasattr(self, 'inputCoverage'):
            inputCoverage = {}
            for coverId, inputs in self.inputCoverage.items():
                inputCoverage[coverId] = [input.inputId for input in inputs]
            repr += f",\n   - inputCoverage = {inputCoverage}"
        # superposition
        if hasattr(self, 'superposition'):
            superposition = self.superposition
            repr += f",\n   - superposition = {superposition}"
        # redundancy
        if hasattr(self, 'redundancy'):
            redundancy = self.redundancy
            repr += f",\n   - redundancy = {redundancy}"
        # neighbors
        if hasattr(self, 'neighbors'):
            neighbors = {}
            for inputId, inputs in self.neighbors.items():
                neighbors[inputId] = {input.inputId for input in inputs}
            repr += f",\n   - neighbors = {neighbors}"
        # components
        if hasattr(self, 'components'):
            components = [{input.inputId for input in component} for component in self.components]
            repr += f",\n   - components = {components}"
        # end of representation
        repr += f"\n>"
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
            print("check_inputs passed")
        
    # initialInput is a dictionary: inputId -> Input associating to each inputId its initial input
    def _init_initialInput(self, initial_inputs: List[Input]) -> Dict[InputId, Input]:
        initialInput = {}
        for input in initial_inputs:
            initialInput[input.inputId] = input
        return initialInput
    
    # inputCoverage is a dictionary: CoverId -> List[Input] of the inputs covering a given coverId
    # requires self.remaining_inputs
    def _init_inputCoverage(self) -> Dict[CoverId, List[Input]]:
        inputCoverage = {}
        for input in self.remaining_inputs:
            for coverId in input.cover:
                if coverId not in inputCoverage:
                    inputCoverage[coverId] = []
                # each input is appended only once
                inputCoverage[coverId].append(input)
        return inputCoverage
        

    # ---- REDUCE PROBLEM ----
    
    # this is the main method of the class, that calls the methods below in order to reduce the search problem
    def reduce_problem(self, compute_diagnostics: Optional[bool] = False, verbose: Optional[bool] = None):
        self.compute_diagnostics = compute_diagnostics
        if self.compute_diagnostics:
            self.diagnostics = {}
        if verbose is not None:
            self.verbose = verbose
        if self.verbose:
            print("start problem reduction")
        # on the one hand, reducing coverage objectives after determining necessary inputs may lead to more duplicates or locally-dominated inputs
        # one the other hand, removing duplicates or locally-dominated inputs may change redundancy, thus may lead to more necessary inputs
        # hence, we have a loop, until a fixpoint is reached
        while True:
            if self.verbose:
                print("determine redundancy")
            self.determine_redundancy()
            self.changed_inputs = []# inputs removed during one iteration
            if self.verbose:
                print("remove duplicates")
            self.remove_duplicates()
            if self.verbose:
                print("remove locally-dominated")
            self.remove_locally_dominated()
            # if no input was removed during this iteration, then the redundancy has not changed, thus we have reached a fixed point
            # such a fixpoint has to happen, because each iteration (except the last one) removes at least one input
            if self.changed_inputs == []:
                break
        self._check_reduction()
        if self.verbose:
            print("divide problem")
        self.divide_problem()
        self._check_coverage()
        if self.verbose:
            print("problem reduced")
            self._print_result()
        return self.necessary_inputs, self.components
    
    # after problem reduction, we should have initial_inputs == removed_inputs + necessary_inputs + remaining inputs
    # because the input coverage is reduced in components, the test is performed on input IDs and not inputs themselves
    # require self.initialInput, self.remaining_inputs, self.removed_inputs, self.necessary_inputs
    # moreover, in case diagnostics were computed, we should have the keys of self.diagnostics to be the same input IDs than removed_inputs
    def _check_reduction(self):
        # gather lists of input IDs
        initial_inputs = [input.inputId for input in self.initialInput.values()]
        necessary_inputs = [input.inputId for input in self.necessary_inputs]
        removed_inputs = [input.inputId for input in self.removed_inputs]
        remaining_inputs = [input.inputId for input in self.remaining_inputs]
        # test number of elements
        if len(initial_inputs) == len(necessary_inputs) + len(removed_inputs) + len(remaining_inputs):
            check_len = True
        else:
            check_len = False
        # test elements
        if set(initial_inputs) == set(necessary_inputs) | set(removed_inputs) | set(remaining_inputs):
            check_set = True
        else:
            check_set = False
        # test diagnostics
        if (not self.compute_diagnostics) or set(self.diagnostics.keys()) == set(removed_inputs):
            check_diagnostics = True
        else:
            check_diagnostics = False
        # verdict
        if check_len and check_set and check_diagnostics:
            if self.verbose:
                print("check_reduction passed")
        else:
            # report inputs
            if (not check_len) or (not check_set):
                print("initial_inputs =", initial_inputs)
                print("necessary_inputs =", necessary_inputs)
                print("removed_inputs =", removed_inputs)
                print("remaining_inputs =", remaining_inputs)
                raise ValueError("Removed, necessary, and remaining inputs do not match initial inputs.")
            # report diagnostics
            if not check_diagnostics:
                print("removed_inputs =", removed_inputs)
                print("diagnostics =", set(self.diagnostics.keys()))
                raise ValueError("Diagnostics do not match removed inputs.")
    
    # the solution should match the initial coverage, i.e., coverage(initial_inputs) = coverage(necessary_inputs) + coverage(components)
    # require self.initialInput, self.necessary_inputs, self.components
    def _check_coverage(self):
        # gather initial coverage
        initial_coverage = set()
        for input in self.initialInput.values():
            initial_coverage |= input.cover
        # gather necessary coverage
        necessary_coverage = set()
        for input in self.necessary_inputs:
            necessary_coverage |= input.cover
        # gather component coverage
        component_coverage = set()
        for component in self.components:
            for input in component:
                component_coverage |= input.cover
        # verdict
        if necessary_coverage | component_coverage == initial_coverage:
            if self.verbose:
                print("check_coverage passed")
        else:
            print("initial_coverage =", initial_coverage)
            print("necessary_coverage =", necessary_coverage)
            print("component_coverage =", component_coverage)
            raise ValueError("The necessary and component inputs do not match initial input coverage.")
        
    # print in the console the final input set and a summary of the solution
    def _print_result(self):
        print(self)
        print(len(self.initialInput), "initial input(s)")
        print(len(self.removed_inputs), "removed input(s)")
        print(len(self.necessary_inputs), "necessary input(s)")
        sizes = [len(component) for component in self.components]
        if len(sizes) == 0:
            print("no component")
        else:
            str_sizes = str(sizes[0])
            for i in range(1, len(sizes)):
                str_sizes += ", " + str(sizes[i])
            print(len(self.components), "component(s), with size:", str_sizes)
    
    
    # ---- DETERMINE REDUNDANCY ----
        
    # compute the redundancy of each input to determine the necessary sequences, then remove the objectives already covered by necessary inputs and update the inputs attribute with the remaining inputs
    def determine_redundancy(self):
        # compute redundancy
        self.superposition = self._init_superposition()
        self.redundancy = self._init_redundancy()
        # distinguish necessary from redundant inputs
        necessary_inputs, redundant_inputs = self._distinguish_inputs()
        self.necessary_inputs += [self.initialInput[input.inputId] for input in necessary_inputs]
        # update inputCoverage by removing coverId already covered by necessary sequences
        for input in necessary_inputs:
            for coverId in input.cover:
                self.inputCoverage.pop(coverId, None)
        # reduce input coverage according to self.inputCoverage, if the coverage is empty then the redundant input is removed, otherwise it is a new input
        self.remaining_inputs, removed_inputs = self._reduce_input_coverage(redundant_inputs)
        self.removed_inputs += removed_inputs
        # recompute inputCoverage based on new inputs
        self.inputCoverage = self._init_inputCoverage()
        # because we removed necessary inputs or redundant inputs with a coverage included in the coverage of the necessary inputs, the superposition of the remaining coverage has not changed
        # hence, because we removed coverage objectives, the redundancy of the remaining inputs can only increase, and new necessary inputs cannot happen without first removing more inputs
            
    # superposition is a dictionary: coverId -> int providing the superposition value for a given coverId
    # requires self.inputCoverage
    def _init_superposition(self) -> Dict[CoverId, int]:
        superposition = {}
        for coverId, covering_inputs in self.inputCoverage.items():
            superposition[coverId] = len(covering_inputs)
        return superposition
    
    # compute the redundancy of input in self
    # requires self.superposition
    def get_redundancy(self, input: Input) -> int:
        inputSuperpos = [self.superposition[coverId] for coverId in input.cover]
        return min(inputSuperpos) - 1
            
    # redundancy is a dictionary: InputId -> int which provides the redundancy value for a given input (id)
    # requires self.remaining_inputs and self.superposition
    def _init_redundancy(self) -> Dict[InputId, int]:
        redundancy = {}
        for input in self.remaining_inputs:
            redundancy[input.inputId] = self.get_redundancy(input)
        return redundancy
        
    # necessary_inputs is a list of inputs with redundancy 0 while redundant_inputs is a list of inputs with redundancy >= 1
    # requires self.remaining_inputs and self.redundancy
    def _distinguish_inputs(self) -> Tuple[List[Input], List[Input]]:
        redundancy = self.redundancy
        necessary_inputs = []
        redundant_inputs = []
        for input in self.remaining_inputs:
            if redundancy[input.inputId] == 0:
                necessary_inputs.append(input)
            else:
                redundant_inputs.append(input)
        return necessary_inputs, redundant_inputs
    
    # keep only that redundant inputs that cover at least one objective in the updated inputCoverage, in that case their coverage is updated
    # the other redundant inputs are removed
    # requires self.initialInput and self.inputCoverage (and self.necessary_inputs for diagnostics)
    def _reduce_input_coverage(self, old_inputs: List[Input]) -> Tuple[List[Input], List[Input]]:
        new_inputs = []
        removed_inputs = []
        objectives = set(self.inputCoverage)
        for i in range(len(old_inputs)):
            oldInput = old_inputs[i]
            newCover = oldInput.cover & objectives
            if newCover == set():
                removed_inputs.append(self.initialInput[oldInput.inputId])
                if self.compute_diagnostics:
                    diagnostic = {'cause': 'objectives'}
                    cause_inputs = [necessInput.inputId for necessInput in self.necessary_inputs if len(necessInput.cover & oldInput.cover) > 0]
                    cause_inputs.sort()
                    diagnostic['inputs'] = cause_inputs
                    self.diagnostics[oldInput.inputId] = diagnostic
            else:
                newInput = Input(oldInput.inputId, oldInput.cost, newCover)
                new_inputs.append(newInput)
        return new_inputs, removed_inputs
    
    
    # ---- REMOVE DUPLICATES ----
        
    # two inputs with the same cost and coverage are considered equivalent
    # if there are several equivalent inputs, this function removes all but the first one
    # requires self.remaining_inputs, self.removed_inputs, self.changed_inputs, and self.inputCoverage
    def remove_duplicates(self):
        inputs = self.remaining_inputs
        # from last to first, to avoid messing with indices when removing an input
        for i in range(len(inputs) - 1, -1, -1):
            input1 = inputs[i]
            # comparison with previous inputs
            for j in range(i):
                input2 = inputs[j]
                if input1.cost == input2.cost and input1.cover == input2.cover:
                    # if input1 and input2 are equivalent, then remove input1 and break the loop on input2 to move to the next input1
                    self.remove_input(input1)
                    if self.compute_diagnostics:
                        diagnostic = {'cause': 'duplicate', 'inputs': [input2.inputId]}
                        self.diagnostics[input1.inputId] = diagnostic
                    break
        
    # remove a given input from self.remaining_inputs, then update self.removed_inputs, self.changed_inputs, and self.inputCoverage accordingly
    def remove_input(self, input: Input):
        remove_from(input, self.remaining_inputs)
        self.removed_inputs.append(self.initialInput[input.inputId])
        self.changed_inputs.append(input)
        for coverId in input.cover:# in inputCoverage
            remove_from(input, self.inputCoverage[coverId])
    
    
    # ---- LOCAL DOMINANCE ----
    
    # an input i0 is locally dominated by inputs i1, ... , iN if they are all distinct, cost(i0) >= cost(i1) + ... + cost(iN), and i1, ... , iN cover the same entities as i0 or more
    # locally-dominated inputs are not required in the final solution, so they are removed to reduce the problem even more
    # they can be removed in no particular order
    def remove_locally_dominated(self):
        # neighbors are computed, then updated during the search for locally-dominated inputs
        self.neighbors = self._init_neighbors()
        self._remove_dominated_inputs()
                
    # neighbors is a dictionary: inputId -> Set[Inputs] mapping each input (id) to the set of its neighbors, according to the overlapping relation: two inputs overlap if and only if they cover at least one objective in common
    # requires self.remaining_inputs and self.inputCoverage
    def _init_neighbors(self) -> Dict[InputId, Set[Input]]:
        neighbors = {}
        # initialize keys with empty neighbor sets
        for input in self.remaining_inputs:
            neighbors[input.inputId] = set()
        # fill neighbor sets, based on coverage
        for coverId, covering_inputs in self.inputCoverage.items():
            for i in range(0, len(covering_inputs)):
                input1 = covering_inputs[i]
                for j in range(i + 1, len(covering_inputs)):
                    input2 = covering_inputs[j]
                    # input1 and input2 are distinct
                    neighbors[input1.inputId].add(input2)
                    neighbors[input2.inputId].add(input1)
        return neighbors
                
    # update neighbors by removing occurrences of removed_input
    def _update_neighbors(self, neighbors: Dict[InputId, Set[Input]], removed_input: Input):
        neigh_inputs = neighbors.pop(removed_input.inputId)
        for input in neigh_inputs:
            remove_from(removed_input, neighbors[input.inputId])
    
    # an input can only be locally dominated by neighboring inputs
    # remove the inputs that are locally dominated by neighboring inputs
    # to save time, the neighbors are updated during the search, to not check for the already removed inputs
    # requires self.remaining_inputs, self.removed_inputs, self.changed_inputs, self.inputCoverage, and self.neighbors
    def _remove_dominated_inputs(self):
        inputs = self.remaining_inputs
        neighbors = self.neighbors
        # from last to first, to avoid messing with indices when removing an input
        for i in range(len(inputs) - 1, -1, -1):
            current_input = inputs[i]
            current_cost = current_input.cost
            current_cover = current_input.cover
            current_isDominated = False
            neigh_inputs = list(neighbors[current_input.inputId])
            # each subset of neighboring inputs is taken into account once, based on the order of the list above
            # in order to save computations during the iteration, each subset is represented by a triple (list, cost, cover) where list is the list of inputs in the subset, cost is the cumulative cost of inputs in the subset, and cover is the cumulative coverage of inputs in the subset
            sublists = [([], 0, set())]
            for neigh_input in neigh_inputs:
                neigh_cost = neigh_input.cost
                neigh_cover = neigh_input.cover
                newSublists = []
                for sublist_inputs, sublist_cost, sublist_cover in sublists:
                    cumul_cost = sublist_cost + neigh_cost
                    # we consider only the sublists that have a cost lower or equal to the cost of current input
                    if cumul_cost <= current_cost:
                        cumul_cover = sublist_cover | neigh_cover
                        # we check if the cover of the current input is reached
                        # in that case, current_input is dominated so the search can stop
                        if cumul_cover >= current_cover:
                            current_isDominated = True
                            break
                        # otherwise, we store the candidate, so that it can be extended later by the next neighboring inputs
                        else:
                            newSublist = (sublist_inputs + [neigh_input], cumul_cost, cumul_cover)
                            newSublists.append(newSublist)
                # the search stops if the current input is dominated
                if current_isDominated:
                    break
                # otherwise the enriched subsets are added for the next neighboring input
                else:
                    sublists += newSublists
            # if the current input is dominated, then it is removed
            if current_isDominated:
                self.remove_input(current_input)
                if self.compute_diagnostics:
                    diagnostic = {'cause': 'dominated'}
                    cause_inputs = [sublistInput.inputId for sublistInput in sublist_inputs + [neigh_input]]
                    cause_inputs.sort()
                    diagnostic['inputs'] = cause_inputs
                    self.diagnostics[current_input.inputId] = diagnostic
                # to save time, the neighbors are updated during the search, to not check for the already removed inputs
                self._update_neighbors(neighbors, current_input)
                # at the end of this method, some inputs may not have neighbors anymore, in that case they will be considered necessary in the next iteration
                
    
    # ---- DIVIDE PROBLEM ----
    
    #
    def divide_problem(self):
        components = self._init_components()
        self._check_components(components)
        self.components = components
                
    # components is a list of sets of inputs, each set of inputs corresponding to a connected component of the overlapping graph
    # requires self.remaining_inputs and self.neighbors
    def _init_components(self) -> List[Set[Input]]:
        neighbors = self.neighbors
        remaining_inputs = self.remaining_inputs[:]# copy
        components = []
        while len(remaining_inputs) > 0:
            # start new component
            input = remaining_inputs.pop()
            components.append(set())
            inputs_toVisit = {input}
            # visit component using neighbors
            while len(inputs_toVisit) > 0:
                input = inputs_toVisit.pop()
                remove_from(input, remaining_inputs)
                components[-1].add(input)
                new_neighbors = neighbors[input.inputId] - components[-1]
                inputs_toVisit |= new_neighbors
        return components
    
    # check union of components == inputs
    def _check_components(self, components: List[Set[Input]]):
        union_components = set()
        for component in components:
            union_components |= component
        if union_components == set(self.remaining_inputs):
            if self.verbose:
                print("check_components passed")
        else:
            raise ValueError("The union of components does not match the inputs.")
        

    # ---- GET DIAGNOSTICS ----
    
    # diagnostics is a dictionary: InputId -> dict, where:
    #   - dict['cause'] is a string  (amongst 'objectives', 'duplicate', and 'dominated') indicating the step where the input was removed
    #   - dict['inputs'] is a list of inputIds, indicating the inputs involved in the removal of the input
    #       - for 'objectives': the necessary inputs that cover the input objectives
    #       - for 'duplicate': the duplicate input that was kept
    #       - for 'dominated': the inputs that locally-dominate the input
    def get_diagnostics(self):
        try:
            return self.diagnostics
        except AttributeError:
            return None


# ---- AUXILIARY FUNCTIONS ----

# remove an element from a list or a set, and silently fails if the element is not in it
# this version is prefered to the (clearer) variant:
#    if element in listOrSet:
#        listOrSet.remove(element)
# because the element may be removed from listOrSet between the check and the method call
def remove_from(element: Any, listOrSet: Union[List, Set]):
    try:
        listOrSet.remove(element)
    except ValueError:
        pass
