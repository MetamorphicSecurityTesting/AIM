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


import csv
import os
import argparse
import time

import pandas as pd
import sys
import numpy as np


def ensure_new_component_last(df):
    # Check if there's any row with ID equal to 'new component'
    new_component_exists = df[0].eq('new component').any()

    if new_component_exists:
        # Move the row with ID 'new component' to the end
        new_component_row = df[df[0] == 'new component']
        df = df[df[0] != 'new component']
        df = pd.concat([df, new_component_row], ignore_index=True)
    else:
        # Add a new row with ID 'new component' at the end
        new_component_row = pd.DataFrame({'id': ['new component']})
        df = pd.concat([df, new_component_row], ignore_index=True)

    return df

def main():
    start_time = time.time()
    args = get_args()
    oracle_file = args.path_MOCCO_inputs
    necessary_inputs_path = args.path_necessary_input
    components_inputs_path = args.path_impro_components
    # Load the CSV file
    oracle_df = pd.read_csv(oracle_file, sep=',', header= None)
    necessary_inputs = pd.read_csv(necessary_inputs_path, sep='	', header= None)
    components_inputs = pd.read_csv(components_inputs_path, sep=',', header= None)

    oracle_df[0] = oracle_df[0].astype(str)
    necessary_inputs[0] = necessary_inputs[0].astype(str)
    components_inputs[0] = components_inputs[0].astype(str)

    # result = oracle_df[oracle_df[0].isin(necessary_inputs[0])]
    result = pd.merge(necessary_inputs, oracle_df, left_on=0, right_on=0)

    combined = pd.concat([result, components_inputs]).drop_duplicates(subset=[0]).reset_index(drop=True)
    combined = combined.drop_duplicates(subset=[0])
    combined = ensure_new_component_last(combined)
    print("")

    #
    # # Reorder columns to id, cost, SubClass
    # df_sorted = combined[['id','cost', 'SubClass']]

    file_path = oracle_file.rsplit(".", 1)[0] + "inputset_component.csv"

    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)

    output_path = os.path.join(os.path.realpath(directory), "reduced_inputs.csv")
    # refData_path = os.path.join(path_output, '..', 'refData.csv')

    combined.to_csv(output_path, header= False, index=False)
    # # Write the DataFrame to the CSV file line by line and append 'new component'
    # with open(output_path, 'w', newline='') as csvfile:
    #     csv_writer = csv.writer(csvfile)
    #     for index, row in df_sorted.iterrows():
    #         csv_writer.writerow([int(row['id']), int(row['cost']), row['SubClass']])
    #     csv_writer.writerow(['new component'])
    end_time = time.time()
    execution_time = end_time - start_time
    # Construct the output file path

    output_file = os.path.join(os.path.realpath(directory), "MergeTime.txt")

    # Save the execution time to the output file
    with open(output_file, "w") as file:
        file.write(f"Execution Time: {execution_time} seconds")

    print(f"Execution time saved to {output_file}")


def get_args():
    parser = argparse.ArgumentParser(
        prog='inputreducer',
        description='initial input set for MOCCO'
    )

    parser.add_argument('path_MOCCO_inputs',
        metavar='MOCCO_input_PATH',
        help='path to the csv file of action subclasses minimized')

    parser.add_argument('path_necessary_input',
                        metavar='NECESSARY_INPUT_PATH',
                        help='relative path to the cost csv file')

    parser.add_argument('path_impro_components',
                        metavar='IMPRO_COMPONENTS_PATH',
                        help='relative path to the IMPRO components')

    return parser.parse_args()


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <path_to_csv>")
        sys.exit(1)
    main()
