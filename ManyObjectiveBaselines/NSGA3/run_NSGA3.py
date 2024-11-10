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


from MOBaselines.NSGA3 import NSGA3
import sys
import argparse

def main():
    args = get_args()
    Subclass_file_path = args.path_subclass
    cost_path = args.path_sorted_cost
    reduced_input_path = args.path_reduced_inputset
    time_budget = args.budget
    NSGA3.NSGA3.main(reduced_input_path=reduced_input_path, Subclass_file_path=Subclass_file_path, cost_path=cost_path, time_budget= time_budget)

def get_args():
    parser = argparse.ArgumentParser(
        prog='inputreducer',
        description='initial input set for NSGA-3'
    )
    parser.add_argument('path_reduced_inputset',
                        metavar='REDUCED_INPUTSET_PATH',
                        help='path to the csv file of action subclasses')

    parser.add_argument('path_subclass',
        metavar='SUBCLASS_PATH',
        help='path to the csv file of action subclasses')

    parser.add_argument('path_sorted_cost',
                        metavar='SORTED_COST_PATH',
                        help='relative path to the cost csv file')

    parser.add_argument('-b', '--budget',
                        type=int,
                        default=600,
                        help='time budget (in seconds)'
                        )

    return parser.parse_args()


if __name__ == "__main__":
    main()
