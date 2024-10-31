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

collections.Iterable = collections.abc.Iterable
collections.Mapping = collections.abc.Mapping
collections.MutableSet = collections.abc.MutableSet
collections.MutableMapping = collections.abc.MutableMapping
import hyper
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances
import warnings
warnings.filterwarnings("ignore")

class KMeansWithDistanceMatrix(KMeans):
    def __init__(self, n_clusters=90, init='k-means++', n_init=20, max_iter=500,
                 tol=1e-4, verbose=0, random_state=None, copy_x=True,
                algorithm='lloyd'):
        super().__init__(n_clusters=n_clusters, init=init, n_init=n_init, max_iter=max_iter,
                         tol=tol, verbose=verbose, random_state=random_state, copy_x=copy_x,
                       algorithm=algorithm)

    def fit(self, X, y=None, sample_weight=None):
        # Convert distance matrix to feature matrix
        X = pairwise_distances(X, metric='precomputed')
        return super().fit(X, y=y, sample_weight=sample_weight)

