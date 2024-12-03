from typing import List, Optional
from MOCCO.Functions.selection import select
from .class_input import Input, InputId
from .class_individual import Individual

class Roofers:

    # ---- INITIALIZATION AND REPRESENTATION ----
        
    def __init__(self, initial_individual: Individual, populationSize: int):
        self.initial_individual = initial_individual
        self._check_populationSize(populationSize)
        self.populationSize = populationSize
        # initialize roofer population
        self.individuals = []
        for roofer in self._init_individuals():
            self.add_roofer(roofer)
    
    def __repr__(self):
        repr = f"<Roofers (id {id(self)}):\n"
        # initial individual
        repr += f"   - initial_individual = {self.initial_individual}\n"
        # population size
        repr += f"   - populationSize = {self.populationSize}\n"
        # individuals
        repr += f"   - individuals = {self.individuals}\n"
        # end of representation
        repr += f">"
        return repr
    
    def _check_populationSize(self, populationSize: int):
        if populationSize < 2:
            raise ValueError("The roofer population size should be >= 2.")
    
    def _init_individuals(self) -> List[Individual]:
        # prepare initial inputs and their occurrences, i.e., the number of times they were selected during this method
        initial_inputs = self.initial_individual.inputs[:]# copy
        occurrence = {}
        for input in initial_inputs:
            occurrence[input.inputId] = 0
        # generate individuals
        individuals = []
        for i in range(self.populationSize):
            # initialize empty individual
            individual_inputs = []
            individual = Individual(individual_inputs)
            # prepare variables for iteration
            remaining_inputs = initial_inputs[:]# copy
            remaining_objectives = set(self.initial_individual.inputCoverage)
            while len(remaining_objectives) > 0:
                # randomly select an objective not already covered, with uniform distribution
                potential_objectives = list(remaining_objectives)
                coverId = select(potential_objectives)
                # randomly select an input able to cover this objective, with a distribution where weights are inversely proportional to 1 + occurrence, in order to focus on diversity
                potential_inputs = list(self.initial_individual.inputCoverage[coverId])
                weights = [1.0/(1.0 + occurrence[input.inputId]) for input in potential_inputs]
                selected_input = select(potential_inputs, weights = weights)
                # remove input from remaining inputs and remove objectives already covered by this input
                remaining_inputs.remove(selected_input)
                remaining_objectives -= selected_input.cover
                # add input to individual inputs, then reduce
                individual_inputs.append(selected_input)
                individual = Individual(individual_inputs)
                individual, gain = individual.reduce_neighborhood(selected_input)
                individual_inputs = individual.inputs
                # occurrence is not updated here because an input that is added at an iteration can be removed during a subsequent iteration
            # individual now covers all objectives, it is appended, then occurrence is updated
            individuals.append(individual)
            for input in individual.inputs:
                occurrence[input.inputId] += 1
        return individuals
    
    # check, then add an individual
    def add_roofer(self, individual: Individual, verbose: Optional[bool] = False):
        self._check_roofer(individual)
        if verbose:
            print("   - update roofers")
        # if the population reached maximum size, then one of the most expensive roofer is randomly selected (using a uniform distribution), then removed
        if len(self.individuals) >= self.populationSize:
            costs = [roofer.get_cost() for roofer in self.individuals]
            cost_max = max(costs)
            expensive_individuals = [roofer for roofer in self.individuals if roofer.get_cost() == cost_max]
            selected_roofer = select(expensive_individuals)
            self.individuals.remove(selected_roofer)
        # append new roofer
        self.individuals.append(individual)
    
    def _check_roofer(self, individual: Individual):
        if not set(individual.inputCoverage) == set(self.initial_individual.inputCoverage):
            raise ValueError("A roofer should exactly cover all the objectives.")
