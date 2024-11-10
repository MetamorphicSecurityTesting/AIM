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


from typing import Union, Set

# both should be immutable
InputId = Union[str, int]
CoverId = Union[str, int]

class Input:

    def __init__(self, inputId: InputId, cost: int, coveredEntities: Set[CoverId]):
        self.inputId = inputId
        if cost <= 0:
            raise ValueError("The cost of input", inputId, "should be > 0")
        self.cost = cost
        if len(coveredEntities) == 0:
            raise ValueError("Input", inputId, "should cover something.")
        self.cover = coveredEntities
    
    def __repr__(self):
        repr = f"<Input (id {id(self)}):\n"
        repr += f"   - inputId = {self.inputId},\n"
        repr += f"   - cost = {self.cost},\n"
        repr += f"   - cover = {self.cover}\n"
        repr += f">"
        return repr
