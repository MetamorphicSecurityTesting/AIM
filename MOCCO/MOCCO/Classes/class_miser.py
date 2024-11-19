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

from typing import List, Dict, Optional, Any
from MOCCO.Functions.normalization import Value, normalize, normalize_complement
from .class_input import Input, CoverId
from .class_individual import Individual


# the Miser class inherits attributes and methods from the Individual class, but it contains more information which are specific to the considered miser population, like an initial input coverage or a fitness vector
class Miser(Individual):
    
    def __init__(self, inputs: List[Input], initial_inputCoverage: Dict[CoverId, List[Input]], objectives: List[CoverId], verbose: Optional[bool] = False):
        # inheritance
        Individual.__init__(self, inputs, verbose = verbose)
        # objectives are necessary to compute the fitness vector
        self.objectives = objectives
        # the initial input coverage of the objectives is necessary to compute the potential
        self.initial_inputCoverage = initial_inputCoverage
        # initialize potential for get_potential
        self.potential = {}

    # ---- POTENTIAL ----
        
    # return the potential at a given objective, if it was already computed, otherwise compute then return it
    # potential is a dictionary: coverId -> int, initialized empty at __init__
    def get_potential(self, coverId: CoverId) -> int:
        try:
            return self.potential[coverId]
        except KeyError:
            self.potential[coverId] = self._init_potential(coverId)
            return self.potential[coverId]
    
    def _init_potential(self, coverId: CoverId) -> int:
        # potential_inputs should not be empty, as every coverId comes from an initial input
        potential_inputs = self.initial_inputCoverage[coverId]
        # potential computes the maximum possible gain of adding an input able to cover the objective coverId, minus the cost of that input
        potential_values = []
        for input in potential_inputs:
            # potential is computed only if coverId is not covered by the miser, hence input is not in self.inputs
            new_inputs = self.inputs + [input]
            # compute then reduce a new individual to determine the gain
            new_individual = Individual(new_inputs)
            reduced_individual, gain = new_individual.reduce_neighborhood(input)
            potential_values.append(gain - input.cost)
        potential_value = max(potential_values)
        # the worst cost is gain - input.cost, where gain = 0 and input is the least expensive input
        # hence, we add a term that does not depend on inputs in self to ensure that the potential is positive or zero
        potential_value += min([input.cost for input in potential_inputs])
        if potential_value < 0:
            raise ValueError("Potential should be >= 0, this is unexpected.")
        return potential_value

    # ---- FITNESS VECTOR ----
        
    # return the fitness vector of a miser, if it was already computed, otherwise compute then return it
    def get_fitness_vector(self) -> List[Value]:
        try:
            return self.fitness_vector
        except AttributeError:
            self.fitness_vector = self._init_fitness_vector()
            return self.fitness_vector
        
    # fitness_vector is a list [cost(individual), f_cov1(individual), ..., f_covN(individual)], where [cov1, ..., covN] is the list of objectives
    def _init_fitness_vector(self) -> List[Value]:
        vector = [normalize(self.get_cost())]
        for coverId in self.objectives:
            value = self.get_objective_function(coverId)
            vector.append(value)
        return vector
            
    # if the individual covers the objective, then the value is 0, otherwise it is the (normalized then complemented) potential
    def get_objective_function(self, coverId: CoverId) -> Value:
        if coverId in self.inputCoverage:
            value = 0.0
        else:
            potential = self.get_potential(coverId)
            value = normalize_complement(potential)
        return value

    # ---- EXPOSURE ----
        
    # return the exposure of a miser, if it was already computed, otherwise compute then return it
    def get_exposure(self) -> Value:
        try:
            return self.exposure
        except AttributeError:
            self.exposure = self._init_exposure()
            return self.exposure
                
    def _init_exposure(self) -> Value:
        exposure = 0.0
        vector = self.get_fitness_vector()
        # the value at index 0 is the normalized cost, the other ones are coverage values
        for val in vector[1:]:
            exposure += val
        return exposure

    # ---- PARETO DOMINANCE ----
        
    # miser1 = self dominates miser 2 if:
    #   1) for each objective function, we have f_i(miser1) <= f_i(miser2)
    #   and 2) there exists an objective function such that f_i(miser1) < f_i(miser2)
    def _pareto_dominates(self, miser2: Any) -> bool:# Any should be Self, available from Python 3.11
        vector1 = self.get_fitness_vector()
        vector2 = miser2.get_fitness_vector()
        # vector1 and vector2 have the same length = 1 + len(self.objectives)
        strict_dominance = False
        for i in range(len(vector1)):
            value1 = vector1[i]
            value2 = vector2[i]
            if value1 > value2:
                return False
            if value1 < value2:
                strict_dominance = True
        return strict_dominance
