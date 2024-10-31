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

# from pymoo.optimize import minimize
# from pymoo.model.problem import Problem
# from pymoo.algorithms.nsga2 import NSGA2
# import collections.abc
# #hyper needs the four following aliases to be done manually.
# collections.Iterable = collections.abc.Iterable
# collections.Mapping = collections.abc.Mapping
# collections.MutableSet = collections.abc.MutableSet
# collections.MutableMapping = collections.abc.MutableMapping
# #Now import hyper
# import hyper
# import abydos.distance as ad
# import numpy as np
# import hdbscan
# import pandas as pd
# import warnings
# warnings.filterwarnings("ignore")
#
# df = pd.read_csv('FinalData.csv', sep='	')
# for i in range(df['output'].__len__()):
#     if str(df['output'][i]) == 'nan':
#         df['output'][i] = ''
# data = df['output']
# n = len(data)
# distance_matrix = np.zeros((n, n))
# for i in range(len(data)):
#     print(i)
#     for j in range(i + 1, len(data)):
#         a = data[i].split()
#         b = data[j].split()
#         distance_matrix[i, j] = ad.bag(data[i].split(), data[j].split())
#         distance_matrix[j, i] = distance_matrix[i, j]
#
#
# from sklearn.cluster import DBSCAN
# from sklearn.metrics import silhouette_samples, silhouette_score
#
# def benchmarks_Hdbscan(n):
#     n = int(n)
#
#     clusterer = hdbscan.HDBSCAN(min_cluster_size=n, metric='precomputed')#allow_single_cluster=True
#     # Fit the clusterer to the distance matrix
#     clusterer.fit(distance_matrix)
#     # Get the cluster labels for each datapoint
#     labels = clusterer.labels_
#     silhouette_avg = -1 * silhouette_score(distance_matrix, labels, metric='precomputed')
#     # Compute the silhouette scores for each sample
#
#     sample_silhouette_values = silhouette_samples(distance_matrix, labels, metric='precomputed')
#     sample_silhouette_values = sample_silhouette_values + abs(np.min(sample_silhouette_values))
#     # gini_coef.append(silAnalysis.gini( sample_silhouette_values))
#     total = 0
#     for i, xi in enumerate(sample_silhouette_values[:-1], 1):
#         total += np.sum(np.abs(xi - sample_silhouette_values[i:]))
#     gini_coef = total / (len(sample_silhouette_values) ** 2 * np.mean(sample_silhouette_values))
#     return silhouette_avg , gini_coef
#
#
#
#
#
# X = np.arange(2, 12, 1)
#
# # X = np.meshgrid(X,1)
# Z1 = np.zeros(X.shape)
# Z2 = np.zeros(X.shape)
#
# for i in range(X.shape[0]):
#         a = X[i]
#         # Z1[i,j] , Z2[i,j]= benchmarks.kursawe((X[i,j],Y[i,j]))
#         Z1[i], Z2[i] = benchmarks_Hdbscan(X[i])
#
# class ProblemWrapper(Problem):
#     def _evaluate(self, designs, out, *args, **kwargs):
#         res =[]
#         for design in designs:
#             a = design[0]
#             # res.append(benchmarks.kursawe(design))
#             res.append(benchmarks_Hdbscan(design[0]))
#         out['F'] = np.array(res)
#
# problem = ProblemWrapper(n_var=1, n_obj=2, xl=[2], xu=[12])
#
# algorithm = NSGA2(pop_size=50)
# stop_criteria = ('n_gen', 50)
#
# results = minimize(
#     problem=problem,
#     algorithm=algorithm,
#     termination=stop_criteria
# )
#
# print(results.F)
# print(results.X)
# res_data = results.F.T
# print(res_data)
#
# # import plotly.graph_objects as go
# # fig = go.Figure(data=go.Scatter(x=res_data[0], y = res_data[1]))
# # fig.show()
