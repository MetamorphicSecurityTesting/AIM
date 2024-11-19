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
 
# this file gathers the available test


# test reduce individual
def test_reduce(verbose: bool):
    from .test_reduce import reduce_considered_inputs, reduce_individual, reduce_groundTruth
    individual, gain = reduce_individual.reduce(reduce_considered_inputs)
    if verbose:
        if (individual.inputs, gain) == reduce_groundTruth:
            print("test_reduce passed")
        else:
            print("test_reduce failed")
    
# test fitness vector
def test_fitness(verbose: bool):
    from .test_fitness import fitness_miser, fitness_groundTruth
    fitness_vector = fitness_miser.get_fitness_vector()
    if verbose:
        if fitness_vector == fitness_groundTruth:
            print("test_fitness passed")
        else:
            print("test_fitness failed")
    
# test example 1
def test_example1(populationSize: int, generations: int, time_budget: int, verbose: bool):
    from .test_example1 import example1_population, test1_groundTruth
    final_individual = example1_population.genetic_search(populationSize = populationSize, generations = generations, time_budget = time_budget, verbose = False)
    if verbose:
        if set(final_individual.inputs) == test1_groundTruth:
            print("test_example1 passed")
        else:
            print("test_example1 failed, but since the genetic search is non-deterministic, you may have been unlucky, so you should try several times.")
    
# test example 2
def test_example2(populationSize: int, generations: int, time_budget: int, verbose: bool):
    from .test_example2 import example2_population, test2_groundTruth
    final_individual = example2_population.genetic_search(populationSize = populationSize, generations = generations, time_budget = time_budget, verbose = False)
    if verbose:
        if set(final_individual.inputs) == test2_groundTruth:
            print("test_example2 passed")
        else:
            print("test_example2 failed, but since the genetic search is non-deterministic, you may have been unlucky, so you should try several times.")
