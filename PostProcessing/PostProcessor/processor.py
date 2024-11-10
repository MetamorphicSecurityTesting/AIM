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


class postProc:
    def __init__(self,  initialInputSetFilePath, sorted_inputIds, subClassPath):


        # input to be read from the cmd
        minimized_inputs_IDs = sorted_inputIds
        file_path= initialInputSetFilePath.rsplit(".", 1)[0] + "_minimized.json"

        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)

        # Get the file name without the extension (last name)
        # last_name = os.path.splitext(filename)[0]
        refData_dir_parent = os.path.dirname(subClassPath)
        self.finalInputSetFilePath = os.path.join(refData_dir_parent, filename)

        # open the json file of initial inputs
        initial_input = postProc.readFromJson(self, initialInputSetFilePath)
        # Define the minimized input set:
        minimized_input_dict ={}
        self.minimized_input_dict = minimized_input_dict
        postProc.inspector(self, minimized_inputs_IDs, initial_input)
        postProc.WriteToJson(self)
        reqired_toBe_cleaned= postProc.readFromJson(self, self.finalInputSetFilePath)

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



def main():
    minimized_inputs_IDs = [2, 3, 5, 7, 9, 10, 33, 34, 37, 38, 51, 53, 54, 56, 61, 64, 75, 76, 79, 87, 88, 93, 96, 99,
                            104, 108, 114, 117, 119, 120, 121, 122, 123, 125, 129, 132, 134, 135, 139, 141, 147, 150, 151, 154, 156, 157, 159]
    # postProc(minimized_inputs_IDs)

# is not executed if the module is imported
if __name__ == "__main__":
    main()
