from typing import List, Tuple, Set, Optional
import time
from MOCCO.Functions.selection import select, split
from .class_input import Input, CoverId
from .class_individual import Individual
from .class_roofers import Roofers
from .class_misers import Misers

class Population:

    # ---- INITIALIZATION AND REPRESENTATION ----
    
    def __init__(self, initial_individual: Individual):
        # attributes from initial individual
        self.verbose = initial_individual.verbose
        if self.verbose:
            print("Initialize population")
        self.initial_individual = initial_individual
        # default attributes
        self.default_populationSize = 20
        self.default_generations = 100
    
    def __repr__(self):
        repr = f"<Population (id {id(self)}):\n"
        # initial individual
        repr += f"   - initial_individual = {self.initial_individual}\n"
        # end of representation
        repr += f">"
        return repr

    # ---- EXHAUSTIVE SEARCH ----
    
    def exhaustive_search(self, verbose: Optional[bool] = None) -> Individual:
        if verbose is not None:
            self.verbose = verbose
        if self.verbose:
            print("Start exhaustive search")
        initial_individual = self.initial_individual
        individual, gain = initial_individual.reduce(initial_individual.inputs)
        if self.verbose:
            print("End exhaustive search")
        return individual

    # ---- GENETIC SEARCH ----
    
    def genetic_search(self, populationSize: Optional[int] = None, generations: Optional[int] = None, time_budget: Optional[int] = None, verbose: Optional[bool] = None) -> Individual:
        time_start = time.time()
        # arguments
        if populationSize is not None:
            self.populationSize = populationSize
        else:
            self.populationSize = self.default_populationSize
        if generations is not None:
            self.generations = generations
        else:
            self.generations = self.default_generations
        if verbose is not None:
            self.verbose = verbose
        if time_budget is not None and time_budget < 0:
            raise ValueError("Time budget should be non-negative.")
        # there is a search only if there are at least two initial inputs
        if len(self.initial_individual.inputs) < 2:
            if self.verbose:
                print("A search is not needed as the initial individual contains", len(self.initial_individual.inputs), "input.")
            return self.initial_individual
        # iterative search
        self.initialize_attributes()
        current_gen = 0
        while current_gen < self.generations or time_budget is not None:
            # the fixed number of generations is ignored if there is a time budget
            current_gen += 1
            if self.verbose:
                print("Generation", current_gen)
            # compute parents and offspring
            parent1, parent2 = self._select_parents()
            half1, half2 = split(self.objectives)
            offspring1, offspring2, edge = self._gen_offspring(parent1, parent2, half1, half2)
            mutant1, mutant2 = self._mutate_offspring(offspring1, offspring2, edge)
            # check time budget
            if time_budget is None or time.time() - time_start < time_budget:
                # there is no time budget or it is not exhausted yet
                self.update_population(mutant1)
                self.update_population(mutant2)
            else:
                # time budget is exhausted, so the population is frozen
                break
        # search result
        self.final_individual = self._determine_solution()
        if self.verbose:
            print("Complete genetic search")
        return self.final_individual

    # ---- INITIALIZE SEARCH ATTRIBUTES ----
    
    def initialize_attributes(self):
        if self.verbose:
            print("Start genetic search:")
            print("   - roofer population size =", self.populationSize)
            print("   - number of generations =", self.generations)
            print("Initialize population")
        # extract and sort objectives for a standard representation
        self.initial_inputCoverage = self.initial_individual.inputCoverage
        self.objectives = list(self.initial_inputCoverage.keys())
        self.objectives.sort()
        # initialize roofers and misers
        self.roofers = Roofers(self.initial_individual, self.populationSize)
        self.misers = Misers(self.initial_inputCoverage, self.objectives)

    # ---- SELECT PARENTS ----
    
    def _select_parents(self) -> Tuple[Individual, Individual]:
        if self.verbose:
            print("   - select parents")
        # a roofer parent is always selected
        roofer_individuals = self.roofers.individuals[:]
        weights = [1.0/roofer.get_cost() for roofer in roofer_individuals]
        roofer1 = select(roofer_individuals, weights = weights)
        # then, a miser parent is selected if there is any, otherwise another roofer parent is selected
        if len(self.misers.individuals) == 0:
            roofer_individuals.remove(roofer1)
            weights = [1.0/roofer.get_cost() for roofer in roofer_individuals]
            roofer2 = select(roofer_individuals, weights = weights)
            return roofer1, roofer2
        else:
            miser_individuals = self.misers.individuals[:]
            weights = [1.0/miser.get_exposure() for miser in miser_individuals]
            miser1 = select(miser_individuals, weights = weights)
            return roofer1, miser1

    # ---- GENERATE OFFSPRING ----
    
    # offsping1 and offsping2 of parent1 and parent2 according to the split of objectives half1 and half2
    # edge is a set of inputs that cover objectives in both half1 and half2
    def _gen_offspring(self, parent1: Individual, parent2: Individual, half1: List[CoverId], half2: List[CoverId]) -> Tuple[Individual, Individual, Set[Input]]:
        if self.verbose:
            print("   - crossover")
        # set of inputs covering each objective half
        half1_inputs = self._get_coveringInputs(half1)
        half2_inputs = self._get_coveringInputs(half2)
        edge = half1_inputs & half2_inputs
        # offspring parts
        offspring1_part1 = {input for input in parent1.inputs if input in half1_inputs}
        offspring1_part2 = {input for input in parent2.inputs if input in half2_inputs}
        offspring2_part1 = {input for input in parent2.inputs if input in half1_inputs}
        offspring2_part2 = {input for input in parent1.inputs if input in half2_inputs}
        # offspring individuals
        offspring1_inputs = list(offspring1_part1 | offspring1_part2)
        offspring1 = Individual(offspring1_inputs)
        offspring2_inputs = list(offspring2_part1 | offspring2_part2)
        offspring2 = Individual(offspring2_inputs)
        return offspring1, offspring2, edge
    
    def _get_coveringInputs(self, objectives: List[CoverId]) -> Set[Individual]:
        inputs = set()
        for coverId in objectives:
            inputs |= set(self.initial_inputCoverage[coverId])
        return inputs

    # ---- MUTATE OFFSPRING ----
        
    # each offspring is independently mutated, then the mutants are reduced based on the edge of the split
    def _mutate_offspring(self, offspring1: Individual, offspring2: Individual, edge: Set[Input]) -> Tuple[Individual, Individual]:
        if self.verbose:
            print("   - mutation")
        # mutation
        mutant1 = self._mutate(offspring1)
        mutant2 = self._mutate(offspring1)
        # reduction according to edge
        # this occurs even if an input was removed during mutation, since it also removes inputs from crossover
        mutant1, gain = mutant1.reduce_edge(edge)
        mutant2, gain = mutant2.reduce_edge(edge)
        return mutant1, mutant2
        
    # randomly select one input with uniform distribution, then generate a mutant of the individual for this input
    def _mutate(self, individual: Individual) -> Individual:
        initial_inputs = self.initial_individual.inputs[:]# copy
        individual_inputs = individual.inputs[:]# copy
        # if the individual contains a single input, we do not want to select this input and thus to generate an empty individual
        # this is not an issue for selection since the initial individual contains at least two inputs
        if len(individual_inputs) == 1:
            single_input = individual_inputs[0]
            initial_inputs.remove(single_input)
        # selection
        selected_input = select(initial_inputs)
        # mutation
        if selected_input in individual_inputs:
            individual_inputs.remove(selected_input)
        else:
            individual_inputs.append(selected_input)
        # generate mutant
        if len(individual_inputs) == 0:
            raise ValueError("A mutant should not be empty, this is unexpected.")
        mutant = Individual(individual_inputs)
        return mutant

    # ---- UPDATE POPULATION ----
    
    # update roofer or miser population, depending on the considered individual
    def update_population(self, individual: Individual):
        # determine if the individual is a roofer or a miser
        individual_coverage = set(individual.inputCoverage)
        initial_coverage = set(self.initial_individual.inputCoverage)
        if not individual_coverage <= initial_coverage:
            raise ValueError("An offspring coverage should be a subset of the initial coverage. This is unexpected.")
        # then, if the individual is new, leverage add function of the corresponding population
        if individual_coverage == initial_coverage:
            # individual is a roofer candidate
            is_new = self._is_new(individual, self.roofers.individuals)
            if is_new:
                self.roofers.add_roofer(individual, verbose = self.verbose)
        else:
            # individual is a miser candidate
            is_new = self._is_new(individual, self.misers.individuals)
            if is_new:
                self.misers.add_miser(individual, verbose = self.verbose)
    
    # to prevent duplication, check if the inputset of a candidate is the same as the inputset of an individual in the considered population
    def _is_new(self, candidate: Individual, individuals: List[Individual]) -> bool:
        candidate_inputs = set(candidate.inputs)
        is_new = True
        for individual in individuals:
            individual_inputs = set(individual.inputs)
            if candidate_inputs == individual_inputs:
                is_new = False
                break
        return is_new

    # ---- DETERMINE SOLUTION ----
    
    # the final individual is randomly selected, using uniform distribution, amongst the least costly roofers
    def _determine_solution(self) -> Individual:
        if self.verbose:
            print("Determine solution")
        costs = [roofer.get_cost() for roofer in self.roofers.individuals]
        cost_min = min(costs)
        candidates = [roofer for roofer in self.roofers.individuals if roofer.get_cost() == cost_min]
        final_individual = select(candidates)
        return final_individual
