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
import numpy as np
from deap import base, creator, tools, algorithms
import time
import csv
import ast
import pandas as pd
import os
import networkx as nx
import itertools
import sys
import argparse
pd.options.mode.chained_assignment = None

class NSGA3():
    # Function to suppress print statements
    def suppress_print(a):
        sys.stdout = open(os.devnull, 'w')

    # Function to restore print statements
    def restore_print(a):
        sys.stdout.close()
        sys.stdout = sys.__stdout__
    def check_pop(file_path, id_list):
        # Specify columns to read
        columns_to_read = ['SubClass', 'id']
        # Read the CSV file into a DataFrame
        a = id_list
        df = pd.read_csv(file_path, sep='\t')
        grouped = df.groupby('id')['SubClass'].apply(lambda x: set(x)).reset_index()
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
        add_list = []
        add_id_list = []
        a = grouped['id']
        for i in missing_numbers:
            for j in range(grouped['id'].__len__()):
                if i in grouped['SubClass'][j]:
                    id_list.append(int(grouped['id'][j]))
                    add_list.append(grouped['SubClass'][j])
                    break
        return id_list

    def generate_list(index, length=83):
        """Generate a list of given length with a 1 at the specified index and 0s elsewhere."""
        binary_list = [0] * length
        if 0 <= index < length:
            binary_list[index-1] = 1
        return binary_list


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
                binary_list = NSGA3.generate_list(index)
                binary_lists.append(binary_list)
                index_input.append(index)
                # costs.append(cost)
                # coverage.append(cover)

        return index_input, binary_lists

    def get_coverage(file_path):
        # Specify columns to read
        columns_to_read = ['SubClass', 'id']
        # Read the CSV file into a DataFrame
        df = pd.read_csv(file_path, sep='\t')
        grouped = df.groupby('id')['SubClass'].apply(lambda x: set(x)).reset_index()
        return grouped
        # return (grouped['SubClass'].values).tolist()

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
        necessaryitems_index=[]
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

            check_list  =  tuple(item for item in removal_sequence if item != remove_id)

            for values in check_list:
                if values  in necessary_items:
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
            cost = NSGA3.calculate_cost(sequence, coverages_individual, costs_individual, total_cost)
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
                    potential = 1/(1+total_cost)
                    fitness_vector[index] = potential
                else:
                    gain = NSGA3.gain(coverage, index, total_cost)
                    potential = 1/(gain+1)
                    fitness_vector[index] = potential
        return fitness_vector

    def eval_coverage_cost(individual):
        a = costs_individual
        total_cost = sum(individual[i] * costs_individual[i] for i in range(0, len(individual)-1))
        coverage = set()
        a = coverages_individual
        for i in range(len(individual)):
            if individual[i] == 1:
                coverage.update(coverages_individual['SubClass'][i])
        # unique_count = NSGA3.count_unique_items(coverage)
        coverage_vector = [0 if x in list(coverage) else 1 for x in range(int(NOBJ-1))]
        fitness_Coverage_vector = NSGA3.potential(total_cost, coverage_vector)
        # Ensure fitness values match NOBJ (5 values)
        fitness_values = [total_cost] + fitness_Coverage_vector
        assert len(fitness_values) == NOBJ, f"Fitness length mismatch. Expected {NOBJ}, got {len(fitness_values)}"

        return fitness_values


    # Custom time-based termination criterion
    class TimeBasedTermination:
        def __init__(self, max_time):
            self.start_time = None
            self.max_time = max_time

        def __call__(self, population, gen, *args, **kwargs):
            if self.start_time is None:
                self.start_time = time.time()
            return time.time() - self.start_time < self.max_time

    def determine_population(population, necessary_items, necessaryitems_index):
        max_coverage = 0
        selected_population =[]
        a = necessary_items
        for i , ind in enumerate(population):
            for index in necessaryitems_index:
                ind[index] = 1
        # full vulnerability coverage and minimum cost
        for i, ind in enumerate(population):
            # Filter the DataFrame to include only rows where 'id' is in the list of numbers
            # Extract indices where binary_list is 1 and increment by 1
            indices = [i + 1 for i, x in enumerate(ind) if x == 1]
            filtered_df = coverages_individual[coverages_individual['id'].isin(indices)]
            # Extract the 'SubClass' column and convert it to a set to get unique values
            subclasses_set = (filtered_df['SubClass'])
            # Merge all sets into one set using the union method
            merged_coverage = set().union(*subclasses_set)
            if len(merged_coverage) == NOBJ - 1:
                # print('full coverage')
                selected_population.append(ind)
            elif len(merged_coverage) < NOBJ - 1:

                max_coverage = len(merged_coverage)
                selected_ind = ind
                selected_population.append(ind)
        return selected_ind


    def determine_final_solution(population, Subclass_file_path):
        max_cost = 1000000000
        max_coverage = 0
        selected_population =[]
        for i, ind in enumerate(population):
            total_cost = sum(ind[i] * costs_individual[i] for i in range(len(ind)))
            # Extract indices where binary_list is 1 and increment by 1
            indices = [i + 1 for i, x in enumerate(ind) if x == 1]
            filtered_df = coverages_individual[coverages_individual['id'].isin(indices)]
            # Extract the 'SubClass' column and convert it to a set to get unique values
            subclasses_set = (filtered_df['SubClass'])
            # Merge all sets into one set using the union method
            merged_coverage = set().union(*subclasses_set)
            if len(merged_coverage) == NOBJ - 1:
                if total_cost < max_cost:
                    selected_ind = ind
                    max_cost = total_cost
                # return indices
            elif len(merged_coverage) > max_coverage:
                max_coverage = len(merged_coverage)
                selected_ind = ind
                max_cost = total_cost

        indices = [index_input[i] for i, x in enumerate(selected_ind) if x == 1]
        selected_ind = NSGA3.check_pop(Subclass_file_path, indices)
        return selected_ind , max_cost

    def find_indices_of_ones(binary_list):
        indices = [index+1 for index, value in enumerate(binary_list) if value == 1]
        return indices


    def count_unique_items(list_of_sets):
        value = (list_of_sets['SubClass'].values).tolist()
        unique_items = set().union(*value)
        return len(unique_items)

    def count_missing_items(list_of_sets):
        # Step 1: Merge all sets into a single set
        merged_set = set().union(*list_of_sets)

        # Step 2: Sort the resulting set
        sorted_list = sorted(merged_set)
        expected_range = set(range(NOBJ-1))

        # Step 4: Find missing elements
        missing_elements = expected_range - merged_set
        return missing_elements

    def main(reduced_input_path, Subclass_file_path, cost_path, time_budget):
        global costs_individual, coverages_individual, NOBJ, necessary_items, index_input, necessary_items_coverage, start_time

        index_input , inputs = NSGA3.process_csv(reduced_input_path)
        coverages_individual = NSGA3.get_coverage(Subclass_file_path)
        ids,necessary_items, necessary_items_coverage, necessaryitems_index = NSGA3.inputAnalysis(reduced_input_path, coverages_individual)
        list_id = list(ids)
        unique_count = NSGA3.count_unique_items(coverages_individual)

        # coverages_individual = coverages_individual
        costs_individual = []
        with open(cost_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                costs_individual = (row)

        costs_individual = list(map(float, costs_individual))
        NOBJ = unique_count + 1  # number of subclasses + 1 cost
        # self.NOBJ = NOBJ
        if hasattr(creator, "FitnessMulti"):
            del creator.FitnessMulti

        if hasattr(creator, "Individual"):
            del creator.Individual

        # Define the custom fitness and individual classes
        creator.create("FitnessMulti", base.Fitness, weights=(-1.0,) + (-1.0,) * unique_count)  # 4 coverage objectives + 1 cost
        creator.create("Individual", list, fitness=creator.FitnessMulti)

        # Parameters
        P = [1, 2]
        SCALES = [1, 0.5]

        # Create, combine and removed duplicates
        ref_points = [tools.uniform_reference_points(NOBJ, p, s) for p, s in zip(P, SCALES)]
        ref_points = np.concatenate(ref_points, axis=0)
        _, uniques = np.unique(ref_points, axis=0, return_index=True)
        ref_points = ref_points[uniques]
        # Increase or adjust the number as needed
        # Initialize DEAP toolbox
        toolbox = base.Toolbox()
        toolbox.register("attr_bool", random.randint, 0, 1)
        toolbox.register("individual", tools.initRepeat, creator.Individual, toolbox.attr_bool, n=len(inputs[0]))
        toolbox.register("population", tools.initRepeat, list, toolbox.individual)

        toolbox.register("mate", tools.cxTwoPoint)
        toolbox.register("mutate", tools.mutFlipBit, indpb=1.0 / len(inputs[0]))
        toolbox.register("select", tools.selNSGA3, ref_points=ref_points)
        toolbox.register("evaluate", NSGA3.eval_coverage_cost)

        # Genetic Algorithm parameters
        num_ref_points = len(ref_points)
        pop_size = ((num_ref_points + 3) // 4) * 4

        # Initialize population
        pop = toolbox.population(n=pop_size)

        NSGA3.determine_population(pop, necessary_items, necessaryitems_index)

        # Apply NSGA-III algorithm with DEAP
        termination = NSGA3.TimeBasedTermination(max_time=time_budget)
        start_time = time.time()
        hof = tools.HallOfFame(maxsize=1)
        logbook = tools.Logbook()
        logbook.header = ['gen', 'nevals'] + (hof[0].fitness.values if hof else [])
        gen = 0
        while termination(pop, gen):
            gen += 1
            offspring = algorithms.varAnd(pop, toolbox, cxpb=1, mutpb=1.0 / pop_size)
            elapsed_time = time.time() - start_time

            if elapsed_time >= time_budget:
                break


            for ind in offspring:
                if sum(ind) == 0:  # Check if all elements are zero
                    toolbox.mutate(ind)  # Apply mutation

                    del ind.fitness.values  # Invalidate fitness
            # Evaluate the individuals with an invalid fitness
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_budget:
                break

            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = map(toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Select the next generation population using NSGA-III mechanism
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_budget:
                break

            try:
                # print(len(pop + offspring))
                pop = toolbox.select(pop + offspring, k=pop_size)

            except IndexError as e:
                print("An error occurred during selection:", e)
                raise

            # Update the Hall of Fame with the generated individuals
            elapsed_time = time.time() - start_time
            if elapsed_time >= time_budget:
                break

            hof.update(pop)

            # Append the current generation statistics to the logbook
            record = hof[0].fitness.values if hof else []
            elapsed_time = time.time() - start_time
            # print(elapsed_time)
            if elapsed_time >= time_budget:
                break
            logbook.record(gen=gen, nevals=len(invalid_ind), **{f'f{i}': v for i, v in enumerate(record)})


        # Assign crowding distance for final population
        tools.emo.assignCrowdingDist(pop)
        pareto_front = tools.sortNondominated(pop, len(pop), first_front_only=True)[0]

        # selected_pop = NSGA3.determine_final_solution(pop)
        selected_pop, cost = NSGA3.determine_final_solution(pareto_front, Subclass_file_path)
        file_path = Subclass_file_path.rsplit(".", 1)[0] + "_NSGA3.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)

        output_path = os.path.join(os.path.realpath(directory), "NSGA3_minimized_inputset.csv")
        with open(output_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for element in selected_pop:
                csv_writer.writerow([element])
        print("The result is written in: " + str(output_path))

