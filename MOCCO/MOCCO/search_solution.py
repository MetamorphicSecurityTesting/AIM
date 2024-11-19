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

import argparse
from .Tests.tests import test_reduce, test_fitness, test_example1, test_example2
# usage example to run the tests with default parameters:
# mocco -v
# with population size = 50 and number of generation = 200:
# mocco -p 50 -g 200 -v
# with time budget = 3 seconds:
# mocco -b 3 -v
# (time budget can be 0, to test the initialization step)

# is not executed if the module is imported
if __name__ == "__main__":
    main()

def main():
    # arguments
    args = get_args()
    populationSize = args.populationSize
    generations = args.generations
    time_budget = args.budget
    verbose = args.verbose
    # run available tests
    test_reduce(verbose)
    test_fitness(verbose)
    test_example1(populationSize, generations, time_budget, verbose)
    test_example2(populationSize, generations, time_budget, verbose)

# parse arguments from command line
def get_args():
    parser = argparse.ArgumentParser(
        prog='MOCCO',
        description='MOCCO genetic algorithm, searching an input set that minimize the cost while covering all the action subclasses'
    )
    parser.add_argument('-p', '--populationSize',
        type=int,
        default=None,
        help='number of individuals per population'
    )
    parser.add_argument('-g', '--generations',
        type=int,
        default=None,
        help='number of generations for the evolutionary search'
    )
    parser.add_argument('-b', '--budget',
        type=int,
        default=None,
        help='time budget (in seconds)'
    )
    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='display execution information in the console')
    return parser.parse_args()
