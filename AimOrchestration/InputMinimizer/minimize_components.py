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


import time
import argparse
from pandas import read_csv
import pandas as pd
from IMPRO import Input as ImproInput
from IMPRO import InputSet
from MOCCO import Input as GeneticInput
from MOCCO import Individual, Population
import ast
import os
import csv
import re
import warnings
warnings.filterwarnings("ignore")

class Component_minimizer:

    def write_list_to_txt(file_path, data_list):
        with open(file_path, 'w') as txtfile:
            for item in data_list:
                txtfile.write(str(item) + ' ,')

    def write_list_to_csv(file_path, data_list):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for item in data_list:
                csv_writer.writerow([item])

    def write_list_to_csv_set(file_path, data_list):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for items in data_list:
                for item in items:
                    csv_writer.writerow([item])

def str2set(self, string):
        string = string.replace("{", "").replace("}", "").replace(" ", "")
        elements = string.split(",")
        elements = [float(element) for element in elements]
        result_set = set(elements)
        return result_set





# mimizer.search_solution()
# inputIds = [input.inputId for input in minimizer.solution]
# inputIds.sort()


def search_components():
    args = get_args()
    path_to_components = args.path_components
    populationSize = args.populationSize
    generations = args.generations
    time_budget = args.budget
    verbose = args.verbose
    # df = read_csv(path_to_components, sep='	', header=None,names=['0'])
    # Read the entire CSV file into a DataFrame.
    df = pd.read_csv(path_to_components, header=None)

    # Find the row indices where "new component" occurs.
    new_component_indices = df.index[df[0] == 'new component'].tolist()

    # Split the DataFrame into separate DataFrames based on the "new component" indices.
    dataframes = [df.iloc[start:end] for start, end in zip([0] + new_component_indices, new_component_indices + [None])]

    # minimized_components = []
    minimized_components_input_id=[]
    for df_chunk in dataframes:
        minimized_components=[]
        if df_chunk.iloc[0, 0].lower() == 'new component' and len(df_chunk)>1:
            df_chunk.drop(df_chunk.index[0], inplace=True)
        if len(df_chunk) == 1:
            break



        inputs = []

        component = []
        for index, row in df_chunk.iterrows():
            input_data = {
                "inputId": row[0],
                "cost": row[1],
                "cover": row[2]
            }
            component.append(input_data)


        # on each component, convert to MOCCO input to obtain the initial individual
        inputs = [GeneticInput(int(input["inputId"]), int(input["cost"]), ast.literal_eval(input["cover"])) for input in component]
        initial_individual = Individual(inputs)
        start_time = time.time()
        print("start_time", start_time, "seconds")
        population = Population(initial_individual)
        # then, the genetic search provides the input IDs of the solution
        final_individual = population.genetic_search(populationSize = populationSize, generations = generations, time_budget = time_budget, verbose = verbose)
        minimized_components.append([final_individual])
        end_time = time.time()
        duration = end_time - start_time
        print("Operation took", duration, "seconds")
        # print(minimized_components)
        # Extract input IDs using regular expression
        # minimized_components = str(minimized_components)
        numbers = re.findall(r'\d+', str(minimized_components))

        # Convert the extracted numbers to integers
        components_input_id = [int(num) for num in numbers][1:]
        minimized_components_input_id.append(components_input_id)
    if(len(minimized_components_input_id))>1:
        input_id= minimized_components_input_id[0]
        for i in range(1,len(minimized_components_input_id)):
            input_id += minimized_components_input_id[i]
        minimized_components_input_id = input_id
    if (len(minimized_components_input_id)) == 1:
        minimized_components_input_id= minimized_components_input_id[0]
    print(minimized_components_input_id)
    file_path = path_to_components.rsplit(".", 1)[0] + "_minimized.csv"
    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)
    # path_to_output = os.path.join(path_to_components, '..', filename)
    refData_dir_parent = os.path.dirname(path_to_components)
    path_to_output = os.path.join(refData_dir_parent, filename)
    Component_minimizer.write_list_to_csv(path_to_output, minimized_components_input_id)
    print("Minimization step successfully terminated.")
    print("The result is written in: " + str(path_to_output))
    # Perform some operation





def get_args():
    parser = argparse.ArgumentParser(
        prog='inputminimizer',
        description='initial input set'
    )
    parser.add_argument('path_components',
        metavar='COMPONENTS_PATH',
        help='relative path to the initial input set json file')
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

# minimize-inputs inputset.json outputs.txt costs.csv -d Levenshtein -o Kmeans -a Kmeans -v

# is not executed if the module is imported
if __name__ == "__main__":
    search_components()
