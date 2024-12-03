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
