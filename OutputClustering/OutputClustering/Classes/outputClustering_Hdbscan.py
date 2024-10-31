
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

import collections.abc
#hyper needs the four following aliases to be done manually.
# import ActionClustering.Classes.actionClustering_Dbscan


collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
#Now import hyper
import hyper
# import abydos.distance as ad
import textdistance
import numpy as np
import pandas as pd
from Levenshtein import distance as lev
import hdbscan
import os
from OutputClustering.Classes.pareto_Hdbscan_outputClasses import pareto_hdbscan
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")
from pymoo.configuration import Configuration
Configuration.show_compile_hint = False

class clustering:
    def __init__(self,refData_dir,distance_function):
        print("HDBSCAN is running")
        df = pd.read_csv(refData_dir, sep='	')
        self.df = df
        # Create an empty distance matrix
        df_prun = df
        for i in range(df['output'].__len__()):
            if str(df['output'][i]) == 'nan':
                df['output'][i] = ''
                df_prun = df_prun.drop(i)
        df_prun = df_prun.reset_index()
        data = df['output']
        if str(distance_function).lower() in ['lev', 'levenshtein', 'levenstein']:
            clustering.HDbscan_lev(self, data, df, refData_dir)
        elif str(distance_function).lower() in ['bag']:
            clustering.HDbscan_bag(self, data, df, refData_dir)
        elif str(distance_function).lower() in ['all']:
            print("Executing HDBSCAN with Levenshtein distance")
            clustering.HDbscan_lev(self, data, df, refData_dir)
            print("Executing HDBSCAN with Bag distance")
            clustering.HDbscan_bag(self, data, df, refData_dir)
        # print("Done!")


    def Levenshtein_distance(self, data):
        # Calculate the pairwise Levenshtein distances between the strings
        distances = np.zeros((len(data), len(data)))
        for i in range(len(data)):
            # print(i)
            for j in range(i + 1, len(data)):
                distances[i, j] = lev(data[i].split(), data[j].split())
                distances[j, i] = distances[i, j]
        print("Lev distance is selected")
        return distances

    def Bag_distance(self, data):
        # Calculate the pairwise Bag distances between the strings
        distances = np.zeros((len(data), len(data)))
        for i in range(len(data)):
            # print(i)
            for j in range(i + 1, len(data)):
                distances[i, j] = textdistance.bag(data[i].split(), data[j].split())
                distances[j, i] = distances[i, j]
        print("Bag distance is selected")
        return distances

    def HDbscan_lev(self, data, df, refData_dir ):
        # Your data, which should be a list of strings or a dataframe
        self.df = df

        # Calculate the pairwise Levenshtein distances between the strings
        distances = clustering.Levenshtein_distance(self, data)

        self.distance_matrix = distances
        dis = np.zeros(len(data))
        # print("Getting the Hyper parameter value!")
        resF, resX = pareto_hdbscan.init(self, distances)
        if resF.size != 0 or  resF.any():
            a = np.array(resF[:, 0])

            index = np.where(a == a.min())
            index = index[0]
            minimum = 100
            if len(index) > 1:
                for i in index:
                    if resX[i, 0] < minimum:
                        minimum = resX[i, 0]
                        n_clusters = int(minimum)
            else:
                n_clusters = int(resX[index, 0])


        clusterer = hdbscan.HDBSCAN(min_cluster_size=2, metric='precomputed')  # allow_single_cluster=True
        clusterer.fit(distances)
        labels = clusterer.labels_

        df['labels'] = labels
        # Print the cluster labels
        self.labels = labels

        # write to csv
        # Specify the name of the new folder
        folder_name = "Lev_HDBSCAN"
        # Create a Path object representing the new folder
        folder_path = Path(folder_name)
        # Create the new folder
        if not folder_path.exists():
            folder_path.mkdir()

        refData_dir_parent = os.path.dirname(refData_dir)
        file_path = refData_dir.rsplit("_", 1)[0] + "_classes.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        path_to_output = os.path.join(refData_dir_parent, 'Lev_HDBSCAN',filename)
        df.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')
        print("Output clustering successfully terminated.")
        print("The result is written in: " + str(path_to_output))




    def HDbscan_bag(self, data, df, refData_dir):
        # Your data, which should be a list of strings or a dataframe
        self.df = df
        # Calculate the pairwise Bag distances between the strings
        distances = clustering.Bag_distance(self, data)

        self.distance_matrix = distances
        dis = np.zeros(len(data))
        # print("Getting the Hyper parameter value!")
        resF, resX = pareto_hdbscan.init(self, distances)
        if resF.size != 0 or  resF.any():
            a = np.array(resF[:, 0])

            index = np.where(a == a.min())
            index = index[0]
            minimum = 100
            if len(index) > 1:
                for i in index:
                    if resX[i, 0] < minimum:
                        minimum = resX[i, 0]
                        n_clusters = int(minimum)
            else:
                n_clusters = int(resX[index, 0])


        clusterer = hdbscan.HDBSCAN(min_cluster_size=2, metric='precomputed')  # allow_single_cluster=True
        clusterer.fit(distances)
        labels = clusterer.labels_

        df['labels'] = labels
        # Print the cluster labels
        self.labels = labels

        # write to csv
        # Specify the name of the new folder
        folder_name = "Bag_HDBSCAN"
        # Create a Path object representing the new folder
        folder_path = Path(folder_name)
        # Create the new folder
        if not folder_path.exists():
            folder_path.mkdir()
        refData_dir_parent = os.path.dirname(refData_dir)
        file_path = refData_dir.rsplit("_",1)[0] + "_classes.csv"
        # Split the file path into directory and file components
        directory, filename = os.path.split(file_path)
        path_to_output = os.path.join(refData_dir_parent, 'Bag_HDBSCAN',filename)
        df.to_csv(path_to_output, sep='\t', encoding='utf-8', header='true')

        print("Output clustering successfully terminated.")
        print("The result is written in: " + str(path_to_output))
