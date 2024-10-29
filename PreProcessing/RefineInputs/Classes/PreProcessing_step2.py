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


import re
import pandas as pd
from unicodedata import normalize
import warnings
import os
# Disable the warning
warnings.filterwarnings("ignore")
from RefineInputs.Classes.PreProcessing_step3 import *


class Rtestsuite:

    def __init__(self,df, outputPath, target_dir,input_json):
        # print("30% is completed!")

        outputPath = os.path.realpath(outputPath)

        # current_dir = os.path.dirname(os.path.abspath(__file__))

        # path_to_dataComplete = os.path.join(target_dir, 'dataComplete3.csv')
        # path_to_outputRef = os.path.join(target_dir)

        # df = pd.read_csv(path_to_dataComplete, sep='	')
        self.df = df
        lines = target_dir #outputRef
        target_dir = outputPath
        Rtestsuite.clean(self, lines)
        Rtestsuite.preprocess(self,df)
        # print("50% is completed!")
        Rtestsuite.compare(self,self.df, self.refdf, target_dir,input_json, outputPath)

    def compare(self,df, refdf,target_dir,input_json, outputPath):
        self.df = df
        self.refdf = refdf
        flag = False
        for row in range(refdf['sequence'].__len__()):
            for mainrow in range(df['sequence'].__len__()):
               cc= refdf['user'][row]

               if refdf['sequence'][row] == df['sequence'][mainrow]:
                    a = refdf['url'][row]
                    b = df['url'][mainrow]
                    c = refdf['index'][row]
                    d = refdf['url'][row]
                    if refdf['url'][row] == 'access the index http://192.168.56.103:8080/':
                        output = "Jenkins Skip to content log in sign up Jenkins User: Password: Create an account if you are not a member yet.Page generated: Jan 30, 2023 2:31:33 AM CETREST APIJenkins ver. 2.121.1"
                        refdf['output'][row] = Rtestsuite.cleanOutput(self, output)
                        break

                    if refdf['url'][row] == df['url'][mainrow] and refdf['index'][row] == str(df['index'][mainrow]) :
                        # print(df['output'][mainrow])
                        output = df['output'][mainrow]
                        refdf['output'][row] = Rtestsuite.cleanOutput(self,output)
                        break
        # Rtestsuite.writeToCsv(self, refdf,target_dir,input_json)
        preProc_step3(refdf, target_dir, input_json, outputPath)
        # print("Refined InputSet is ready!")



    def preprocess(self,df):
        #{"sequence": [], "url": [], "index": [], "user": [], "output": []}
        self.df = df
        for mSeq in range (df['sequence'].__len__()):
            df['sequence'][mSeq] = Rtestsuite.cleanSeq(self, df['sequence'][mSeq].split('], '))
            # print(df['url'][mSeq])
            df['url'][mSeq] = df['url'][mSeq].split(' : ')
            if(df['url'][mSeq].__len__()==1):
                continue
            else:
                df['url'][mSeq] = df['url'][mSeq][1].replace(']', '')


    def read(self,text):
        with open(text) as f:
            lines = f.readlines()
        return lines

    def clean(self, lines):
        blocks = []
        rows = []
        flag = False
        counter = False
        for l in range(lines.__len__()):
            a = lines[l]
            if lines[l].startswith('*** Starting'):
                l = l + 1
            elif lines[l].startswith('!'):
                l = l + 1
            elif lines[l].startswith('*'):
                l = l + 1
                counter = True
                flag = True
                blocks.append(rows)
                rows = []

            if flag == True:
                if lines[l].startswith('Starting ChromeDriver') or lines[l].startswith('Only local') or lines[l].startswith('Please see https') \
                        or lines[l].startswith('ChromeDriver') or lines[l].startswith('Jan.') or lines[l].startswith('INFO: Detected') or counter :
                    l = l + 1
                    counter = False
                else:
                    rows.append(lines[l])
                    counter = False
            if lines[l].startswith('MR tested with'): break
       # print(blocks[len(blocks)-1])
        Rtestsuite.dataExtraction(self, blocks)

    def dataExtraction(self, blocks):
        a= blocks
        my_dict = {"key": []}
        seq_dict = {"seq": []}
        new_row = {"sequence": [], "url": [], "index": [], "user": [],"output":[]}
        refdf = pd.DataFrame(new_row)
        counter = 1
        for box in blocks:
            username = ""
            sequence = ""
            index = ""
            action = ""

            for i in range(0, box.__len__()):
                if box[i].startswith("username"):
                    username = box[i].lstrip('username: [Account: username=')
                    username = username.lstrip('pwd=')
                    username = username.lstrip(']\n')
                    username = username.split(" ")
                    username = username[0]
                    if username.__len__() == 1:
                        username = 'user' + username
                    elif username == 'min':
                        username = 'admin'
                    elif username == 'll':
                        username = ''

                elif box[i].startswith("sequence"):
                    sequence = box[i].lstrip('sequence: ')
                    sequence = sequence.replace("\n", '')
                    seqList = sequence.split('], ')
                    sequence = Rtestsuite.cleanSeq(self, seqList)

                elif box[i].startswith("position"):
                    index = box[i].lstrip('position: ')
                    index = index.replace("\n", '')

                elif box[i].startswith("action:"):
                    action = box[i].lstrip('action: ')
                    action = action.replace("\n", '')
                    action = action.split(' : ')
                    action = action[1].replace(']','')

                    if sequence != "":
                        # new_row = {"sequence":[sequence], "url":[url[int(index)]],"index":[index], "user":[username], "output": [output]}

                        newRow = [sequence, action, index, username,'']
                        value = str(sequence) + index + username
                        if sequence not in seq_dict.values():
                            seq_dict["seq"].append(sequence)
                        if value not in my_dict.values() :
                            my_dict["key"].append(value)
                            refdf.loc[len(refdf.index)] = newRow
                        counter = counter + 1

            # df.append(new_row)
      #  Rtestsuite.writeToCsv(self, refdf)
        self.refdf = refdf


    def cleanSeq(self, seqList):
        for s in range (seqList.__len__()):
           # print(seqList[s].split(" : "))
            seqList[s] = seqList[s].split(" : ")[1]
            if s ==0:
                temp = seqList[s]
                seqList[s] = '[' + temp

            if s == seqList.__len__()-1:
                temp = seqList[s]
                seqList[s] = '[' + temp
            else:
                temp = seqList[s]
                seqList[s] = '[' + temp + ']'

        return seqList

    def cleanOutput(self, output):

        # removing special characters
        output = str(output)
        output = output.replace(u'\\xa0', '')
        output = output.replace(u'\xa0', '')
        output = output.replace(' ','')
        output = normalize('NFKD', output)
        output = output.replace('â€˜', '')
        output = output.replace('Â»', '')

        # removing menue
        if output.__contains__('[Jenkins] Skip to content'):
            output = output.replace('[Jenkins] Skip to content','')
        if output.__contains__('ENABLE AUTO REFRESH Jenkins'):
            output = output.replace('ENABLE AUTO REFRESH Jenkins','')
        if output.__contains__('Back to Project Status Changes Console Output View Build Information Previous Build'):
            output = output.replace('Back to Project Status Changes Console Output View Build Information Previous Build','')
        if output.__contains__('Changes Console Output View Build Information Parameters People Build History Project Relationship Check File Fingerprint My Views Build Queue'):
            output = output.replace('Changes Console Output View Build Information Parameters People Build History Project Relationship Check File Fingerprint My Views Build Queue', '')
        if output.__contains__('New Item People Build History Project Relationship Check File Fingerprint Manage Jenkins My Views Credentials New View Build Queue'):
            output = output.replace('New Item People Build History Project Relationship Check File Fingerprint Manage Jenkins My Views Credentials New View Build Queue', '')
        if output.__contains__('New Item People Build History Project Relationship Check File Fingerprint Manage Jenkins My Views Credentials System New View Build Queue'):
            output = output.replace('New Item People Build History Project Relationship Check File Fingerprint Manage Jenkins My Views Credentials System New View Build Queue', '')
        if output.__contains__('New Item People Build History Project Relationship Check File Fingerprint New View Build Queue'):
            output = output.replace('New Item People Build History Project Relationship Check File Fingerprint New View Build Queue', '')
        if output.__contains__('Back to Dashboard Build Queue'):
            output = output.replace('Back to Dashboard Build Queue', '')
        if output.__contains__('Back to Dashboard Manage Jenkins New Node Configure Build Queue'):
            output = output.replace('Back to Dashboard Manage Jenkins New Node Configure Build Queue', '')
        if output.__contains__('Nodes slave1 Back to List Status Build History Load Statistics'):
            output = output.replace('Nodes slave1 Back to List Status Build History Load Statistics', '')
        if output.__contains__('Nodes slave1 Back to List Status Delete Agent Configure Build History Load Statistics'):
            output = output.replace('Nodes slave1 Back to List Status Delete Agent Configure Build History Load Statistics', '')
        if output.__contains__('People Build History Project Relationship Check File Fingerprint My Views Build Queue'):
            output = output.replace('People Build History Project Relationship Check File Fingerprint My Views Build Queue', '')
        if output.__contains__('People Status Builds Configure My Views Credentials'):
            output = output.replace('People Status Builds Configure My Views Credentials', '')
        if output.__contains__('Welcome Jenkins'):
            output = output.replace('Welcome Jenkins', '')


        # removing footer
        if output.__contains__('Not Found Powered by Jetty'):
            output = output.split('Reason:')[0]
        if output.__contains__('The document tree is shown below'):
            output = output.split('The document tree is shown below')[0]
        if output.__contains__('Build History of Jenkins'):
            output = output.split('Build History of Jenkins')[0]
        if output.__contains__('100Build History'):
            output = output.split('100Build History')[0]
        if output.__contains__('add description All + S'):
            output = output.split('add description All + S')[0]
        if output.__contains__('Build History on master'):
            output = output.split('Build History on master')[0]
        if output.__contains__('Time Since?'):
            output = output.split('Time Since?')[0]
        if output.__contains__('They are available at'):
            output = output.split('They are available at')[0]
        if output.__contains__('100 jobWithFileParam'):
            output = output.split('100 jobWithFileParam')[0]
        if output.__contains__('No recent builds failed.'):
            output = output.split('No recent builds failed.')[0]


        if output.__contains__('JenkinsJenkins at http://localhost:8080'):
            output = ''
        if output.__contains__('"temporarilyOffline"'):
            output = ''
        if output.__contains__('Number of executors not executing an'):
            output = ''

        #
        # Removing tags, footer, date and time
        if output.startswith('[\''):
            output = output.split('[\'')[1].split('\']')[0]
            output = output.split('Page generated:')[0]
        elif output.startswith('[\"'):
            output = output.split('[\"')[1].split('\']')[0]
            output = output.split('Page generated:')[0]
        else:
            output = output.split('Page generated:')[0]
        if output.startswith('<?xml version='):
            output = ''
        if output.startswith('{\n'):
            output = ''
        if output.startswith('SSHLauncher'):
            output = ''
        if output.__contains__('SSHLauncher'):
            output = output.split('SSHLauncher')[0]
        if output.startswith('<?xml version='):
            output = ''
        if output.startswith('java.io'):
            output = ''
        if output.startswith('{"'):
            output = ''
        if output.startswith("Started by user user2"):
                output = ''

        if str(output) == 'nan':
            output = ''
        output = [re.sub(r"\([a-zA-Z]+ [0-9]+, [0-9]+ ([0-9]+:)+[0-9]+ [A-Z]+\)", ' ', k) for k in output.split("\n")][0]
        output = [re.sub(r"([0-9]+(.[0-9]+)*) [yr|mo|day|hr|min|sec|ms]+", ' ', k) for k in output.split("\n")][0]
        # # output = [re.sub(r"[^a-zA-Z0-9]+", ' ', k) for k in output.split("\n")][0]
        # I have to remove the menue
        return output


    def writeToCsv(self, refdf, target_dir,input_json):

        # current_dir = os.path.dirname(os.path.abspath(__file__))
        path_to_output = os.path.join(target_dir, '..','RefinedInputSet.csv')
        refdf.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')
        preProc_step3(refdf, target_dir, input_json)



