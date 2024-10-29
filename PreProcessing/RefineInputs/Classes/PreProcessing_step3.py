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


from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.tokenize import word_tokenize
import re
import pandas as pd
import os
import io
import ast
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import sys
import numpy as np
import json
import warnings
warnings.filterwarnings("ignore")
# word_tokenize accepts
# a string as an input, not a file.
class preProc_step3:
    def __init__(self, refdata_step2,target_dir, input_json, output):
        # print("70% is completed!")

        # df = pd.read_csv('./refData3_march10.csv', sep='	')
        # df = pd.read_csv(refdata_step2, sep='	')
        df = refdata_step2
        # my_list = [''] * 1232
        # df['parameter'] = my_list
        input_path = input_json
        df['method'] = ''
        df['id'] = ''
        df['parameter'] = ''
        # df = refdata_step2
        for i in range(df['output'].__len__()):
            if str(df['output'][i]) == 'nan':
                df['output'][i] = ''

            df = preProc_step3.getParameter(self, df)
            sequence_list = str(df["sequence"][i])
            # sequence_list = ast.literal_eval(df_sequence)
            # Extract the URLs from the sequence_list
            a = sequence_list[3:-3].replace('[','').replace(']','').replace('\"','\'')
            a = sequence_list.replace('[', '').replace(']', '').replace('\"', '\'')
            df["sequence"][i] = '['+'\''+a+'\''+']'



        with open(input_json, 'r') as json_file:
            data = json.load(json_file)

        # preProc_step3.getMethod(self, df, target_dir, data, input_path, output)
        preProc_step3.RemovingStopWords(self, df, target_dir, data, input_path, output)


    def RemovingStopWords(self, df , target_dir, input_json, input_path, output):
        self.df = df
        stop_words = set(stopwords.words('english'))
        for o in range(df['output'].__len__()):

            if df['output'][o] != '':
                a = df['output'][o]


                df['output'][o] = df['output'][o].lower()
                df['output'][o]  = re.sub(r'\d+', '', df['output'][o] )
                word_tokens = word_tokenize(df['output'][o])
                # converts the words in word_tokens to lower case and then checks whether
                # they are present in stop_words or not
                word_tokens = [re.sub(r'[^\w\s]', '', w) for w in word_tokens]
                # re.sub(r'\d+', '', text)

                word_tokens = ' '.join(word_tokens)

                word_tokens = word_tokenize(word_tokens)

                filtered_sentence = [w for w in word_tokens if not w.lower() in stop_words]
                # with no lower case conversion

                filtered_sentence= ' '.join( filtered_sentence)

                df['output'][o] = filtered_sentence
                if df['output'][o].__contains__('welcome jenkins'):
                    df['output'][o] = df['output'][o].replace('welcome jenkins', '')


                string = df['output'][o]

                # Tokenize the string into words
                words = word_tokenize(string)

                # Initialize a PorterStemmer and a WordNetLemmatizer
                ps = PorterStemmer()
                wnl = WordNetLemmatizer()

                # Perform stemming and lemmatization on each word
                stemmed_words = [ps.stem(w) for w in words]
                lemmatized_words = [wnl.lemmatize(w) for w in words]


                df['output'][o] = ' '.join( lemmatized_words)


        preProc_step3.getMethod(self, df,target_dir, input_json, input_path, output)


    def getParameter(self, df):
        for s in range(df['sequence'].__len__()):
            len = 0
            if df['url'][s].__contains__('click on /'):
                continue
            else:
                len =(df['url'][s].split(' ')).__len__()
                a = df['url'][s]

                if df['url'][s].__contains__('log in'):
                    p = df['url'][s].split(' ')[3]
                    df['parameter'][s] = df['url'][s].split(' ')[3]

                df['url'][s] = df['url'][s].split(' ')[len-1]
        return df


    def getMethod(self,df,target_dir,input_json, input_path, output):

        # Extract the sequence of actions

        for i in range(df['sequence'].__len__()):

            a = df['sequence'][i]
            https_urls = re.findall(r'(http?://[^\s\]]+]?|click on /[\S\s]+?)', df['sequence'][i])

            # http_urls = re.findall(r'(http?://[^\s\]]+]?|click on /\S+)', df['sequence'][i])

            for hlen in range(len(https_urls)):
                if "click on " in https_urls[hlen]:
                    https_urls[hlen] = https_urls[hlen].replace("click on ", "")
            cleaned_urls = [url.rstrip("', ") for url in https_urls]
            cleaned_urls = [url.rstrip("']") for url in cleaned_urls]
            df['sequence'][i] = cleaned_urls

            # Managing the special cases
            if str(df['sequence'][i]) == "['http://192.168.56.103:8080/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/job/jobWithFileParam/', 'http://192.168.56.103:8080/job/jobWithFileParam/configure', 'http://192.168.56.103:8080/job/jobWithFileParam/configSubmit', 'http://192.168.56.103:8080/job/jobWithFileParam/build?delay=0sec', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/console', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/consoleText']" \
                    and (str(df['user'][i]) == 'admin' or (str(df['user'][i+1]) == 'admin' and str(df['user'][i]) == 'nan')):
                df['id'][i]= '159'
            elif str(df['sequence'][i]) =="['http://192.168.56.103:8080/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/job/jobWithFileParam/', 'http://192.168.56.103:8080/job/jobWithFileParam/configure', 'http://192.168.56.103:8080/job/jobWithFileParam/configSubmit', 'http://192.168.56.103:8080/job/jobWithFileParam/build?delay=0sec', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/console', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/consoleText']" and (str(df['user'][i]) == 'user2' or (str(df['user'][i+1]) == 'user2' and str(df['user'][i]) == 'nan')):
                df['id'][i] = '160'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/user/user1/my-views/view/all/builds', 'http://192.168.56.103:8080/user/user1/', 'http://192.168.56.103:8080/user/user1/api/', 'http://192.168.56.103:8080/me/api/xml?tree=jobsname,viewsname,jobsname']":
                df['id'][i] = '40'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/user/user1/my-views/view/all/builds', '/u']":
                df['id'][i] = '60'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/computer/slave1/', 'http://192.168.56.103:8080/computer/slave1/log', 'http://192.168.56.103:8080/computer/slave1/api/', 'http://192.168.56.103:8080/computer/slave1/api/json?tree=jobsname']":
                df['id'][i] = '67'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/computer/slave1/', 'http://192.168.56.103:8080/computer/slave1/log', 'http://192.168.56.103:8080/computer/slave1/api/', '/c']":
                df['id'][i] = '68'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/user/user1/my-views/view/all/builds', 'http://192.168.56.103:8080/user/user1/', 'http://192.168.56.103:8080/user/user1/api/', 'http://192.168.56.103:8080/me/api/xml?tree=jobsname,viewsname,jobsname', 'http://192.168.56.103:8080/me/api/xml?tree=jobs%5bname%5d,views%5bname,jobs%5bname%5d%5d']":
                df['id'][i] = '132'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/computer/slave1/', 'http://192.168.56.103:8080/computer/slave1/log', 'http://192.168.56.103:8080/computer/slave1/api/', 'http://192.168.56.103:8080/computer/slave1/api/json?tree=jobsname', 'http://192.168.56.103:8080/me/my-views/view/all/api/json?tree=jobs%5bname%5d']":
                df['id'][i] = '147'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/toggleCollapse?paneId=executors']" and (str(df['user'][i]) == 'user2' or (str(df['user'][i+1]) == 'user2' and str(df['user'][i]) == 'nan') or (str(df['user'][i+2]) == 'user2' and str(df['user'][i+1]) == 'nan' and str(df['user'][i]) == 'nan')):
                df['id'][i] = '110'

        for key, json_value in input_json.items():
            method =''
            sequence = []
            id =''

            for item in json_value:
                if 'url' in item:
                    sequence.append(item['url'])
                if 'elementURL' in item:
                    sequence.append(item['elementURL'])
                if 'method' in item:
                    method = item['method']
                id = key.split('path')[1]



            df['sequence'] = df['sequence'].apply(lambda x: [item.replace(' ', '') for item in x])
            mask = df['sequence'].apply(lambda x: sequence == x)
            mask_method = mask & (df['id'].isnull() | df['id'].eq(''))
            # Update the 'method' column for the matching rows
            df.loc[mask_method, 'method'] = method
            df.loc[mask_method, 'id'] = id


        for i, row in df.iterrows():
            if row['method'] == '' or pd.isnull(row['method']):
                matching_row = df[(df['url'] == row['url']) & (df.index != i) & (df['method'] != '')].head(1)
                if not matching_row.empty:
                    # df.at[i, 'url'] = matching_row['url'].values[0]
                    df.at[i, 'method'] = matching_row['method'].values[0]

        df['method'] = df['method'].replace(['', None, np.nan], 'get')

        for i in range (len(df['id'])):

            if str(df['sequence'][i]) == "['http://192.168.56.103:8080/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/job/jobWithFileParam/', 'http://192.168.56.103:8080/job/jobWithFileParam/configure', 'http://192.168.56.103:8080/job/jobWithFileParam/configSubmit', 'http://192.168.56.103:8080/job/jobWithFileParam/build?delay=0sec', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/console', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/consoleText']" and (
                    str(df['user'][i]) == 'admin' or (str(df['user'][i + 1]) == 'admin' and (str(df['user'][i]) == 'nan' or str(df['user'][i]) == ''))):
                df['id'][i] = '159'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/job/jobWithFileParam/', 'http://192.168.56.103:8080/job/jobWithFileParam/configure', 'http://192.168.56.103:8080/job/jobWithFileParam/configSubmit', 'http://192.168.56.103:8080/job/jobWithFileParam/build?delay=0sec', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/console', 'http://192.168.56.103:8080/job/jobWithFileParam/lastBuild/consoleText']" and (
                    str(df['user'][i]) == 'user2' or (str(df['user'][i + 1]) == 'user2' and (str(df['user'][i]) == 'nan' or str(df['user'][i]) == ''))):
                df['id'][i] = '160'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/user/user1/my-views/view/all/builds', 'http://192.168.56.103:8080/user/user1/', 'http://192.168.56.103:8080/user/user1/api/', 'http://192.168.56.103:8080/me/api/xml?tree=jobsname,viewsname,jobsname']":
                df['id'][i] = '40'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/user/user1/my-views/view/all/builds', '/u']":
                df['id'][i] = '60'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/computer/slave1/', 'http://192.168.56.103:8080/computer/slave1/log', 'http://192.168.56.103:8080/computer/slave1/api/', 'http://192.168.56.103:8080/computer/slave1/api/json?tree=jobsname']":
                df['id'][i] = '67'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/computer/slave1/', 'http://192.168.56.103:8080/computer/slave1/log', 'http://192.168.56.103:8080/computer/slave1/api/', '/c']":
                df['id'][i] = '68'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/user/user1/my-views/view/all/builds', 'http://192.168.56.103:8080/user/user1/', 'http://192.168.56.103:8080/user/user1/api/', 'http://192.168.56.103:8080/me/api/xml?tree=jobsname,viewsname,jobsname', 'http://192.168.56.103:8080/me/api/xml?tree=jobs%5bname%5d,views%5bname,jobs%5bname%5d%5d']":
                df['id'][i] = '132'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/me/my-views', 'http://192.168.56.103:8080/computer/slave1/', 'http://192.168.56.103:8080/computer/slave1/log', 'http://192.168.56.103:8080/computer/slave1/api/', 'http://192.168.56.103:8080/computer/slave1/api/json?tree=jobsname', 'http://192.168.56.103:8080/me/my-views/view/all/api/json?tree=jobs%5bname%5d']":
                df['id'][i] = '147'
            elif str(df['sequence'][i]) == "['http://192.168.56.103:8080/', '/', 'http://192.168.56.103:8080/j_acegi_security_check', 'http://192.168.56.103:8080/toggleCollapse?paneId=executors']" and (
                    str(df['user'][i]) == 'user2' or (str(df['user'][i + 1]) == 'user2' and str(df['user'][i]) == '') or (str(df['user'][i + 2]) == 'user2' and str(df['user'][i + 1]) == '' and str(df['user'][i]) == '')):
                df['id'][i] = '110'

        # Check for null values
        if df['id'].isnull().any():
            print("There are null values in the id column.")

        # Check for empty strings
        if any(column == '' for column in df['id']):
            print("There are empty values in the id column.")
        preProc_step3.writeToCsv(self, df, target_dir , input_path)
        preProc_step3.writeToCsv(self, df, target_dir, output)

    def writeToCsv(self, df, target_dir , input_json):
        # current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = input_json.rsplit(".", 1)[0] + "_preprocessed.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)

        refData_dir_parent = os.path.dirname(target_dir)
        path_to_output = os.path.join(refData_dir_parent, filename)
        df.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')


# preProc_step3(r'C:\Users\nbaya076\Dropbox\GitHub\Examples\Example1\RefinedInputSet.csv', r'C:\Users\nbaya076\Dropbox\GitHub\Examples\Example1\outputs1_preprocessed.csv',r'C:\Users\nbaya076\Dropbox\GitHub\Examples\Example1\inputset.json',r'C:\Users\nbaya076\Dropbox\GitHub\Examples\Example1\outputs.txt')
