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


import os
import numpy as np
from sklearn.cluster import DBSCAN
import pandas as pd
from Levenshtein import distance as lev
from ActionClustering.Classes.pareto_DBSCAN_actionSet import pareto_Dbscan
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

class urlDist:
    def __init__(self,refined_data,OutputClasses_dir):
        # Dbscan_lev_eps=4.92_n=1_march10_withMethod.csv
        # Dbscan_bag_eps=4.5_n=1_march10_withMethod.csv
        # Kmeans_lev_k=42_march10_withMethod.csv
        # Kmeans_bag_k=40_march10_withMethod.csv

        print("DBSCAN is running for Action Clustering")
        df = pd.read_csv(OutputClasses_dir, sep='	')
        # df = pd.read_csv('lev_Kmeans_outputClasses.csv', sep='	')
        self.df = df
        urlDist.actionSet(self, refined_data, df, OutputClasses_dir)


    def actionSet(self, refined_data, df, OutputClasses_dir):
        self.df = df
        # sort df based on the labels
        # actionSet=[]
        d = {"sequence":[],
                    "url":[],
                    "index":[],"user":[],
                    "output": [],
                    "labels": [],
                    "parameter": [],
                    "method": [],
                    "SubClass": []
                    }
        df_final = pd.DataFrame(data=d)
        self.df_final = df_final
        df.sort_values(by=['labels'])
        # get the output classes

        counter = 0
        for i in range (max(df['labels'])+1):
            # actionSet = df.loc[df['labels'] == i]
            array = ['post', '0']
            array1=['get']
            actionSet_post = df.loc[(df['labels'] == i) & df['method'].isin(array)]
            actionSet_get =  df.loc[(df['labels'] == i) & df['method'].isin(array1)]

            # apply clustering with my distance function and get the labels
            actionSet_post['url'] = actionSet_post['url'].fillna('')
            actionSet_get['url'] = actionSet_get['url'].fillna('')


            if len(actionSet_post) > 1:
                urlDist.Dbscan(self, actionSet_post)

            if len(actionSet_get) > 1:
                urlDist.Dbscan(self, actionSet_get)

            if len(actionSet_post) == 1:
                actionSet_post['SubClass'] = [int(0)]
                urlDist.sortLabels(self, actionSet_post)

            if len(actionSet_get) == 1:
                actionSet_get['SubClass'] = [int(0)]
                urlDist.sortLabels(self, actionSet_get)



        # write to csv
        # Specify the name of the new folder
        folder_name = "DBSCAN"
        # Create a Path object representing the new folder

        refData_dir_parent = os.path.dirname(OutputClasses_dir)
        folder_path = os.path.join(refData_dir_parent,folder_name)
        # Check if the folder already exists before creating it
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)


        file_path = refined_data.rsplit("_", 1)[0] + "_action_subclasses.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        path_to_output = os.path.join(folder_path, filename)
        self.df_final.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')

        print("Action clustering successfully terminated.")
        print("The result is written in: "+str(folder_path))
        os.environ['OUTPUT_PATH'] = path_to_output

    def Dbscan(self, actionSet):

        # Calculate the pairwise Levenshtein distances between the strings
        data = actionSet['url']
        param = actionSet['parameter']
        distances = np.zeros((len(data), len(data)))
        for i in range(len(data)):

            for j in range(i + 1, len(data)):
                a = list(data)[i]
                b = list(data)[j]
                distances[i, j] = urlDist.urlDistFunc(self, list(data)[i], list(data)[j], list(actionSet['parameter'])[i], list(actionSet['parameter'])[j])
                distances[j, i] = distances[i, j]
        self.distance_matrix = distances
        dis = np.zeros(len(data))
        if distances.any() == np.zeros((len(data), len(data))).any():
            actionSet['SubClass'] = np.zeros(len(data))
            urlDist.sortLabels(self, actionSet)

        else:
            resF, resX = pareto_Dbscan.init(self,distances)

            if resF != [[]]:
                a = np.array(resF[:,0])

                index = np.where(a == a.min())
                index = index[0]
                if len(index)>1:
                    index = index[0]
                n_clusters = int(resX[index,0])
                eps = (resX[index, 1])


            clusterer = DBSCAN(eps=eps, min_samples=int(n_clusters), metric='precomputed')  # lev = 54 bag = 59        #pareto  lev = 57 , bag =63
            clusterer.fit(distances)
            labels = clusterer.labels_
            # Get the cluster assignments for each string

            actionSet['SubClass'] = labels

            # seperator = actionSet.head(1)
            urlDist.sortLabels(self, actionSet)



    def urlDistFunc(self,url1,url2, param1, param2):
        url1=url1.split('/')
        url1 = list(filter(lambda x: x != "", url1))
        url2=url2.split('/')
        url2 = list(filter(lambda x: x != "", url2))

        i = 0
        while url1.__len__()>0 and url2.__len__()>0 and url1[i]==url2[i]:
            url1.pop(i)
            url2.pop(i)

        dist = url1.__len__()+url2.__len__()
        paramDist = 0

        if str(param1) == 'nan': param1 = ''
        if str(param2) == 'nan': param2 = ''
        if param1 != param2 and len(param1) > 0 and len(param2)>0:
            paramDist = lev(param1,param2)
            paramDist = paramDist/(paramDist+1)

        if param1 != param2 and (param1.__len__() > 0 or param2.__len__() > 0):
            paramDist = 1



        return dist + paramDist

    def sortLabels(self,actionSet):
        if self.df_final.size == 0:
            counter = 0
        else:
            counter = max(self.df_final['SubClass'])+1
        list_subclass_labels = actionSet['SubClass']
        sorted_labels = list_subclass_labels.sort_values()

        if actionSet.size > 1:
            for i in range(len(sorted_labels) - 1):
                b = sorted_labels.iloc[i+1]
                if sorted_labels.iloc[i+1]-sorted_labels.iloc[i]==0 or sorted_labels.iloc[i+1]-sorted_labels.iloc[i]==1:
                    continue
                else:
                    a = sorted_labels.iloc[i + 1]
                    b = sorted_labels.iloc[i]+1
                    sorted_labels = sorted_labels.replace(sorted_labels.iloc[i + 1], sorted_labels.iloc[i]+1)
                    list_subclass_labels = list_subclass_labels.replace(to_replace=a, value=b)


        if min(list_subclass_labels) == 0:
            list_subclass_labels = list_subclass_labels + counter
        else:
            mini = min(list_subclass_labels)
            list_subclass_labels = list_subclass_labels + counter - mini
        actionSet['SubClass'] = list_subclass_labels
        self.df_final = pd.concat([self.df_final, actionSet])



# urlDist(r'C:\Users\nbaya076\Dropbox\GitHub\Examples\RunningExample\bag_HDBSCAN\outputClasses.csv')
