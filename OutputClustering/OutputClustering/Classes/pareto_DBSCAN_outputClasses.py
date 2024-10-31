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
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_samples, silhouette_score
from pymoo.optimize import minimize
from pymoo.model.problem import Problem
from pymoo.algorithms.nsga2 import NSGA2
import pandas as pd
import warnings
warnings.filterwarnings("ignore")


class pareto_Dbscan():

    def init(self,  distance_matrix):
        self.distance_matrix = distance_matrix
        # probwrap = ProblemWrapper(distance_matrix)
        global own
        own = copy.deepcopy(self)
        own.__dict__.update(self.__dict__)
        xu = len(distance_matrix)

        X = np.arange(1, 2, 1)
        Y = np.arange(4.8, 7, 1)
        X, Y = np.meshgrid(X, Y)
        Z1 = np.zeros(X.shape)
        Z2 = np.zeros(X.shape)

        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                a = X[i, j]
                b = Y[i, j]
                # Z1[i,j] , Z2[i,j]= benchmarks.kursawe((X[i,j],Y[i,j]))
                Z1[i, j], Z2[i, j] = pareto_Dbscan.benchmarks_Dbscan(self, X[i, j], Y[i, j])

        xu = len(distance_matrix)


        problem = ProblemWrapper(n_var=2, n_obj=2, xl=[1, 4], xu=[4.8, 10])


        algorithm = NSGA2(pop_size=30)
        stop_criteria = ('n_gen', 30)

        results = minimize(
            problem=problem,
            algorithm=algorithm,
            termination=stop_criteria
        )



        res_data = results.F.T

        return  results.F, results.X




    def benchmarks_Dbscan(self, n, eps):
        distance_matrix = own.distance_matrix

        n = int(n)

        if n> len(distance_matrix):
            n = len(distance_matrix)-1
        clusterer = DBSCAN(eps=eps, min_samples=int(n), metric='precomputed')
        # Fit the clusterer to the distance matrix
        clusterer.fit(distance_matrix)
        # Get the cluster labels for each datapoint
        labels = clusterer.labels_
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
            print("nan value detected")
            # res.append(np.array([(1,0)]))
        else:
            for design in designs:
                a = design[0]
                # res.append(benchmarks.kursawe(design))
                res.append(pareto_Dbscan.benchmarks_Dbscan(self,design[0], design[1]))
                # fitness.append((3*res[0]+res[1],0))

            out['F'] = np.array(res)


