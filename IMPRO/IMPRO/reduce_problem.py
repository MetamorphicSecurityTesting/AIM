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

from .Tests.test0 import inputSet0, groundTruth0
from .Tests.test1 import inputSet1, groundTruth1
from .Tests.test2 import inputSet2, groundTruth2
from .Tests.test3 import inputSet3, groundTruth3
from .Tests.run_tests import run_test

# for the available tests, reduce the problem then compare the result with ground truth
def main():
    # test 0
    inputSet0.reduce_problem(compute_diagnostics = True)
    verdict0 = run_test(inputSet0, groundTruth0)
    # test 1
    inputSet1.reduce_problem(compute_diagnostics = True)
    verdict1 = run_test(inputSet1, groundTruth1)
    # test 2
    inputSet2.reduce_problem(compute_diagnostics = True)
    verdict2 = run_test(inputSet2, groundTruth2)
    # test 3
    inputSet3.reduce_problem(compute_diagnostics = True)
    verdict3 = run_test(inputSet3, groundTruth3)

# is not executed if the module is imported
if __name__ == "__main__":
    main()
