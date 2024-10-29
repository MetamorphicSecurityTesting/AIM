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


import argparse
from .Classes.PreProcesseing_step1 import preProc
from .Classes.Preprocessing_Joomla import preProc_joomla
from .Classes.PreProcessing_step2 import Rtestsuite

def main():
    # arguments
    args = get_args()
    input_json = args.sutInputsetJsonPath
    outputPath = args.sutOutputPath
    sut = args.sut
    # refOutputPath = args.sutRefOutputPath
    verbose = args.verbose
    # the processing is done in two steps
    if verbose:
        print("refine input set: step 1")
    if sut.lower() in ["", "jenkins"]:
        preProc(outputPath, input_json)
    if sut.lower() in ['joomla']:
        preProc_joomla(outputPath, input_json)
    # if verbose:
    #     print("refine input set: step 2")
    # pre2 = Rtestsuite(refOutputPath)

# parse arguments from command line
def get_args():
    parser = argparse.ArgumentParser(
        prog='preprocess',
        description='refine initial input set'
    )
    parser.add_argument('sutInputsetJsonPath',
                        metavar='SUT_INPUTSET_JSON_PATH',
                        help='relative path to the SUT inputset json file')
    parser.add_argument('sutOutputPath',
        metavar='SUT_OUTPUT_PATH',
        help='relative path to the SUT output file')

    # parser.add_argument('sutRefOutputPath',
    #     metavar='SUT_REF_OUTPUT_PATH',
    #     help='relative path to the SUT Refined output file')
    parser.add_argument('costPath',
                        metavar='COST_PATH',
                        help='relative path to the cost file')

    parser.add_argument('-s', '--sut',
                        type=str,
                        help='system under test')

    parser.add_argument('-v', '--verbose',
        action='store_true',
        help='display execution information in the console')
    return parser.parse_args()

if __name__ == "__main__":
    args = get_args()
    main()
