/*******************************************************************************
 * Copyright (c) University of Ottawa 2022-2024
 * Created by Nazanin Bayati (n.bayati@uottawa.ca),  Yoann Marquer (yoann.marquer@uni.lu)
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
 

from MOCCO.Classes.class_input import Input
from MOCCO.Classes.class_individual import Individual


# inputId, cost, cover
inputA = Input('A', 42, {'a', 'b'})# not considered
inputB = Input('B', 98, {'b', 'c'})# neighbor with high cost
inputC = Input('C', 10, {'c', 'd'})# added
inputD = Input('D', 99, {'d', 'e'})# neighbor with high cost
inputE = Input('E', 33, {'e', 'f'})# not considered
reduce_individual = Individual([inputA, inputB, inputC, inputD, inputE])
                
neighbors = reduce_individual.get_neighbors()
reduce_considered_inputs = [inputC] + neighbors[inputC.inputId]

# inputB and inputD are removed
gain = 98 + 99
reduce_groundTruth = ([inputA, inputC, inputE], gain)
