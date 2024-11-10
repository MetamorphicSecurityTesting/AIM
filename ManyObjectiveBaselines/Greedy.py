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


import pandas as pd
import os
import csv
import argparse

class Node:
    def __init__(self, input_id, cost, coverage):
        self.id = input_id  # Input ID
        self.cost = cost  # Input cost
        self.coverage = coverage  # Input coverage
        self.next = None  # Pointer to the next node


# LinkedList class to manage the linked list
class LinkedList:
    def __init__(self):
        self.head = None  # Initialize the head of the list to None

    # Method to append a new node to the linked list
    def append(self, input_id, cost, coverage):
        new_node = Node(input_id, cost, coverage)
        if not self.head:
            self.head = new_node  # If the list is empty, set the head to the new node
        else:
            current = self.head
            while current.next:  # Traverse to the last node
                current = current.next
            current.next = new_node  # Append the new node at the end of the list

    # Method to find a node by id and return its cost and coverage
    def find(self, input_id):
        current = self.head
        while current:
            if current.id == input_id:  # If the id matches, return the corresponding node
                return current
            current = current.next
        return None  # If not found, return None

def string_to_set(data):
    a_cleaned = data.strip('{}').split(',')
    # Step 2: Convert the elements into integers and create a set
    input_cover = set(map(lambda x: (float(x.strip())), a_cleaned))
    return input_cover

def write2csv(data , directory, file_name):
    output_path = os.path.join(os.path.realpath(directory), file_name)
    with open(output_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        for element in data:
            csv_writer.writerow([element])

def main():
    args = get_args()
    reduced_input_path = args.path_reduced_inputset
    final_cost=0
    data = pd.read_csv(reduced_input_path, sep=',', header=None).dropna()

    # Apply the function to the column
    data[2] = data[2].apply(string_to_set)

    data = data.groupby(0, as_index=False).agg({
        1: 'first',  # Keep the first occurrence of column 1 values
        2: lambda sets: set().union(*sets)  # Merge the sets of floats in column 2
    })

    data.to_csv(reduced_input_path, index=False, header=None)
    coverages = list(data[2])
    ids = list(data[0].astype(float))
    costs = list(data[1].astype(float))

    # Initialize the linked list
    linked_list = LinkedList()

    # Populate the linked list with values from the lists
    for i in range(len(ids)):
        linked_list.append(ids[i], costs[i], coverages[i])

    # Example: Find a node with input_id == 1 and print its attributes
    input_id = 1
    result_node = linked_list.find(input_id)
    data = pd.read_csv(reduced_input_path, sep=',', header=None).dropna()
    allInputs = set(data[0].astype(float))
    converted_sets = [set(map(lambda x: float(float(x)), s.strip('{}').split(','))) for s in set(data[2])]
    # Step 2: Merge all sets into one
    remainingObjectivesToCover = set.union(*converted_sets)
    selectedInputs = set()
    while remainingObjectivesToCover != set():
        costEffectiveness = {}
        for input in (allInputs - selectedInputs):
            input_node = linked_list.find(input)
            costEffectiveness[input_node.id] = len(remainingObjectivesToCover & input_node.coverage)/input_node.cost

        chosenInput = max(costEffectiveness, key=costEffectiveness.get)
        selectedInputs.add(chosenInput)
        result_node = linked_list.find(chosenInput)
        remainingObjectivesToCover -= result_node.coverage
        final_cost =  final_cost + result_node.cost
    # print(sorted(selectedInputs))
    # print(final_cost)

    file_path = reduced_input_path.rsplit(".", 1)[0] + "greedy.csv"
    directory, filename = os.path.split(file_path)
    write2csv(selectedInputs, directory, "Greedy_minimized_inputset.csv")
    print("The result is written in: "+ str(directory)+'/'+"Greedy_minimized_inputset.csv")





def get_args():
    parser = argparse.ArgumentParser(
        prog='inputreducer',
        description='initial input set for Random search'
    )
    parser.add_argument('path_reduced_inputset',
                        metavar='REDUCED_INPUTSET_PATH',
                        help='path to the  reduced input set')

    return parser.parse_args()


if __name__ == "__main__":
    main()
