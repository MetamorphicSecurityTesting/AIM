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
from MOCCO.Classes.class_population import Population


# inputId, cost, cover
input56 = Input(56, 229, set(['49']))
input150 = Input(150, 294, set(['18', '19']))
input151 = Input(151, 300, set(['18', '19', '49']))
example1_population = Population(Individual([input56, input150, input151]))

test1_groundTruth = {input151}
