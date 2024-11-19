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
input5 = Input(5, 179, set(['33']))
input117 = Input(117, 87, set(['23']))
input119 = Input(119, 110, set(['23', '24']))
input120 = Input(120, 252, set(['23', '24', '33']))
example2_population = Population(Individual([input5, input117, input119, input120]))

test2_groundTruth = {input120}
