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

import pandas as pd
import os
from RefineInputs.Classes.PreProcessing_step2 import *

class preProc:
    def __init__(self,target_dir, input_json):
       print("Starting Pre-processing")
       print("It will take a while...")
       # Access the file within the target directory
       # path_to_input = os.path.join(target_dir, 'output.txt')
       lines = preProc.read(self, target_dir)

       # Find the index where '******counter:0' appears
       split_index = next((i for i, line in enumerate(lines) if '*******Counter: 0' in line), None)

       # Check if '******counter:0' exists in the file
       if split_index is not None:
           # Split the lines into two parts based on the index
           lines_before_counter = lines[:split_index]
           lines_after_counter = lines[split_index:]

       lines = lines_before_counter
       refOutputlines = lines_after_counter
       preProc.clean(self,lines,target_dir,refOutputlines, input_json)
       a =  preProc.dataframe(self)



    def read(self,text):

        with open(text, 'r', encoding='iso-8859-1') as f:
            # content = f.read()
            # with open(text) as f:
            lines = f.readlines()
        return lines


    def dataExtraction(self, blocks,target_dir,refOutputlines, input_json):
        my_dict={"key":[]}
        seq_dict={"seq":[]}
        new_row = {"sequence": [], "url": [], "index": [], "user": [], "output": []}
        df = pd.DataFrame(new_row)
        counter = 1
        for box in blocks:
            username = ""
            sequence = ""
            index = ""
            output = ""
            outputIndex = 1000
            outputEnd = 0
            for i in range(0, box.__len__()):
                if box[i].startswith("username"):
                    username = box[i].lstrip('username: ')
                    username = username.replace("\n", '')
                    if username.__len__()==1:
                        username = 'user'+username
                    elif username == 'dmin':
                        username = 'admin'
                elif box[i].startswith("sequence"):
                    sequence = box[i].lstrip('sequence: ')
                    sequence = sequence.replace("\n", '')
                    url = sequence.split('],')
                elif box[i].startswith("position"):
                    index = box[i].lstrip('position: ')
                    index = index.replace("\n", '')
                    outputIndex = i+1

                elif i == outputIndex:
                    #if outputIndex ==  outputEnd or outputEnd == 0:
                        a = box[i].replace("\n", '')
                        if (box[i].replace('\n', '') != '') and  box.__len__()-i<=2:
                            output = box[i].replace("\n", '')
                            break

                        elif box[i+1].startswith("output o2:"):
                            if (box[i].replace('\n', '') != ''):
                                output = box[i].replace("\n", '')
                                break

                        #break
                       # elif box[i + 1]!= "output o2: $$$$$$$$$$$$$":
                        else:
                            res = []
                            while box[i] != 'output o2: $$$$$$$$$$$$$\n':
                                res.append(box[i])
                                i = i+1
                                if box[i].startswith('!!!!!') or i == box.__len__()-1:
                                    break
                            output = res
                            break

            if sequence!= "" and output !='':
               # new_row = {"sequence":[sequence], "url":[url[int(index)]],"index":[index], "user":[username], "output": [output]}

                newRow = [sequence,url[int(index)], index, username, output]
                value = sequence+index+username
                if sequence not in seq_dict.values():
                    seq_dict["seq"].append(sequence)
                if value not in my_dict.values() and username != "ANONYMOUS":
                    my_dict["key"].append(value)
                    df.loc[len(df.index)] = newRow
                counter = counter + 1
               # df.append(new_row)
        # preProc.writeToCsv(self,df,target_dir, refOutputPath, input_json)
        Rtestsuite(df,target_dir, refOutputlines, input_json)
        self.df = df
        preProc.dataframe(self)


    def dataframe(self):
        return self.df


    def clean(self, lines,target_dir,refOutputlines, input_json):

        blocks = []
        rows =[]
        flag = False
        for l in range(lines.__len__()-1):
            a = lines[l]
            if lines[l].startswith('*'):
                l = l+1

                flag = True
                blocks.append(rows)
                rows = []

            if flag == True:
                if lines[l].startswith('%'):
                    l = l + 1
                else:
                    rows.append(lines[l])
            if lines[l].startswith('MR tested with'): break

        preProc.dataExtraction(self, blocks,target_dir,refOutputlines, input_json)

    def writeToCsv(self, df, target_dir, refOutputPath,input_json):
  
        path_to_output = os.path.join(target_dir, '..', 'PreprocData_step1.csv')
        df.to_csv( path_to_output, sep='\t', encoding='utf-8', header='true')
        # Rtestsuite(df, refOutputPath,input_json)


# preProc( r'C:\Users\nbaya076\Dropbox\GitHub\Examples\Example1\outputs.txt',r'C:\Users\nbaya076\Dropbox\GitHub\Examples\Example1\inputset.json')


