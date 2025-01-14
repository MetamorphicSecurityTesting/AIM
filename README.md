We have provided the following details regarding the AIM tool:

- [Prepare the Test Environment](#prepare-the-test-environment )
- [Perform Input set minimization](#perform-input-set-minimization)
- [Perform Input Set Minimization (step-by-step)](#perform-input-set-minimization-(step-by-step))
- [Evaluating the Tool: Key Metrics and Techniques](#evaluating-the-tool-key-metrics-and-techniques)
- [Generating Tables](#generating-tables)
- [How to Cite This Work](#how-to-cite-this-work)


## Prepare the Test Environment 

You can clone and navigate the corresponding directory by running:
```
git clone ssh://git@github.com/MetamorphicSecurityTesting/AIM/.git

```

First, you can set up and activate a virtual environment in your working directory with, for Mac/Linux:
```
python3 -m venv venv
source venv/bin/activate
```

Alternatively, for Windows:
```
python -m venv venv
venv\Scripts\activate
```

The following assumes Mac/Linux.
For Windows users, please use `python` instead of `python3`.
Please note that you need Python 3.11 or before. 
 
Please unzip the following files PreProcessing, OutputClustering, ActionClustering, IMPRO, MOCCO, PostProcessing, and AimOrchestration. 
In any case, to install the packages we use `pip`.
You can update the installer to the latest version, then install AIM and its evaluation framework using:
```
pip install --upgrade pip setuptools 
pip install ./PreProcessing 
pip install ./OutputClustering 
pip install ./ActionClustering 
pip install ./IMPRO 
pip install ./MOCCO 
pip install ./PostProcessing 
pip install ./AimOrchestration 
```

Using dependencies, this will install the AIM
[PreProcessing](https://github.com/MetamorphicSecurityTesting/AIM/tree/main/PreProcessing),
[OutputClustering](https://github.com/MetamorphicSecurityTesting/AIM/tree/main/ActionClustering),
[ActionClustering](https://github.com/MetamorphicSecurityTesting/AIM/tree/main/OutputClustering),
[IMPRO](https://github.com/MetamorphicSecurityTesting/IMPRO),
[MOCCO](https://github.com/MetamorphicSecurityTesting/GeneticAlgorithm),
[PostProcessing](https://github.com/MetamorphicSecurityTesting/PostProcessor), and
[AimInputSetMinimizer](https://github.com/MetamorphicSecurityTesting/AIM/tree/main/AimOrchestration)
packages.

This will also install other packages that are imported by the AIM tool.
One of them, the `nltk` package, also requires the following instructions to work properly:
```
python3
import nltk
nltk.download('all')
exit()
```

Once everything is set up, you can begin using the AIM pipeline.


## Perform Input set minimization

We have provided the required inputs to replicate the results for Jenkins and Joomla in `AimDatabase/Data/Jenkins` and `AimDatabase/Data/Joomla` directories, which contain the following files: 

- `inputset.json` is the input set to be minimized 
- `costs.csv` contains cost information  
- `outputs.zip` contains output information and it requires to be unzipped 
- `Duplicate` folder contains the expected results of input set minimization and all generated intermediate files 

Then, you can run the AIM pipeline as a whole, using the following command for Jenkins:
```
minimize-inputs inputset.json outputs.txt costs.csv -d Levenshtein -o Kmeans -a Kmeans -s jenkins -v 
```

The `-d` (output distance) argument is optional. The supported distances are Levenshtein and bag distances. By default, all the options are executed. 
The `-o` (output clustering algorithm) argument is optional. The supported algorithms are Kmeans, DBSCAN, and HDBSCAN. By default, all the options are executed. 
The `-a` (action clustering algorithm) argument is optional. The supported algorithms are Kmeans, DBSCAN, and HDBSCAN. By default, all the options are executed. 
The `-s` (system under test) argument is mandatory. The supported system under tests are Jenkins and Joomla. 

Note that, for each combination of distance, output clustering algorithm, and action clustering algorithm, results would be produced in a Dist_Out/Act directory, where Dist is the corresponding distance, Out is the corresponding output clustering algorithm, and Act is the corresponding action clustering algorithm. 

Finally, the `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

At the end of the execution, you should obtain in the console an output like: 

```
(...)
42 inputs selected: 2, 3, 7, 9, 10, 33, 34, 37, 38, 51, 53, 54, 61, 64, 75, 76, 79, 87, 88, 93, 96, 99, 104, 108, 114, 120, 121, 122, 123, 125, 129, 132, 134, 135, 139, 141, 147, 151, 154, 156, 157, 159
73.75 % of the initial input set was removed
minimized input set written in Lev_Kmeans/Kmeans/inputset_minimized.json
```

This will take approximately half an hour, on a desktop PCs (Dell G7 7500, RAM 16 Gb, Intel(R) Core(TM) i9-10885H CPU @ 2.40 GHz) machine, to generate the minimized input set file `inputset_minimized.json` in the `Lev_Kmeans/Kmeans` directory.
It contains the selected inputs and it can be used to execute metamorphic relations.

Finally, you can close your virtual environment.
```
deactivate
```


## Perform input set minimization (step-by-step)

Alternatively, instead of using the `minimize-inputs` command line, you can execute several commands to observe the different steps of the execution, or in case you already have intermediate files (like the ones in the Duplicate directory) and thus you do not need to generate them again. 
 
 
## Preprocessing 
As before, first navigate to the `AimDatabase/Data/Jenkins` or `AimDatabase/Data/Joomla` directory, containing the `inputset.json`, `costs.csv`, and `outputs.zip` files, then unzip the output data. 
 
Then, you can extract the relevant input and output information required for the following steps by running: 
```
preprocess-data inputset.json outputs.txt costs.csv -s jenkins –v 
```
The `-s` (system under test) argument is mandatory. The supported system under tests are Jenkins and Joomla. 
The `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

Executing the `preprocess-data` command would generate the following files: 
- `inputset_preprocessed.csv`, containing input information for the inputs, and 
- `outputs_preprocessed.csv`, containing the relevant output information. 

In case you do not want to execute this step, you may use instead in the following steps the `inputset_preprocessed.csv` and `outputs_preprocessed.csv` files from the Duplicate directory. 

## Output Clustering 

You can cluster the pre-processed outputs by running: 
```
cluster-outputs outputs_preprocessed.csv -d Levenshtein -o Kmeans -v 
```

The `-d` (output distance) argument is optional. The supported distances are Levenshtein and bag distances. By default, all the options are executed. 
The `-o` (output clustering algorithm) argument is optional. The supported algorithms are Kmeans, DBSCAN, and HDBSCAN. By default, all the options are executed. 
The `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

Executing the `cluster-outputs` command would generate the `outputs_classes.csv` file in the Lev_Kmeans directory. In case you do not want to execute this step, you may use instead in the following steps the `inputset_classes.csv` file from the Duplicate/Lev_Kmeans directory. 
 
## Action Clustering 
You can cluster the initial inputs by running the following command: 

```
cluster-actions inputset_preprocessed.csv Lev_Kmeans/inputset_classes.csv -a Kmeans -v 
```

The `-a` (action clustering algorithm) argument is optional. The supported algorithms are Kmeans, DBSCAN, and HDBSCAN. By default, all the options are executed. 
The `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

Executing the `cluster-actions` command would generate the `inputset_action_subclasses.csv` file in the Lev_Kmeans/Kmeans directory. In case you do not want to execute this step, you may use instead in the following steps the `inputset_action_subclasses.csv` file from the Duplicate/Lev_Kmeans/Kmeans directory. 

##  Problem reduction (IMPRO)  
You can reduce the problem of minimizing the cost of the input set while covering all action subclasses, by running: 

```
reduce-problem Lev_Kmeans/Kmeans/inputset_action_subclasses.csv costs.csv -v 
```

The `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

Executing the reduce-problem command would generate in the Lev_Kmeans/Kmeans directory the following files: 
- `inputset_necessary.csv`, containing information on the inputs that have to be present in the final solution, and 
- `inputset_components.csv`, containing information on the inputs which belongs to the input set components. 

In case you do not want to execute this step, you may use instead in the following steps the `inputset_necessary.csv` and `inputset_components.csv` files from the Duplicate/Lev_Kmeans/Kmeans directory. 

## A novel genetic search (MOCCO) 

Then, you can run the genetic search on each input set component, by running: 

```
minimize-components Lev_Kmeans/Kmeans/inputset_components.csv -v 
```
The `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

Executing the `minimize-components` command would generate the `inputset_components_minimized.csv` file in the Lev_Kmeans/Kmeans directory. In case you do not want to execute this step, you may use instead in the last step the `inputset_components_minimized.csv` file from the Duplicate/Lev_Kmeans/Kmeans directory. 


## Postprocessing 

Finally, you can gather necessary inputs with inputs from the minimized components, and use the original JSON file to construct the final solution: 
```
postprocess-data inputset.json Lev_Kmeans/Kmeans/inputset_necessary.csv Lev_Kmeans/Kmeans/inputset_components_minimized.csv -v 
```

The `-v` (verbose) argument is optional. It commands the tool to display information in the console during execution. 

Executing the `postprocess-data` command would generate the `inputset_minimized.json` file in the Lev_Kmeans/Kmeans directory. It contains the selected inputs and it can be used to execute metamorphic relations. In case you want to directly execute metamorphic relations, you may use instead the `inputset_minimized.json` file from the Duplicate/Lev_Kmeans/Kmeans directory. 

Finally, you can close your virtual environment.
```
deactivate
```

## Evaluating the Tool: Key Metrics and Techniques

We consider two systems under test: Jenkins and Joomla.

### Jenkins

Again, you can navigate in the `AimDatabase` directory and you can generate the Random Testing baseline results and gather the Adaptive Random Testing baseline results using:
```
gatherBaselines Results/Jenkins/jenkins_results.json Results/Jenkins/jenkins_baseline_art.json -o Results/Jenkins/jenkins_baselines.json -v
```
For each run, the maximum number of inputs in all the minimized input sets is determined, then used to randomly select that many inputs from the initial input set.

You can analyze AIM results and compare them with baselines using:
```
evalAim Results/Jenkins/jenkins_results.json -b Results/Jenkins/jenkins_baselines.json -a Results/Jenkins/jenkins_analysis.json -d Results/Jenkins/jenkins_duels.json -v
```
obtaining the `Results/Jenkins/jenkins_analysis.json` and `Results/Jenkins/jenkins_duels.json` files.
The former contains analysis results for each configuration.
The latter contains results for the statistical metrics for duels between configurations with full vulnerability coverage.


### Joomla

For Joomla, the procedure is the same as for Jenkins:
```
gatherBaselines Results/Joomla/joomla_results.json Results/Joomla/joomla_baseline_art.json -o Results/Joomla/joomla_baselines.json -v
evalAim Results/Joomla/joomla_results.json -b Results/Joomla/joomla_baselines.json -a Results/Joomla/joomla_analysis.json -d Results/Joomla/joomla_duels.json -v
```


### Generating Tables

Finally, you can generate LaTeX tables representing the analysis results.
First, for the vulnerability coverage, with results from both Jenkins and Joomla:
```
genVulnTable Results/Jenkins/jenkins_analysis.json jenkins Results/Joomla/joomla_analysis.json joomla -o Results/Both/vulnerability_coverage.tex -c Results/Both/colors.json -v
```

This will also generate a `colors.json` file, which is used to generate the duel tables separately for Jenkins and Joomla:
```
genDuelTables Results/Jenkins/jenkins_duels.json -s jenkins -c Results/Both/colors.json -d Results/Jenkins/Tables -v
genDuelTables Results/Joomla/joomla_duels.json -s joomla -c Results/Both/colors.json -d Results/Joomla/Tables -v
```


## How to Cite This Work

N. Bayati Chaleshtari, Y. Marquer, F. Pastore, and L. Briand, "AIM: Automated Input Set Minimization for Metamorphic Security Testing," IEEE Transactions on Software Engineering, 2024, doi: 10.1109/TSE.2024.3488525.
