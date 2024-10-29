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


import argparse
import pandas as pd
import ActionClustering
from ActionClustering import *
from OutputClustering import outputClustering
import RefineInputs.Classes
from RefineInputs.Classes.Preprocessing_Joomla import preProc_joomla
from PostProcessor import processor
from pandas import read_csv
from IMPRO import Input as ImproInput
from IMPRO import InputSet
from MOCCO import Input as GeneticInput
from MOCCO import Individual, Population
from PostProcessor import processor
from RefineInputs import Classes
import sys
import os
import numpy as np
import csv
import re


class Minimizer:

    def write_list_to_txt(file_path, data_list):
        with open(file_path, 'w') as txtfile:
            for item in data_list:
                txtfile.write(str(item) + ' ,')

    def write_list_to_csv(file_path, data_list):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for item in data_list:
                csv_writer.writerow([item.inputId])

    def write_list_to_csv_comp(file_path, data_list):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for item in data_list:
                csv_writer.writerow([item])

    def write_list_to_csv_set(file_path, data_list):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for items in data_list:
                for item in items:
                    a = [item.inputId, item.cost, item.cover]
                    csv_writer.writerow([item.inputId, item.cost, item.cover])
                csv_writer.writerow(['new component'])


    def str2set(self, string):
        string = string.replace("{", "").replace("}", "").replace(" ", "")
        elements = string.split(",")
        elements = [float(element) for element in elements]
        result_set = set(elements)
        return result_set

    def __init__(self, path_subclasses, cost_path, verbose = False):
        self.verbose = verbose
        # gather inputs from the subclasses file
        if verbose:
            print("gather inputs ID, cost, and coverage")

        df = read_csv(path_subclasses, sep='	')
        df['SubClass'] = df['SubClass'].round().astype(str)

        # Group sequences by subclass and merge subclass values
        # grouped_df = df.groupby('sequence')['SubClass'].apply(','.join).reset_index()
        grouped_df = df.groupby(['sequence', 'id'])['SubClass'].apply(','.join).reset_index()
        grouped_df_joomla = df.groupby(['id'])['SubClass'].apply(','.join).reset_index()
        df_sorted = grouped_df.sort_values('id', ascending=True)
        # print(grouped_df)
        df_sorted['cost'] = ''

        cost_df = pd.read_csv(cost_path, sep=' ')
        # mainDF = pd.read_csv(r'C:\Users\nbaya076\Dropbox\GitHub\Examples\RunningExample\refData.csv', sep='  ')
        list_cost = cost_df.values
        list_cost = str(list_cost[0]).split('[')[1].split(']')[0].split('\'')[1].split(',')
        cost = np.array(list_cost)

        # for i in range(0, cost.__len__()):
        #     if int(df_sorted['id'][i]) == 157:
        #         df_sorted['cost'][i] = cost[0]
        #     if int(df_sorted['id'][i]) == 158:
        #         df_sorted['cost'][i] = cost[1]
        #     if int(df_sorted['id'][i]) == 159:
        #         df_sorted['cost'][i] = cost[2]
        #     if int(df_sorted['id'][i]) == 160:
        #         df_sorted['cost'][i] = cost[3]
        # df_sorted.set_index('id', inplace=True)
        # a = cost[4:len(cost)]
        # b = df_sorted.loc[1:len(df_sorted) - 4, 'cost']
        # df_sorted.loc[1:len(df_sorted) - 4, 'cost'] = cost[4:len(cost)]
        print(len(df_sorted))
        print(len(cost))
        df_sorted['cost'] = cost

        inputs = []
        for i in range(df_sorted.__len__()):
            inputId = int(i+1)
            cost = int(df_sorted['cost'].iloc[i])
            coverEntry = df_sorted['SubClass'].iloc[i]
            cover = Minimizer.str2set(self,coverEntry)
            input = ImproInput(inputId, cost, cover)
            inputs.append(input)
        self.inputs = inputs

    def search_solution(self,path_inputset_init,path_subclasses, compute_diagnostics = False):
        verbose = self.verbose
        # initialize then reduce the problem
        inputSet = InputSet(self.inputs, verbose = verbose)
        necessary_inputs, components = inputSet.reduce_problem(compute_diagnostics = compute_diagnostics, verbose = verbose)
        if compute_diagnostics:
            diagnostics = inputSet.get_diagnostics()
            print("diagnostics =", diagnostics)
        # solve the problem on each component and gather the results
        self.minimized_inputset = necessary_inputs# necessary inputs have to be part of the solution


        # writing neseccary inputs in a csv file
        file_path = path_inputset_init.rsplit(".", 1)[0] + "_necessary.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        # path_to_output = os.path.join(path_subclasses, '..', filename)

        refData_dir_parent = os.path.dirname(path_subclasses)
        path_to_output = os.path.join(refData_dir_parent, filename)


        Minimizer.write_list_to_csv(path_to_output, necessary_inputs)


        # Writing components in a csv file
        file_path = path_inputset_init.rsplit(".", 1)[0] + "_components.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        # path_to_output = os.path.join(path_subclasses, '..', filename)

        refData_dir_parent = os.path.dirname(path_subclasses)
        path_to_output = os.path.join(refData_dir_parent, filename)

        Minimizer.write_list_to_csv_set(path_to_output, components)

        print("Reduction step successfully terminated.")
        print("The result is written in: " + str(path_to_output))


        minimized_components=[]
        minimized_components_input_id=[]
        for component in components:
            print("component:")
            # print(component)
            # on each component, convert to MOCCO input to obtain the initial individual
            inputs = [GeneticInput(input.inputId, input.cost, input.cover) for input in component]
            initial_individual = Individual(inputs)
            population = Population(initial_individual)
            print(population)
            # then, the genetic search provides the input IDs of the solution
            final_individual = population.genetic_search(verbose = verbose)
            self.minimized_inputset += [inputSet.initialInput[input.inputId] for input in final_individual.inputs]
            minimized_components.append([[input.inputId for input in final_individual.inputs]])

            # print(minimized_components)
            # Extract input IDs using regular expression
            # minimized_components = str(minimized_components)
            numbers = re.findall(r'\d+', str(minimized_components))

            # Convert the extracted numbers to integers
            components_input_id = [int(num) for num in numbers][1:]
            minimized_components_input_id.append(components_input_id)
        if (len(minimized_components_input_id)) > 1:
            input_id = minimized_components_input_id[0]
            for i in range(1, len(minimized_components_input_id)):
                input_id += minimized_components_input_id[i]
            minimized_components_input_id = input_id
        if (len(minimized_components_input_id)) == 1:
            minimized_components_input_id = minimized_components_input_id[0]
        print(minimized_components_input_id)




        # Writing minimized components in a csv file
        file_path = path_inputset_init.rsplit(".", 1)[0] + "_components_minimized.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        # path_to_output = os.path.join(path_subclasses, '..', filename)

        refData_dir_parent = os.path.dirname(path_subclasses)
        path_to_output = os.path.join(refData_dir_parent, filename)

        Minimizer.write_list_to_csv_comp(path_to_output, minimized_components_input_id)
        print("Minimization step successfully terminated.")
        print("The result is written in: " + str(path_to_output))
        if verbose:
            print("selected inputs gathered in solution")
        return self.minimized_inputset

