/*******************************************************************************
 * Copyright (c) University of Ottawa 2022-2024
 * Created by Nazanin Bayati (n.bayati@uottawa.ca)
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


import random
from deap import base, creator, tools, algorithms
import time
import os
import csv
import ast
import pandas as pd
import networkx as nx
import itertools
import argparse
pd.options.mode.chained_assignment = None
import warnings
# Suppress specific runtime warnings
warnings.filterwarnings("ignore", category=RuntimeWarning, message="A class named 'FitnessMulti' has already been created and it ")
warnings.filterwarnings("ignore", category=RuntimeWarning, message="A class named 'Individual' has already been created and it ")



class MOSA:

    def generate_list(index):
        """Generate a list of given length with a 1 at the specified index and 0s elsewhere."""
        final_list=[]
        length = len(index)
        for i in range (0,length):
            binary_list = [0] * length
            binary_list[i] = 1
            final_list.append(binary_list)
        return final_list

    def process_csv(file_path):
        """Read CSV file, remove the last row, and process each remaining row to generate lists based on the first number."""
        binary_lists = []
        costs = []
        index_input = []
        with open(file_path, mode='r') as file:
            csv_reader = list(csv.reader(file))
            csv_reader.pop()  # Remove the last row
            for row in csv_reader:
                index = int(row[0])
                cost = float(row[1])
                cover = ast.literal_eval(row[2])  # Convert the string representation of a set to an actual set
                index_input.append(index)

        return index_input

    def get_coverage(file_path):
        # Specify columns to read
        columns_to_read = ['SubClass', 'id']
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, sep='\t')
        grouped = df.groupby('id')['SubClass'].apply(lambda x: set(x)).reset_index()
        return grouped
        # return (grouped['SubClass'].values).tolist()

    def merge_binary_lists(lists):
        # Assuming all binary lists are of the same length
        merged_list = lists[0]
        for lst in lists[1:]:
            merged_list = [max(a, b) for a, b in zip(merged_list, lst)]
        return merged_list

    def inputAnalysis(reduced_input_path, df):
        reduced_inputs = pd.read_csv(reduced_input_path, header=None)
        reduced_inputs_id = list(reduced_inputs[0])
        reduced_inputs_id.pop()
        # Convert the list to float for matching with 'id' column
        match_list = [float(num) for num in reduced_inputs_id]

        # Filter the DataFrame to keep only rows that match the 'id' values in match_list
        filtered_df = df[df['id'].isin(match_list)]

        # Convert the 'id' column to integers
        filtered_df['id'] = filtered_df['id'].astype(int)
        df = filtered_df.reset_index()
        # Step 1: Create a frequency dictionary
        frequency_dict = {}
        for index, row in df.iterrows():
            for number in row['SubClass']:
                if number in frequency_dict:
                    frequency_dict[number] += 1
                else:
                    frequency_dict[number] = 1

        # Step 2: Identify necessary items
        necessaryitems = set()
        necessaryitems_index = []
        necessaryitems_coverage = set()
        for index, row in df.iterrows():
            for number in row['SubClass']:
                if frequency_dict[number] == 1:
                    necessaryitems.add(row['id'])
                    necessaryitems_index.append(index)
                    necessaryitems_coverage = necessaryitems_coverage.union(row['SubClass'])
                    break

        # Initialize a graph
        G = nx.Graph()

        # Add nodes to the graph
        for index, row in df.iterrows():
            G.add_node(row['id'])

        # Add edges for intersecting sets
        for index, row in df.iterrows():
            current_set = row['SubClass']
            current_id = row['id']

            for other_index, other_row in df.iterrows():
                if index != other_index:
                    if current_set & other_row['SubClass']:
                        G.add_edge(current_id, other_row['id'])

        # Find connected components
        connected_components = list(nx.connected_components(G))

        # Separate necessary items and neighbors
        neighbors_groups = []
        for component in connected_components:
            # Remove necessary items from the neighbor groups
            component = component - necessaryitems
            if len(component) > 0:
                neighbors_groups.append(list(component))

        # Convert necessaryitems to a list for output consistency
        necessaryitems = list(necessaryitems)

        return df['id'], necessaryitems, list(necessaryitems_coverage), necessaryitems_index

        # Function to calculate the cost for a given sequence of removals

    def calculate_cost(removal_sequence, df, costs_list, total_cost):
        current_df = df.copy()
        total_cost = 0
        necessary_items = set()

        for remove_id in removal_sequence:
            # Remove the row with the given id
            current_df = current_df[current_df['id'] != remove_id]
            index_of_value = index_input.index(remove_id)
            total_cost = total_cost + costs_list[index_of_value]
            # Update necessary items based on unique numbers
            frequency_dict = {}
            for index, row in current_df.iterrows():
                for number in row['SubClass']:

                    if number in frequency_dict:
                        frequency_dict[number] += 1
                    else:
                        frequency_dict[number] = 1

            necessary_items = set()
            for index, row in current_df.iterrows():
                for number in row['SubClass']:

                    if frequency_dict[number] == 1:
                        necessary_items.add(row['id'])
                        break

            check_list = tuple(item for item in removal_sequence if item != remove_id)

            for values in check_list:
                if values in necessary_items:
                    index_of_value = index_input.index(values)
                    total_cost = total_cost + costs_list[index_of_value]
            # Calculate the cost of remaining necessary items
            # total_cost = sum(costs_list[int(id) - 1] for id in necessary_items)

        return total_cost

    def gain(coverage, givenIndex, total_cost):
        # Get all IDs that can cover the given numbers
        ids_to_consider = set()
        for index, row in coverages_individual.iterrows():

            c = row['SubClass']
            if givenIndex in row['SubClass'] and row['id'] in index_input:
                ids_to_consider.add(row['id'])
        # Generate all possible removal sequences
        removal_sequences = list(itertools.permutations(ids_to_consider))

        # Track the maximum cost
        max_cost = 0
        max_sequence = []

        for sequence in removal_sequences:
            cost = MOSA.calculate_cost(sequence, coverages_individual, costs_individual, total_cost)
            if cost > max_cost:
                max_cost = cost
                max_sequence = sequence

        # print("Maximum Cost:", max_cost)
        # print("Removal Sequence for Maximum Cost:", max_sequence)
        return max_cost

    def potential(total_cost, coverage):
        fitness_vector = coverage
        gain = total_cost
        for index, element in enumerate(coverage):

            if element == 1:
                if index in necessary_items_coverage:
                    potential = 1 / (1 + total_cost)
                    fitness_vector[index] = potential
                # else:
                #     gain = MOSA.gain(coverage, index, total_cost)
                #     potential = 1 / (gain + 1)
                #     fitness_vector[index] = potential
        return fitness_vector

    def eval_coverage_cost(individual):
        a = costs_individual
        total_cost = sum(individual[i] * costs_individual[i] for i in range(0, len(individual) - 1))
        coverage = set()
        a = coverages_individual
        for i in range(len(individual)):
            if individual[i] == 1:
                coverage.update(coverages_individual['SubClass'][i])
        # unique_count = MOSA.count_unique_items(coverage)
        coverage_vector = [0 if x in list(coverage) else 1 for x in range(int(NOBJ - 1))]
        fitness_Coverage_vector = MOSA.potential(total_cost, coverage_vector)
        # Ensure fitness values match NOBJ (5 values)
        fitness_values = [total_cost] + fitness_Coverage_vector
        assert len(fitness_values) == NOBJ, f"Fitness length mismatch. Expected {NOBJ}, got {len(fitness_values)}"

        return fitness_values
    def count_unique_items(list_of_sets):
        value = (list_of_sets['SubClass'].values).tolist()
        unique_items = set().union(*value)
        return len(unique_items)

    def getCoverage(archive):

        coverage = set()
        a = filtered_coverage
        individual = MOSA.merge_binary_lists(archive)
        for i in range(len(individual)):
            if individual[i] == 1:
                coverage.update(filtered_coverage['SubClass'][i])
        # unique_count = MOSA.count_unique_items(coverage)
        coverage_vector = [0 if x in list(coverage) else 1 for x in range(int(NOBJ - 1))]
        return coverage_vector


    def update_archive(archive_dict, archive):
        for i in range(len(archive)):
            cost_item = 0
            binary_series = pd.Series(archive[i])
            filtered_df = filtered_coverage[binary_series == 1]
            a = filtered_coverage
            b = coverages_individual
            c = costs_individual
            item_coverage = list(filtered_df['SubClass'].tolist()[0])

            # retreive all the inputs that can cover the objectives:

            for index, value in enumerate(archive[i]):
                if value == 1:
                    cost_item += costs_individual[index]

            for item in item_coverage:
                if item in archive_dict:
                    if archive_dict[item] == []:
                        archive_dict[item] = (archive[i], cost_item)
                    else:
                        archive_dict[item] = (archive[i], cost_item)

        archive_dict.popitem()
        merged_list = archive_dict[0][0]

        # Iterate over the remaining lists and perform element-wise OR
        for key in list(archive_dict.keys())[1:]:
            merged_list = [a | b for a, b in zip(merged_list, archive_dict[key][0])]

        return archive_dict


    def update_archive_new(archive, offsprings):
        number_list = list(range(NOBJ))
        # among the new offsprings and the current inputs in the archive we choose the one that has the lowest cost
        # Initialize the merged list with the first list in list_of_lists
        merged_list = archive[0]

        # Iterate over the remaining lists and perform element-wise OR
        for current_list in archive[1:]:
            merged_list = [a | b for a, b in zip(merged_list, current_list)]

        merged_list_offspring = offsprings[0]

        # Iterate over the remaining lists and perform element-wise OR
        for current_list in offsprings[1:]:
            merged_list_offspring = [a | b for a, b in zip(merged_list_offspring, current_list)]

        individuals = [a | b for a, b in zip(merged_list_offspring, merged_list)]
        coverage_individual = filtered_coverage[[bool_value == 1 for bool_value in individuals]]
        cost_individual = [num for num, flag in zip(costs_individual, individuals) if flag == 1]

        result = {}
        for number in number_list:
            matching_ids = coverage_individual[coverage_individual['SubClass'].apply(lambda x: number in x)]['id'].tolist()
            if matching_ids:
                result[number] = matching_ids

        # Convert the result to a DataFrame for better visualization
        result_df = pd.DataFrame([(number, ids) for number, ids in result.items()], columns=['Number', 'Matching IDs'])
        # Calculate the minimum cost for each set of numbers and add it as a new column
        result_df['MinCost'] = result_df['Matching IDs'].apply(lambda num_set: min(num_set, key=lambda num: costs[int(num) - 1]))
        # Calculate the minimum cost for each set of numbers and add it as a new column
        result_df['Cost'] = result_df['Matching IDs'].apply(lambda num_set: min(costs[int(num) - 1] for num in num_set))

        unique_numbers = result_df['MinCost'].unique()
        # Sum the costs for these unique numbers
        cost_archive = result_df[result_df['MinCost'].isin(unique_numbers)].groupby('MinCost')['Cost'].sum().sum()

        a = index_input
        # Create the list of binary lists
        archive = []
        for num in unique_numbers:
            binary_list = [1 if i == index_input.index(num) else 0 for i in range(len(index_input))]
            archive.append(binary_list)
        a = archive
        return archive, cost_archive

    def check_coverage(id_list):
        # Specify columns to read
        columns_to_read = ['SubClass', 'id']
        # Read the CSV file into a DataFrame
        grouped = filtered_coverage
        id_df = pd.DataFrame(id_list, columns=['id'])
        merged_df = id_df.merge(grouped, on='id', how='left')

        # Extract the SubClass sets for the given ids and merge them
        merged_set = set().union(*merged_df.set_index('id')['SubClass'])
        # merged_set = set().union(*grouped.set_index('id').loc[id_list, 'SubClass'])
        merged_set = {int(x) for x in merged_set}
        # Sort the merged set
        sorted_list = sorted(merged_set)

        # Check for missing numbers
        full_range = set().union(*grouped.set_index('id')['SubClass'])
        # full_range = set(range(min(sorted_list), max(sorted_list) + 1))
        missing_numbers = full_range - merged_set
        # print(missing_numbers)
        return merged_set, missing_numbers

    def update_archive1(archive, population):
        for ind in population:
            for arch_ind in archive:
                # full archive
                result = MOSA.merge_binary_lists(archive)
                indices_of_ones = [index_input[i] for i, x in enumerate(result) if x == 1]
                coverage, missing_obj = MOSA.check_coverage(indices_of_ones)
                # member of archive
                indices_of_ones = [index_input[i] for i, x in enumerate(arch_ind) if x == 1]
                arch_coverage, arch_missing_obj = MOSA.check_coverage(indices_of_ones)
                # memeber of population
                pop_ind_ones = [index_input[i] for i, x in enumerate(ind) if x == 1]
                pop_coverage, pop_missing_obj = MOSA.check_coverage(pop_ind_ones)
                ind_zeros = [index for index, value in enumerate(ind.fitness.values[1:]) if value == 0]
                arch_ind_zeros = [index for index, value in enumerate(arch_ind.fitness.values[1:]) if value == 0]
                # If they cover the same indices of zeros or more with a lower cost, then replace
                if len(missing_obj) != 0:
                    if any(item in pop_coverage for item in missing_obj):
                        archive.append(ind)

                else:
                    if set(pop_coverage) == set(arch_coverage):
                        if ind.fitness.values[0] < arch_ind.fitness.values[0]:
                            archive.remove(arch_ind)
                            archive.append(ind)

                    # Or if by adding this we will cover a new objective, replace that set with what we have
                    elif set(arch_coverage).issubset(set(pop_coverage)):
                        archive.remove(arch_ind)
                        archive.append(ind)

        return archive

    # Define the crowding distance function
    def assign_crowding_dist(population):
        if len(population) == 0:
            return

        distances = [0.0] * len(population)
        for i in range(len(population[0].fitness.values)):
            population.sort(key=lambda ind: ind.fitness.values[i])
            distances[0] = distances[-1] = float('inf')
            min_f = population[0].fitness.values[i]
            max_f = population[-1].fitness.values[i]
            if max_f == min_f:
                continue
            for j in range(1, len(population) - 1):
                distances[j] += (population[j + 1].fitness.values[i] - population[j - 1].fitness.values[i]) / (
                            max_f - min_f)

        for ind, dist in zip(population, distances):
            ind.crowding_dist = dist


    # Define the selection function
    def preference_sorting(population):
        # Replace this function with the actual preference sorting logic for test cases
        population.sort(key=lambda ind: ind.fitness.values)
        return population

        # Function to check if an individual is all zeros

    def is_all_zeros(individual):
        return all(gene == 0 for gene in individual)
        # Custom function to generate offspring and avoid all zeros

    def varAndAvoidAllZeros(population, toolbox, cxpb, mutpb):
        offspring = algorithms.varAnd(population, toolbox, cxpb, mutpb)
        for i, ind in enumerate(offspring):
            while MOSA.is_all_zeros(ind):
                ind = toolbox.clone(random.choice(population))  # Clone a RandomS individual from the population
                offspring[i] = ind
                toolbox.mutate(ind)  # Mutate the cloned individual
                del ind.fitness.values  # Invalidate the fitness of the modified individual
        return offspring

    # Define the main function
    def main(reduced_input_path, Subclass_file_path, cost_path, time_budget):
        # RandomS.seed(64)
        global costs_individual, costs, filtered_coverage, coverages_individual, NOBJ, necessary_items, index_input, necessary_items_coverage, start_time
        index_input = MOSA.process_csv(reduced_input_path)
        inputs =  MOSA.generate_list(index_input)

        b = inputs
        coverages_individual = MOSA.get_coverage(Subclass_file_path)
        ids, necessary_items, necessary_items_coverage, necessaryitems_index = MOSA.inputAnalysis(reduced_input_path,
                                                                                             coverages_individual)
        # print(index_input)
        c = ids
        filtered_coverage = coverages_individual[coverages_individual['id'].isin(index_input)].reset_index()
        # filtered_coverage = filtered_coverage.reset_index()
        filtered_coverage = filtered_coverage[['id', 'SubClass']]
        a = filtered_coverage
        list_id = list(ids)
        unique_count = MOSA.count_unique_items(coverages_individual)
        # print("Total count of unique items:", unique_count)
        # coverages_individual = coverages_individual
        costs = []
        with open(cost_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                costs = (row)

        costs = list(map(float, costs))
        a = costs
        costs_individual=[]
        for (i) in list_id:
            b = costs[0]
            costs_individual.append(costs[i-1])
        # a= costs_individual

        pop_size = 50
        TIME_BUDGET = time_budget
        NOBJ = unique_count + 1

        creator.create("FitnessMulti", base.Fitness,weights=(-1.0,) + (-1.0,) * unique_count)  # 4 coverage objectives + 1 cost
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        # Create the toolbox with the right parameters
        toolbox = base.Toolbox()
        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(inputs[0]))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("evaluate", MOSA.eval_coverage_cost)
        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(inputs[0]))
        toolbox.register("select", tools.selNSGA2)

        # Create an initial population
        cost_archive = 0
        # pop = toolbox.population(n=pop_size)
        # archive = [creator.Individual(ind) for ind in inputs]
        pop = [creator.Individual(ind) for ind in inputs]

        archive = pop.copy()

        # Evaluate the entire population
        # the initial fitness is the coverage of the objective
        fitnesses = list(map(toolbox.evaluate, pop))
        for ind, fit in zip(pop, fitnesses):
            ind.fitness.values = fit

        start_time = time.time()

        gen = 0
        while time.time() - start_time < TIME_BUDGET:
            gen += 1
            offspring = MOSA.varAndAvoidAllZeros(pop, toolbox, 1, 1.0 / pop_size)
            if time.time() - start_time >= TIME_BUDGET:
                break
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
            if time.time() - start_time >= TIME_BUDGET:
                break
            pop[:] = toolbox.select(pop + offspring, pop_size)
            pop = [ind for ind in pop if sum(ind) > 0]
            if time.time() - start_time >= TIME_BUDGET:
                break
            # Apply preference sorting
            pop = MOSA.preference_sorting(pop)

            # Assign crowding distance
            MOSA.assign_crowding_dist(pop)
            if time.time() - start_time >= TIME_BUDGET:
                break
            # Update the archive with the best test cases
            archive, cost_archive = MOSA.update_archive_new(archive, pop)

            fits = [ind.fitness.values[0] for ind in pop]

            # print(f"Gen {gen}: Min {min(fits)}, Max {max(fits)}, Avg {mean}, Std {std}")

        print(gen)

        # archive_list  = archive_dict
        result = MOSA.merge_binary_lists(archive)
        selected_pop = [index_input[i] for i, x in enumerate(result) if x == 1]
        coverage, missing_items = MOSA.check_coverage(selected_pop)
        file_path = Subclass_file_path.rsplit(".", 1)[0] + "_MOSA.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        output_path = os.path.join(os.path.realpath(directory), "MOSA_minimized_inputset.csv")
        with open(output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for element in selected_pop:
                csv_writer.writerow([element])
        print("The result is written in: " + str(output_path))


def get_args():
    parser = argparse.ArgumentParser(
        prog='inputreducer',
        description='initial input set for NSGA-3'
    )
    parser.add_argument('path_reduced_inputset',
                        metavar='REDUCED_INPUTSET_PATH',
                        help='path to the csv file of action subclasses')

    parser.add_argument('path_subclass',
        metavar='SUBCLASS_PATH',
        help='path to the csv file of action subclasses')

    parser.add_argument('path_sorted_cost',
                        metavar='SORTED_COST_PATH',
                        help='relative path to the cost csv file')

    parser.add_argument('-b', '--budget',
                        type=int,
                        default=600,
                        help='time budget (in seconds)'
                        )

    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    Subclass_file_path = args.path_subclass
    cost_path = args.path_sorted_cost
    reduced_input_path = args.path_reduced_inputset
    time_budget = args.budget
    MOSA.main(reduced_input_path=reduced_input_path, Subclass_file_path=Subclass_file_path, cost_path=cost_path, time_budget=time_budget)
