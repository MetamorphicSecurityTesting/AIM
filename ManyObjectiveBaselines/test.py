import sys
from MOBaselines.MOSA import run_MOSA
from MOBaselines.NSGA3 import run_NSGA3
from MOBaselines import Greedy

# For executing MOSA please use the following code:
argument_sets = [
['', r'./ReducedInputs/Jenkins/Bag_DBSCAN/Kmeans/reduced_inputs.csv',
        r'./ReducedInputs/Jenkins/Bag_DBSCAN/Kmeans/inputset_action_subclasses.csv',
        r'./ReducedInputs/Jenkins/costs.csv']
]

for args in argument_sets:
    sys.argv = args
    run_MOSA.main()


# For executing NSGA-III please use the following code:
argument_sets = [
['', r'./ReducedInputs/Jenkins/Bag_DBSCAN/Kmeans/reduced_inputs.csv',
        r'./ReducedInputs/Jenkins/Bag_DBSCAN/Kmeans/inputset_action_subclasses.csv',
        r'./ReducedInputs/Jenkins/costs.csv']
]

for args in argument_sets:
    sys.argv = args
    run_NSGA3.main()


#For executing Greedy algorithm please use the following code:
argument_sets = [
['', r'./ReducedInputs/Jenkins/Bag_DBSCAN/Kmeans/reduced_inputs.csv']
]
for args in argument_sets:
    sys.argv = args
    Greedy.main()