# mimizer.search_solution()
# inputIds = [input.inputId for input in minimizer.solution]
# inputIds.sort()

def search_inputs():
    args = get_args()
    path_inputset_init = args.path_inputset_init
    path_output = args.path_output
    path_to_cost = args.path_cost
    sut = args.sut
    compute_diagnostics = args.causes
    verbose = args.verbose

    outputClusteringAlgorithm = args.output_clustering_algorithm
    outputClusteringDistance = args.distance_function
    actionClusteringAlgorithm = args.action_clustering_algorithm

    #step1: preprocessing
    if sut.lower() in ['jenkins']:
        RefineInputs.Classes.preProc(path_output, path_inputset_init)
    if sut.lower() in ['joomla']:
        preProc_joomla(path_output, path_inputset_init)

    # step2: OutputClustering
    file_path = path_inputset_init.rsplit(".", 1)[0] + "_preprocessed.csv"

    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)

    # refData_path = os.path.join(os.path.realpath(path_inputset_init), '..', filename)

    refData_dir_parent = os.path.dirname(os.path.realpath(path_inputset_init))
    refData_path = os.path.join(refData_dir_parent, filename)


    # refData_path = os.path.join(path_output, '..', 'refData.csv')
    # print(refData_path)


    if str(outputClusteringAlgorithm).lower() in ['hdbscan','all']:
        if str(outputClusteringDistance).lower() in ['lev', 'levenshtein', 'levenstein', 'all']:
                call_doubleClustering(refData_path, 'HDBSCAN', 'Lev',actionClusteringAlgorithm, path_inputset_init, path_to_cost, compute_diagnostics, verbose)
        if str(outputClusteringDistance).lower() in ['bag', 'all']:
                call_doubleClustering(refData_path, 'HDBSCAN', 'Bag',actionClusteringAlgorithm , path_inputset_init, path_to_cost, compute_diagnostics, verbose)

    if str(outputClusteringAlgorithm).lower() in ['kmeans', 'k-means', 'all']:
        if str(outputClusteringDistance).lower() in ['bag', 'all']:
                call_doubleClustering(refData_path, 'KMEANS', 'Bag',actionClusteringAlgorithm, path_inputset_init, path_to_cost, compute_diagnostics, verbose)
        if str(outputClusteringDistance).lower() in ['lev', 'levenshtein', 'levenstein', 'all']:
                call_doubleClustering(refData_path, 'KMEANS', 'Lev',actionClusteringAlgorithm, path_inputset_init, path_to_cost, compute_diagnostics, verbose)

    if str(outputClusteringAlgorithm).lower() in ['dbscan', 'all']:
        if str(outputClusteringDistance).lower() in ['lev', 'levenshtein', 'levenstein', 'all']:
                call_doubleClustering(refData_path, 'DBSCAN', 'Lev',actionClusteringAlgorithm, path_inputset_init, path_to_cost, compute_diagnostics, verbose)
        if str(outputClusteringDistance).lower() in ['bag', 'all']:
                call_doubleClustering(refData_path, 'DBSCAN', 'Bag',actionClusteringAlgorithm, path_inputset_init, path_to_cost, compute_diagnostics, verbose)



