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


import json
import os
import pandas as pd
import csv
import argparse

class cmd_postProc:


    def __init__(self):

        args = get_args()
        initialInputSetFilePath = args.path_inputset_init
        inputID_path = args.path_inputID
        components_path = args.path_component


        inputs_IDs = []

        with open(inputID_path, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            for row in csv_reader:
                # 'row' is a list containing the values from each row in the CSV file
                inputs_IDs.append(row)
        inputs_IDs = [int(item[0]) for item in inputs_IDs]


        minimized_components =[]
        df = pd.read_csv(components_path, header=None)
        minimized_components = df[0].tolist()
        minimized_components = [x for x in minimized_components if x != 'new component']
        minimized_components = [int(item) for item in minimized_components]
        minimized_inputs_IDs = inputs_IDs + minimized_components
        minimized_inputs_IDs = sorted(minimized_inputs_IDs)

        # minimized_inputs_IDs =
        file_path= initialInputSetFilePath.rsplit(".", 1)[0] + "_minimized.json"

        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)

        # Get the file name without the extension (last name)
        # last_name = os.path.splitext(filename)[0]
        refData_dir_parent = os.path.dirname(components_path)
        self.finalInputSetFilePath  = os.path.join(refData_dir_parent, filename)

        # open the json file of initial inputs
        initial_input = cmd_postProc.readFromJson(self, initialInputSetFilePath)
        # Define the minimized input set:
        minimized_input_dict ={}
        self.minimized_input_dict = minimized_input_dict
        cmd_postProc.inspector(self, minimized_inputs_IDs, initial_input)
        cmd_postProc.WriteToJson(self)
        reqired_toBe_cleaned= cmd_postProc.readFromJson(self, self.finalInputSetFilePath)

    def inspector(self, minimized_inputs_IDs, initial_input):
        initial_input_keys_list = list(initial_input)
        for id in minimized_inputs_IDs:
            path_id = 'path'+str(id)
            if path_id in initial_input_keys_list:
                self.minimized_input_dict[path_id]= initial_input[path_id]

    def readFromJson(self, inputFile):
        with open(inputFile, 'r',encoding='utf-8') as json_file:
            initial_input = json.load(json_file)
        return initial_input

    def WriteToJson(self):

        with open(self.finalInputSetFilePath, 'w', encoding='utf-8') as json_file:
            json.dump( self.minimized_input_dict, json_file , indent=4, ensure_ascii=False)



# initialInputSetFilePath, inputID_path, components_path
def get_args():
    parser = argparse.ArgumentParser(
        prog='inputminimizer',
        description='initial input set'
    )
    parser.add_argument('path_inputset_init',
        metavar='INITIAL_INPUTSET_PATH',
        help='relative path to the initial input set json file')
    parser.add_argument('path_inputID',
        metavar='INPUT_ID_PATH',
        help='relative path to the input id. csv')

    parser.add_argument('path_component',
        metavar='COMPONENT_PATH',
        help='relative path to the component .csv')


    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='display execution information in the console')
    return parser.parse_args()




def main():
    cmd_postProc()

# is not executed if the module is imported
if __name__ == "__main__":
    main()


