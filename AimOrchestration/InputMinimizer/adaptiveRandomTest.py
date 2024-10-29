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
import argparse
import pandas as pd
import ActionClustering
from ActionClustering import *
from PostProcessor import processor
from pandas import read_csv
from IMPRO import Input as ImproInput
from IMPRO import InputSet
from MOCCO import Input as GeneticInput
from MOCCO import Individual, Population
from PostProcessor import processor
import sys
import os
import numpy as np
import csv
import re
import datetime

def adaptiveRandomeTest():  

    current_time = datetime.datetime.now()
    print("Current time:", current_time)
    args = get_args()
    # path_inputset_init = args.path_inputset_init
    path_refinedOutput = args.path_refinedOutput
    actionClusteringAlgorithm = args.action_clustering_algorithm
    verbose = args.verbose

    # # Split the file path into directory and file components
    # directory, filename = os.path.split(path_inputset_init)
    # initData_dir_parent = os.path.dirname(os.path.realpath(path_inputset_init))
    # initData_path = os.path.join(initData_dir_parent, filename)

    directory, filename = os.path.split(path_refinedOutput)
    refData_dir_parent = os.path.dirname(os.path.realpath(path_refinedOutput))
    refData_path = os.path.join(refData_dir_parent, filename)


    # step1: set all the data into one output class add "labels" zero for all the coloumns

    df = read_csv(refData_path, sep='	')
    df['labels']=0  # Replace 'len(df)' with the desired number of rows

    file_path = refData_path.rsplit("_", 1)[0] + "_outputClass.csv"
    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)
    path_to_output = os.path.join(refData_dir_parent, filename)
    df.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')
    print("Output clustering successfully terminated.")
    print("The result is written in: " + str(path_to_output))

    if actionClusteringAlgorithm.lower() in ['hdbscan', 'all']:
        ActionClustering.Classes.actionClustering_Hdbscan.urlDist(refData_path, path_to_output)
        # step4: random selection of each action class
        randomSelection()

    if actionClusteringAlgorithm.lower() in ['kmeans', 'k-means', 'all']:
        ActionClustering.Classes.actionClustering_Kmeans.urlDist(refData_path, path_to_output)
        # step4: random selection of each action class
        randomSelection()

    if actionClusteringAlgorithm.lower() in ['dbscan', 'all']:
        ActionClustering.Classes.actionClustering_Dbscan.urlDist(refData_path, path_to_output)
        # step4: random selection of each action class
        randomSelection()

def randomSelection():
    path_subclasses = os.environ['OUTPUT_PATH']
    # Assuming 'df' is your existing DataFrame
    df = read_csv(path_subclasses, sep='	')
    # Grouping the DataFrame by the 'classes' column
    grouped_df = df.groupby('SubClass')

    selected_ids=[]
    # Now, you can print the values of the 'id' column for each group
    for group_name, group_df in grouped_df:
        ids_in_group = group_df['id'].tolist()
        unique_list_ids = list(set(ids_in_group))
        # Randomly select a value from the list
        random_id = random.choice(unique_list_ids)
        selected_ids.append(int(random_id))
        print("Randomly selected value:", random_id)
    print(selected_ids)

    dir_parent = os.path.dirname(os.path.realpath(path_subclasses))
    file_path = os.path.join(dir_parent, "inputset_minimized_IDs_art.txt")
    print(file_path)
    writeToTxt(file_path, selected_ids)



def writeToTxt(file_path, id_list):
    # Open the file in write mode
    with open(file_path, 'w') as file:
        # Write the list elements in a single line separated by a comma
        file.write(', '.join(map(int, id_list)))

def get_args():
    parser = argparse.ArgumentParser(
        prog='inputART',
        description='initial input set'
    )
    # parser.add_argument('path_inputset_init',
    #     metavar='INITIAL_INPUTSET_PATH',
    #     help='relative path to the initial input set json file')
    parser.add_argument('path_refinedOutput',
        metavar='REF_OUTPUT_PATH',
        help='relative path to the output file .txt')


    parser.add_argument('-a', '--action-clustering-algorithm',
                        type=str,
                        default='all',
                        help='optional argument for the action clustering algorithm, by default it executes all')
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
    adaptiveRandomeTest()
