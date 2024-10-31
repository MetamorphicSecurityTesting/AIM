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


import copy
import numpy as np
from ActionClustering.Classes import *
from sklearn.metrics import silhouette_samples, silhouette_score
from pymoo.optimize import minimize
from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
import pandas as pd
import warnings
warnings.filterwarnings("ignore")
from pymoo.configuration import Configuration
Configuration.show_compile_hint = False


class pareto_kmeans_action():

    def init(self,  distance_matrix):
        self.distance_matrix = distance_matrix
        # probwrap = ProblemWrapper(distance_matrix)
        global own
        own = copy.deepcopy(self)
        own.__dict__.update(self.__dict__)
        xu = len(distance_matrix)
        if xu <= 10:
            X = np.arange(1, xu-1, 1)
        else:
            X = np.arange(1, 10, 1)


        # X = np.meshgrid(X,1)
        Z1 = np.zeros(X.shape)
        Z2 = np.zeros(X.shape)

        for i in range(X.shape[0]):
            # print("Xshape:")
            # print(X.shape[0])
            a = X[i]
            # print(a)
            # Z1[i,j] , Z2[i,j]= benchmarks.kursawe((X[i,j],Y[i,j]))
            Z1[i], Z2[i] = pareto_kmeans_action.benchmarks_kmeans(self,X[i])

        xu = len(distance_matrix)
        # print("xu: "+ str(xu-1))

        problem = ProblemWrapper(n_var=1, n_obj=2, xl=[1], xu=[xu-1])


        algorithm = NSGA2(pop_size=5)
        stop_criteria = ('n_gen', 5)

        results = minimize(
            problem=problem,
            algorithm=algorithm,
            termination=stop_criteria)

        # print(results.F)
        #
        # print(results.X)

        res_data = results.F.T
        # print(res_data)
        return  results.F, results.X

        #
        # problem = ProblemWrapper()
        #
        # algorithm = NSGA2(pop_size=100)
        # stop_criteria = ('n_gen', 100)
        #
        # results = minimize(
        #     problem=problem,
        #     algorithm=algorithm,
        #     termination=stop_criteria
        # )
        #
        # print(results.F)
        #
        # print(results.X)
        #
        # res_data = results.F.T
        # print(res_data)



    def benchmarks_kmeans(self, n):
        distance_matrix = own.distance_matrix
        # print(n)
        # if str(n) == 'nan':
        #     print("nulllll")

        n = int(n)
        # print(n)
        if n> len(distance_matrix):
            n = len(distance_matrix)-1
        clusterer = Main.KMeansWithDistanceMatrix(n_clusters=n)
        # Fit the clusterer to the distance matrix
        clusterer.fit(distance_matrix)
        # Get the cluster labels for each datapoint
        labels = clusterer.labels_
        # print(labels)
        # print(distance_matrix)
        if labels.any() == np.zeros(len(labels)).any():
            return -1,0
        else:
            silhouette_avg = -1 * silhouette_score(distance_matrix, labels, metric='precomputed')
            # Compute the silhouette scores for each sample

            sample_silhouette_values = silhouette_samples(distance_matrix, labels, metric='precomputed')
            sample_silhouette_values = sample_silhouette_values + abs(np.min(sample_silhouette_values))
            # gini_coef.append(silAnalysis.gini( sample_silhouette_values))
            total = 0
            for i, xi in enumerate(sample_silhouette_values[:-1], 1):
                total += np.sum(np.abs(xi - sample_silhouette_values[i:]))
            gini_coef = total / (len(sample_silhouette_values) ** 2 * np.mean(sample_silhouette_values))
            return silhouette_avg, gini_coef



class ProblemWrapper(Problem):
    def _evaluate(self, designs, out, *args, **kwargs):
        res =[]

        if np.isnan(designs).any():
            # print("designsss:")

            # print(designs)
            # print("nan value detected")
            res = np.nan_to_num(designs)
            res2 = []
            for i in res:
                res2.append((0, 1))
            res = res2
            # res.append(np.array([(1,0)]))
        else:
            for design in designs:
                res.append(pareto_kmeans_action.benchmarks_kmeans(self,design[0]))

        out['F'] = np.array(res)