def call_doubleClustering(refData_path, outputClusteringAlgorithm, outputClusteringDistance, actionClusteringAlgorithm ,
                   path_inputset_init, path_to_cost, compute_diagnostics, verbose):


    sys.argv = [
        '', refData_path,
        '-o', outputClusteringAlgorithm,
        '-d', outputClusteringDistance
    ]
    # print('sys.arg: '+str(outputClusteringAlgorithm)+', '+str(outputClusteringDistance)+', '+str(actionClusteringAlgorithm))
    outputClustering.outputClustering()

    #step3: call action clustering

    folder_name = outputClusteringDistance+'_'+outputClusteringAlgorithm
    # path_to_output = os.path.join(refData_path, '..',folder_name, 'outputs_classes.csv')

    refData_dir_parent = os.path.dirname(refData_path)
    file_path = refData_path.rsplit("_", 1)[0] + "_classes.csv"
    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)
    path_to_output = os.path.join(refData_dir_parent, folder_name, filename)




    if actionClusteringAlgorithm.lower() in ['hdbscan', 'all']:
        ActionClustering.Classes.actionClustering_Hdbscan.urlDist(refData_path, path_to_output)
        # step4: call minimizer
        call_minimizer(path_to_cost, path_inputset_init, compute_diagnostics, verbose)

    if actionClusteringAlgorithm.lower() in ['kmeans', 'k-means', 'all']:
        ActionClustering.Classes.actionClustering_Kmeans.urlDist(refData_path, path_to_output)
        # step4: call minimizer
        call_minimizer(path_to_cost, path_inputset_init, compute_diagnostics, verbose)
    if actionClusteringAlgorithm.lower() in ['dbscan', 'all']:
        ActionClustering.Classes.actionClustering_Dbscan.urlDist(refData_path, path_to_output)
        # step4: call minimizer
        call_minimizer(path_to_cost, path_inputset_init, compute_diagnostics, verbose)



