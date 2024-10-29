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
# from ActionClustering import *

from pandas import read_csv
import pandas as pd
from IMPRO import Input as ImproInput
from IMPRO import InputSet
# import Inputset_for_MOCCO
import os
import numpy as np
import csv



class reducer:

    def write_list_to_txt(file_path, data_list):
        with open(file_path, 'w') as txtfile:
            for item in data_list:
                txtfile.write(str(item) + ' ,')

    def write_list_to_csv(file_path, data_list):
        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            for item in data_list:
                csv_writer.writerow([item.inputId])

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

        # df = df_sorted
        # df = read_csv(r'./results/inputset_classes_impro.csv', sep='	')
        # df['id'] = df['id'].astype(int)

        inputs = []
        for i in range(df_sorted.__len__()):
            inputId = int(i+1)
            cost = int(df_sorted['cost'].iloc[i])
            coverEntry = df_sorted['SubClass'].iloc[i]
            cover = reducer.str2set(self,coverEntry)
            input = ImproInput(inputId, cost, cover)
            inputs.append(input)
        self.inputs = inputs

    def search_solution(self,path_subclasses, compute_diagnostics = True):
        verbose = self.verbose
        # initialize then reduce the problem
        inputSet = InputSet(self.inputs, verbose = verbose)
        compute_diagnostics = True
        necessary_inputs, components = inputSet.reduce_problem(compute_diagnostics = compute_diagnostics, verbose = verbose)
        diagnostics = inputSet.get_diagnostics()
        if compute_diagnostics:
            diagnostics = inputSet.get_diagnostics()
            print("diagnostics =", diagnostics)
        # solve the problem on each component and gather the results
        self.minimized_inputset = necessary_inputs# necessary inputs have to be part of the solution
        # print(self.minimized_inputset.diagnostics[22])

        # writing neseccary inputs in a csv file
        file_path = path_subclasses.rsplit("_", 2)[0] + "_necessary.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        # path_to_output = os.path.join(path_subclasses, '..', filename)

        refData_dir_parent = os.path.dirname(path_subclasses)
        path_to_output = os.path.join(refData_dir_parent, filename)
        reducer.write_list_to_csv(path_to_output, necessary_inputs)


        # Writing components in a csv file
        file_path = path_subclasses.rsplit("_", 2)[0] + "_components.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        # path_to_output = os.path.join(path_subclasses, '..', filename)

        refData_dir_parent = os.path.dirname(path_subclasses)
        path_to_output = os.path.join(refData_dir_parent, filename)
        reducer.write_list_to_csv_set(path_to_output, components)
        print("Reduction step successfully terminated.")
        print("The result is written in: " + str(path_to_output))
        return self.minimized_inputset

# mimizer.search_solution()
# inputIds = [input.inputId for input in minimizer.solution]
# inputIds.sort()







def call_minimizer():
    args = get_args()
    path_subclass = args.path_subclass
    path_to_cost = args.path_cost
    verbose = args.verbose

    # initialize minimizer, then search inputs in solution
    path_subclasses = path_subclass
    # path_subclasses = r'C:\Users\nbaya076\Dropbox\GitHub\Examples\RunningExample\lev_Kmeans\Kmeans\inputset_subclasses.csv'

    minimizer = reducer(path_subclasses, path_to_cost, verbose=verbose)
    minimized_inputset = minimizer.search_solution( path_subclasses, compute_diagnostics=False)
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




def get_args():
    parser = argparse.ArgumentParser(
        prog='inputreducer',
        description='initial input set'
    )

    parser.add_argument('path_subclass',
        metavar='OUTPUT_PATH',
        help='relative path to the output file .txt')

    parser.add_argument('path_cost',
                        metavar='COST_PATH',
                        help='relative path to the cost csv file')

    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='display execution information in the console')
    return parser.parse_args()

# minimize-inputs inputset.json outputs.txt costs.csv -d Levenshtein -o Kmeans -a Kmeans -v

# is not executed if the module is imported
if __name__ == "__main__":
    call_minimizer()
