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


import ActionClustering.Classes.actionClustering_Kmeans as kmeans
import ActionClustering.Classes.actionClustering_Dbscan as dbscan
import ActionClustering.Classes.actionClustering_Hdbscan as hdbscan
import argparse
import os
import sys


class actionClustering:
    def __init__(self):
        # get the arguments
        args = get_args()
        refined_data = args.RefinedInputSetPath
        OutputClasses_dir = args.OutputClassesPath
        clusteringAlgorithm = args.clustering_algorithm
        verbose = args.verbose
        if str(clusteringAlgorithm)=='': clusteringAlgorithm = 'all'

        if verbose:
            print("Action clustering")

        kmeans_list =['kmeans','k-means']
        if str(clusteringAlgorithm).lower() in kmeans_list:
            actCl = kmeans.urlDist(refined_data,OutputClasses_dir)

        elif str(clusteringAlgorithm).lower() in ['dbscan']:
            actCl = dbscan.urlDist(refined_data,OutputClasses_dir)

        elif str(clusteringAlgorithm).lower() in ['hdbscan']:
            actCl = hdbscan.urlDist(refined_data,OutputClasses_dir)

        elif str(clusteringAlgorithm).lower() in ['all']:
            actCl = kmeans.urlDist(refined_data,OutputClasses_dir)
            actCl = dbscan.urlDist(refined_data,OutputClasses_dir)
            actCl = hdbscan.urlDist(refined_data,OutputClasses_dir)
        else:
            raise ValueError("The selected algorithm is not supported.")
        
# parse arguments from command line
def get_args():
    parser = argparse.ArgumentParser(
        prog='preprocess',
        description='refine initial input set'
    )
    parser.add_argument('RefinedInputSetPath',
                        metavar='REFINED_INPUTSET_PATH',
                        help='relative path to the refined inputset')
    parser.add_argument('OutputClassesPath',
        metavar='OUTPUT_CLASSES_PATH',
        help='relative path to the SUT output file')
    parser.add_argument('-a', '--clustering-algorithm',
                        type=str,
                        default='all',
                        help='optional argument for the clustering algorithm, by default it executes all')

    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='display execution information in the console')
    return parser.parse_args()

def main():
    actionClustering()


if __name__ == "__main__":
    args = get_args()
    main()