def call_minimizer(path_to_cost, path_inputset_init, compute_diagnostics, verbose):
    # initialize minimizer, then search inputs in solution
    path_subclasses = os.environ['OUTPUT_PATH']
    # path_subclasses = r'C:\Users\nbaya076\Dropbox\GitHub\Examples\RunningExample\lev_Kmeans\Kmeans\inputset_subclasses.csv'
    # print(path_subclasses)
    minimizer = Minimizer(path_subclasses, path_to_cost, verbose=verbose)
    minimized_inputset = minimizer.search_solution(path_inputset_init, path_subclasses, compute_diagnostics=compute_diagnostics)
    # input IDs are used to gather minimized input set from initial input set
    inputIds = [input.inputId for input in minimized_inputset]
    inputIds.sort()
    if len(inputIds) == 0:
        inputIdsStr = "None"
    else:
        inputIdsStr = str(inputIds[0])
        for i in range(1, len(inputIds)):
            inputIdsStr += ", " + str(inputIds[i])
    if verbose:
        print(len(minimized_inputset), "inputs selected:", inputIdsStr)
    if verbose:
        percentage_removed = 1.0 - len(minimized_inputset) / len(minimizer.inputs)
        print(100 * percentage_removed, "% of the initial input set was removed")

    # file_path = path_inputset_init.rsplit(".", 1)[0] + "_minimized_IDs.txt"
    # # Split the file path into directory and file components
    # directory, filename = os.path.split(file_path)
    # # path_to_output = os.path.join(path_subclasses, '..', filename)
    #
    # refData_dir_parent = os.path.dirname(path_subclasses)
    # path_to_output = os.path.join(refData_dir_parent, filename)
    #
    #
    # Minimizer.write_list_to_txt(path_to_output, inputIds)

    # convert input IDs into a json file containing the selected inputs
    postProcInfo = processor.postProc( path_inputset_init, inputIds, path_subclasses)
    path_inputset_final = postProcInfo.finalInputSetFilePath
    print("minimized input set written in", path_inputset_final)






def get_args():
    parser = argparse.ArgumentParser(
        prog='inputminimizer',
        description='initial input set'
    )
    parser.add_argument('path_inputset_init',
        metavar='INITIAL_INPUTSET_PATH',
        help='relative path to the initial input set json file')
    parser.add_argument('path_output',
        metavar='OUTPUT_PATH',
        help='relative path to the output file .txt')

    parser.add_argument('path_cost',
                        metavar='COST_PATH',
                        help='relative path to the cost csv file')

    parser.add_argument('-o', '--output-clustering-algorithm',
                        type=str,
                        default='all',
                        help='optional argument for the clustering algorithm, by default it executes all')

    parser.add_argument('-d', '--distance-function',
                        type=str,
                        default='all',
                        help='optional argument for the distance function, by default it executes all')

    parser.add_argument('-a', '--action-clustering-algorithm',
                        type=str,
                        default='all',
                        help='optional argument for the action clustering algorithm, by default it executes all')
    parser.add_argument('-s', '--sut',
                        type=str,
                        help='system under test')
    parser.add_argument('-c', '--causes',
        action='store_true',
        help='compute diagnostics on why inputs were removed')

    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='display execution information in the console')
    return parser.parse_args()

# minimize-inputs inputset.json outputs.txt costs.csv -d Levenshtein -o Kmeans -a Kmeans -v

# is not executed if the module is imported
if __name__ == "__main__":
    search_inputs()
