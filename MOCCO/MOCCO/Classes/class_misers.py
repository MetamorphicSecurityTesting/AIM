/*******************************************************************************
 * Copyright (c) University of Ottawa 2022-2024
 * Created by Nazanin Bayati (n.bayati@uottawa.ca),  Yoann Marquer (yoann.marquer@uni.lu)
 *     
 *  Licensed under the Apache License, Version 2.0 (the "License");
 *  you may not use this file except in compliance with the License.
 *  You may obtain a copy of the License at
 *  
 *  http://www.apache.org/licenses/LICENSE-2.0
 *  
 *  Unless required by applicable law or agreed to in writing, software
 *  distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *******************************************************************************/

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
