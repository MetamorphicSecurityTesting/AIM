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
import os.path

from pandas import read_csv
from IMPRO import Input as ImproInput
import pandas as pd
import numpy as np
import csv



def clean_inputs():
    args = get_args()
    path_subclasses = args.path_subclass
    cost_path = args.path_cost

    file_path = os.path.abspath(path_subclasses)
    # df = read_csv(path_subclasses, sep='	')
    df = pd.read_csv(path_subclasses, sep='	')
    df['SubClass'] = df['SubClass'].round().astype(str)

    # Group sequences by subclass and merge subclass values
    # grouped_df = df.groupby('sequence')['SubClass'].apply(','.join).reset_index()
    grouped_df = df.groupby(['sequence', 'id'])['SubClass'].apply(','.join).reset_index()
    df_sorted = grouped_df.sort_values('id', ascending=True)

    df_sorted['cost'] = ''

    cost_df = pd.read_csv(cost_path, sep=' ')
    # mainDF = pd.read_csv(r'C:\Users\nbaya076\Dropbox\GitHub\Examples\RunningExample\refData.csv', sep='  ')
    list_cost = cost_df.values
    list_cost = str(list_cost[0]).split('[')[1].split(']')[0].split('\'')[1].split(',')
    cost = np.array(list_cost)

    for i in range(0, cost.__len__()):
        if int(df_sorted['id'][i]) == 157:
            df_sorted['cost'][i] = cost[0]
        if int(df_sorted['id'][i]) == 158:
            df_sorted['cost'][i] = cost[1]
        if int(df_sorted['id'][i]) == 159:
            df_sorted['cost'][i] = cost[2]
        if int(df_sorted['id'][i]) == 160:
            df_sorted['cost'][i] = cost[3]
    df_sorted.set_index('id', inplace=True)
    a = cost[4:len(cost)]
    b = df_sorted.loc[1:len(df_sorted) - 4, 'cost']
    df_sorted.loc[1:len(df_sorted) - 4, 'cost'] = cost[4:len(cost)]


    # df = df_sorted
    # df = read_csv(r'./results/inputset_classes_impro.csv', sep='	')
    # df['id'] = df['id'].astype(int)

    # inputs = []
    # for i in range(df_sorted.__len__()):
    #     inputId = int(i+1)
    #     cost = int(df_sorted['cost'].iloc[i])
    #     coverEntry = df_sorted['SubClass'].iloc[i]
    #     cover = str2set(coverEntry)
    #     input = ImproInput(inputId, cost, cover)
    #     inputs.append(input)
    # data_list = inputs
    file_path = file_path.rsplit(".", 1)[0] + "inputset_prepared.csv"

    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)

    output_path = os.path.join(os.path.realpath(directory), "inputset_prepared.csv")
    # refData_path = os.path.join(path_output, '..', 'refData.csv')

    df_sorted.to_csv(output_path, index=False)
    # write_list_to_csv(file_path, data_list)



def get_args():
    parser = argparse.ArgumentParser(
        prog='inputminimizer',
        description='initial input set'
    )
    parser.add_argument('path_subclass',
        metavar='subclass_PATH',
        help='relative path to the initial input set json file')

    parser.add_argument('path_cost',
                        metavar='COST_PATH',
                        help='relative path to the cost csv file')


    return parser.parse_args()

# minimize-inputs inputset.json outputs.txt costs.csv -d Levenshtein -o Kmeans -a Kmeans -v

# is not executed if the module is imported
if __name__ == "__main__":
    clean_inputs()
