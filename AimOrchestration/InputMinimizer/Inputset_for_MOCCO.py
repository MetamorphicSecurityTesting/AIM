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
import pandas as pd
import sys
import numpy as np
import time

def main():
    start_time= time.time()
    args = get_args()
    file_path = args.path_subclass
    cost_path = args.path_cost
    # Load the CSV file
    df = pd.read_csv(file_path, sep='	')

    # Group by 'id' and collect unique 'SubClass' values for each 'id'
    id_subclass_mapping = df.groupby('id')['SubClass'].apply(lambda x: sorted(set(x))).reset_index()

    # Convert the DataFrame to a dictionary for easier interpretation
    id_subclass_dict = id_subclass_mapping.set_index('id')['SubClass'].to_dict()

    # Print the result
    # for id, subclasses in id_subclass_dict.items():
    #     print(f"id = {id} covered SubClasses: {subclasses}")

    grouped_df =  pd.DataFrame(list(id_subclass_dict.items()), columns=['id', 'SubClass'])


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
    # df_sorted.set_index('id', inplace=True)
    a = cost[4:len(cost)]
    b = df_sorted.loc[0:len(df_sorted) - 5, 'cost']
    df_sorted.loc[0:len(df_sorted) - 5, 'cost'] = cost[4:len(cost)]

    # Convert SubClass lists to sets in string format
    df_sorted['SubClass'] = df_sorted['SubClass'].apply(lambda x: '{' + ', '.join(map(str, x)) + '}')

    # Reorder columns to id, cost, SubClass
    df_sorted = df_sorted[['id','cost', 'SubClass']]

    file_path = file_path.rsplit(".", 1)[0] + "inputset_component.csv"

    # Split the file path into directory and file components
    directory, filename = os.path.split(file_path)

    output_path = os.path.join(os.path.realpath(directory), "subclass_components.csv")
    # refData_path = os.path.join(path_output, '..', 'refData.csv')
    # df_sorted.to_csv(output_path, header= False, index=True)
    # Write the DataFrame to the CSV file line by line and append 'new component'
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for index, row in df_sorted.iterrows():
            csv_writer.writerow([int(row['id']), int(row['cost']), row['SubClass']])
        csv_writer.writerow(['new component'])


    end_time = time.time()
    execution_time = end_time - start_time
    # Construct the output file path

    output_file = os.path.join(os.path.realpath(directory), "time.txt")

    # Save the execution time to the output file
    with open(output_file, "w") as file:
        file.write(f"Execution Time: {execution_time} seconds")

    print(f"Execution time saved to {output_file}")







def get_args():
    parser = argparse.ArgumentParser(
        prog='inputreducer',
        description='initial input set for MOCCO'
    )

    parser.add_argument('path_subclass',
        metavar='SUBCLASS_PATH',
        help='path to the csv file of action subclasses')

    parser.add_argument('path_cost',
                        metavar='COST_PATH',
                        help='relative path to the cost csv file')

    return parser.parse_args()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_csv>")
        sys.exit(1)

    input_file_path = sys.argv[1]
    main(input_file_path)
