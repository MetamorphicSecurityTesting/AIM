from typing import List, Dict, Optional
from .class_input import Input, CoverId
from .class_individual import Individual
from .class_miser import Miser


class Misers:

    # ---- INITIALIZATION AND REPRESENTATION ----
        
    def __init__(self, initial_inputCoverage: Dict[CoverId, List[Input]], objectives: List[CoverId]):
        self.initial_inputCoverage = initial_inputCoverage
        self.objectives = objectives
        # miser population is initially empty
        self.individuals = []
        # initialize fitness_vector for get_fitness_vector
        self.fitness_vector = {}
    
    def __repr__(self):
        repr = f"<Misers (id {id(self)}):\n"
        # individuals
        repr += f"   - individuals = {self.individuals}\n"
        # end of representation
        repr += f">"
        return repr

    # ---- MISER ----
    
    # check, then add an individual if it is non-dominated
    def add_miser(self, individual: Individual, verbose: Optional[bool] = False):
        self._check_miser(individual)
        # the miser class is required to compute the fitness vector
        candidate = self._init_miser(individual.inputs)
        # check Pareto dominance
        is_dominated = False
        for miser in self.individuals:
            if miser._pareto_dominates(candidate):
                is_dominated = True
                break
        # if the candidate is non-dominated, then the misers it dominates are removed, then it is added to the miser population
        if not is_dominated:
            if verbose:
                print("   - update misers")
            for miser in self.individuals:
                if candidate._pareto_dominates(miser):
                    self.individuals.remove(miser)
            self.individuals.append(candidate)
    
    def _check_miser(self, individual: Individual):
        if not set(individual.inputCoverage) < set(self.objectives):
            raise ValueError("A miser should cover a strict subset of the objectives.")
    
    def _init_miser(self, inputs: List[Input]):
        return Miser(inputs, self.initial_inputCoverage, self.objectives)
