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

from typing import Union

Value = Union[int, float]

# this normalization function computes x -> x / (x + 1)
# it normalizes a range of value from [0, infinity) to [0, 1) while preserving the order, i.e., if val1 <= val2 then normalize(val1) <= normalize(val2)
def normalize(value: Value) -> float:
    return value/(value + 1.0)

# this function is similar to normalize as it computes x -> 1 / (x + 1), so normalize_opposite(x) = 1 - normalize(x)
# it normalizes a range of value from [0, infinity) to (0, 1] while reverting the order, i.e., if val1 <= val2 then normalize(val1) >= normalize(val2)
def normalize_complement(value: Value) -> float:
    return 1.0/(value + 1.0)
