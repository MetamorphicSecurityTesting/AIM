
## Installation

To walk you through using the AIM pipeline, we set up
[this repository](https://github.com/MetamorphicSecurityTesting/AIM/tree/main/AimDatabase) 
with examples.
You can clone and navigate the corresponding directory by running:
```
git clone ssh://git@github.com/MetamorphicSecurityTesting/AIM/tree/main/AimDatabase.git
cd AimDatabase
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

In any case, to install the packages we use `pip`.
You can update the installer to the latest version, then install AIM and its evaluation framework using:
```
pip install --upgrade pip setuptools
pip install .
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


## Usage: Minimize Inputs

In the examples directory, first navigate to the `Example1` directory, which contains the following files:
- `inputset.json` is the input set to be minimized
- `costs.csv` contains cost information obtained from the updated [MST](https://github.com/MetamorphicSecurityTesting/MST) framework
- `outputs.zip` contains output information obtained from the [MST](https://github.com/MetamorphicSecurityTesting/MST) framework, and that requires to be unzipped:
```
cd Example1
tar -xf outputs.zip
```

Then, you can run the AIM pipeline as a whole, using the following command:
```
minimize-inputs inputset.json outputs.txt costs.csv -d Levenshtein -o Kmeans -a Kmeans -v
```

The `-d` (output distance) argument is optional.
The supported distances are Levenshtein and bag distances.
By default, all the options are executed.

The `-o` (output clustering algorithm) argument is optional.
The supported algorithms are Kmeans, DBSCAN, and HDBSCAN.
By default, all the options are executed.

The `-a` (action clustering algorithm) argument is optional.
The supported algorithms are Kmeans, DBSCAN, and HDBSCAN.
By default, all the options are executed.

Note that, for each combination of distance, output clustering algorithm, and action clustering algorithm, results would be produced in a `Dist_Out/Act` directory, where `Dist` is the corresponding distance, `Out` is the corresponding output clustering algorithm, and `Act` is the corresponding action clustering algorithm.

Finally, the `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

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


## Usage: Step by Step

Alternatively, instead of using the `minimize-inputs` command line, you can execute several commands to observe the different steps of the execution, or in case you already have intermediate files (like the ones in the `Duplicate` directory) and thus you do not need to generate them again.

As before, in the examples directory, first navigate to the `RunningExample` directory, containing the `inputset.json`, `costs.csv`, and `outputs.zip` files, then unzip the output data:
```
cd Example1
tar -xf outputs.zip
```

Then, you can extract the relevant input and output information required for the following steps by running:
```
preprocess-data inputset.json outputs.txt costs.csv -v
```

The `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

Executing the `preprocess-data` command would generate the following files:
- `inputset_preprocessed.csv`, containing input information for the inputs with a cost > 0, and
- `outputs_preprocessed.csv`, containing the relevant output information.

In case you do not want to execute this step, you may use instead in the following steps the `inputset_preprocessed.csv` and `outputs_preprocessed.csv` files from the `Duplicate` directory.

Then, you can cluster the pre-processed outputs by running:
```
cluster-outputs outputs_preprocessed.csv -d Levenshtein -o Kmeans -v
```

The `-d` (output distance) argument is optional.
The supported distances are Levenshtein and bag distances.
By default, all the options are executed.

The `-o` (output clustering algorithm) argument is optional.
The supported algorithms are Kmeans, DBSCAN, and HDBSCAN.
By default, all the options are executed.

The `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

Executing the `cluster-outputs` command would generate the `outputs_classes.csv` file in the `Lev_Kmeans` directory.
In case you do not want to execute this step, you may use instead in the following steps the `outputs_classes.csv` file from the `Duplicate/Lev_Kmeans` directory.

Then, you can cluster the initial inputs by running:
```
cluster-actions inputset_preprocessed.csv Lev_Kmeans/outputs_classes.csv -a Kmeans -v
```

The `-a` (action clustering algorithm) argument is optional.
The supported algorithms are Kmeans, DBSCAN, and HDBSCAN.
By default, all the options are executed.

The `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

Executing the `cluster-actions` command would generate the `inputset_action_subclasses.csv` file in the `Lev_Kmeans/Kmeans` directory.
In case you do not want to execute this step, you may use instead in the following steps the `inputset_action_subclasses.csv` file from the `Duplicate/Lev_Kmeans/Kmeans` directory.

Then, you can reduce the problem of minimizing the cost of the input set while covering all action subclasses, by running:
```
reduce-problem Lev_Kmeans/Kmeans/inputset_action_subclasses.csv costs.csv -v
```

The `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

Executing the `reduce-problem` command would generate in the `Lev_Kmeans/Kmeans` directory the following files:
- `inputset_necessary.csv`, containing information on the inputs that have to be present in the final solution, and
- `inputset_components.csv`, containing information on the inputs which belongs to the input set components.

In case you do not want to execute this step, you may use instead in the following steps the `inputset_necessary.csv` and `inputset_components.csv` files from the `Duplicate/Lev_Kmeans/Kmeans` directory.

Then, you can run the genetic search on each inputset component, by running:
```
minimize-components Lev_Kmeans/Kmeans/inputset_components.csv -v
```

The `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

Executing the `minimize-components` command would generate the `inputset_components_minimized.csv` file in the `Lev_Kmeans/Kmeans` directory.
In case you do not want to execute this step, you may use instead in the last step the `inputset_components_minimized.csv` file from the `Duplicate/Lev_Kmeans/Kmeans` directory.

Then, you can gather necessary inputs with inputs from the minimized components, and use the original json file to construct the final solution:
```
postprocess-data inputset.json Lev_Kmeans/Kmeans/inputset_necessary.csv Lev_Kmeans/Kmeans/inputset_components_minimized.csv -v
```

The `-v` (verbose) argument is optional.
It commands the tool to display information in the console during execution.

Executing the `postprocess-data` command would generate the `inputset_minimized.json` file in the `Lev_Kmeans/Kmeans` directory.
It contains the selected inputs and it can be used to execute metamorphic relations.
In case you want to directly execute metamorphic relations, you may use instead the `inputset_minimized.json` file from the `Duplicate/Lev_Kmeans/Kmeans` directory.

Finally, you can close your virtual environment.
```
deactivate
```

## Evaluation

We consider two systems under test: Jenkins and Joomla.

### Jenkins

If necessary, you can extract execution time data from an Excel spreadsheet by first converting it to a CSV file, then converting it into a JSON file.
Here, we use as example a spreadsheet for AIM execution time.
In Excel, save the spreadsheet as CSV, obtaining the `aim_execution_time.csv` file, that you can move in the appropriate directory, for instance `Results/Jenkins/`.
The following step requires separators in that file to be commas.
If this is not the case, then go to `Excel Preferences > Edit > Edit Options` to untick `Use system separators` and replace `Decimal separator` by `.` and `Thousands separator` by `,`.
Then, you can convert it to JSON using:
```
csvToJson Results/Jenkins/aim_execution_time.csv -v
```
obtaining the `Results/Jenkins/aim_execution_time.json` file.

Once you have the `Results/Jenkins/aim_execution_time.json`, `Results/Jenkins/costs.json`, and `Results/Jenkins/vulnerabilities.json` files, as well as a `Runs` directory containing run information from `Run1` to `Run50`, you can gather all the data using:
```
gatherResults Results/Jenkins/vulnerabilities.json Results/Jenkins/costs.json ../../Research/Testing/AIM/Results/Jenkins/Runs Results/Jenkins/aim_execution_time.json -o Results/Jenkins/jenkins_results.json -v
```
obtaining the `Results/Jenkins/jenkins_results.json` output file.

Then, from this file you can generate the Random Testing baseline results and gather the Adaptive Random Testing baseline results using:
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

Finally, you can translate the analysis results into LaTeX tables using:
```
genDuelTables Results/Jenkins/jenkins_duels.json -s jenkins -c Results/Both/colors.json -d Results/Jenkins/Tables -v

```


### Joomla

For Joomla, the procedure is the same as for Jenkins.
It requires the `Results/Joomla/aim_execution_time.json`, `Results/Joomla/costs.json`, and `Results/Joomla/vulnerabilities.json` files, as well as a `Runs` directory containing run information from `Run1` to `Run50`.
Then, you can use the following commands to analyze the result:
```
gatherResults Results/Joomla/vulnerabilities.json Results/Joomla/costs.json ../../Research/Testing/AIM/Results/Joomla/Runs Results/Joomla/aim_execution_time.json -o Results/Joomla/joomla_results.json -v
gatherBaselines Results/Joomla/joomla_results.json Results/Joomla/joomla_baseline_art.json -o Results/Joomla/joomla_baselines.json -v
evalAim Results/Joomla/joomla_results.json -b Results/Joomla/joomla_baselines.json -a Results/Joomla/joomla_analysis.json -d Results/Joomla/joomla_duels.json -v
```


### Tables

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

## How to cite this work

N. Bayati Chaleshtari, Y. Marquer, F. Pastore, and L. Briand, "AIM: Automated Input Set Minimization for Metamorphic Security Testing," IEEE Transactions on Software Engineering, 2024, doi: 10.1109/TSE.2024.3488525.
