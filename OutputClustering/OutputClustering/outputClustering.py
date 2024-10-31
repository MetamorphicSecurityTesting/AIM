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

import argparse

import OutputClustering.Classes.outputClustering_Dbscan as dbscan
import OutputClustering.Classes.outputClustering_Hdbscan as hdbscan
import OutputClustering.Classes.outputClustering_Kmeans as kmeans

class outputClustering:
    def __init__(self):
        # get the arguments
        args = get_args()
        refData_dir = args.RefinedInputSetPath
        outputClusteringAlgorithm = args.output_clustering_algorithm
        distanceFunction = args.distance_function

        verbose = args.verbose
        if verbose:
            print("Output clustering")
        # call the desired clustering algorithm



        if str(outputClusteringAlgorithm).lower() in ['kmeans', 'k-means']:
            if verbose:
                print("start K-means algorithm")
            outCl = kmeans.clustering(refData_dir, distanceFunction)

        elif str(outputClusteringAlgorithm).lower() in ['dbscan']:
            if verbose:
                print("start DBSCAN algorithm")
            outCl = dbscan.clustering(refData_dir, distanceFunction)

        elif str(outputClusteringAlgorithm).lower() in ['hdbscan']:
            if verbose:
                print("start HDBSCAN algorithm")
            outCl = hdbscan.clustering(refData_dir, distanceFunction)

        elif str(outputClusteringAlgorithm).lower() in ['all']:
            if verbose:
                print("start all algorithms")
            outCl = hdbscan.clustering(refData_dir, distanceFunction)
            outCl = dbscan.clustering(refData_dir, distanceFunction)
            outCl = kmeans.clustering(refData_dir, distanceFunction)

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
    parser.add_argument('-o', '--output-clustering-algorithm',
        type=str,
        default='all',
        help='optional argument for the clustering algorithm, by default it executes all')

    parser.add_argument('-d', '--distance-function',
                        type=str,
                        default='all',
                        help='optional argument for the distance function, by default it executes all')


    parser.add_argument('-v', '--verbose',
                        action='store_true',
                        help='display execution information in the console')
    return parser.parse_args()


def main():
    outputClustering()


if __name__ == "__main__":
    main()
