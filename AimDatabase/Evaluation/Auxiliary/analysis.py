from typing import List, Dict, Optional

# count for each configuration and run the total cost of the minimized inputset
def analyze_results(vulnerabilities: Dict[str, List[int]], inputCosts: Dict[str, int], runs: Dict[str, Dict[str, List[int]]], exeTime: Dict[str, Dict[str, int]], totalVulns: int, verbose: Optional[bool] = False) -> Dict[str, Dict[str, Dict[str, int]]]:
    if verbose:
        print("analyze results")
    if totalVulns == 0:
        raise ValueError("The total number of vulnerabilities should not be zero.")
    vulns = get_vulnCoverage(vulnerabilities, runs, totalVulns, verbose = verbose)
    sizes = get_sizes(runs, verbose = verbose)
    costs = get_costs(inputCosts, runs, verbose = verbose)
    times = get_times(exeTime, verbose = verbose)
    analysis = {}
    for config in runs.keys():
        analysis[config] = {
            'vulns': vulns[config],
            'sizes': sizes[config],
            'costs': costs[config],
            'times': times[config]
        }
    if verbose:
        print("configuration\t", "cover", "size", "cost", "time", sep = "\t")
        for config in analysis:
            text = f"{config}"
            # baseline names are shorter than config names
            if config == 'RT':
                text += "\t"
            if config in ['RT', 'ART_Kmeans', 'ART_DBSCAN', 'ART_HDBSCAN']:
                text += "\t"
            text += f"\t{analysis[config]['vulns']['total']}"
            text += f"\t{analysis[config]['sizes']['total']}"
            text += f"\t{analysis[config]['costs']['total']}"
            text += f"\t{analysis[config]['times']['total']}"
            print(text)
    return analysis

# count for each configuration and run the number of covered vulnerabilities
def get_vulnCoverage(vulnerabilities: Dict[str, List[int]], runs: Dict[str, Dict[str, List[int]]], totalVulns: int, verbose: Optional[bool] = False) -> Dict[str, Dict[str, int]]:
    if verbose:
        print("compute inputset vulnerability coverages")
    vulnCoverage = {}
    for config, configRuns in runs.items():
        vulnCoverage[config] = {}
        vulnCoverage[config]['total'] = 0# assume 'total' is not a run ID
        vulnCoverage[config]['ratio'] = 0.0# assume 'ratio' is not a run ID
        for run, inputset in configRuns.items():
            nbCovered = 0
            for vuln, inputs in vulnerabilities.items():
                covered = False
                # check each vulnerable input
                for input in inputs:
                    # usual case, where input is simply an input ID
                    if isinstance(input, int):
                        if input in inputset:
                            covered = True
                    # case where multiple inputs must be present in the input set at the same time
                    elif isinstance(input, list):
                        if len(input) == 0:
                            raise ValueError("Vulnerability input should not be empty")
                        # all inputs in input should be present in inputset
                        covered = True
                        for inp in input:
                            if inp not in inputset:
                                covered = False
                    # this case should not happen
                    else:
                        raise ValueError(f"Vulnerability input has an unexpected type: {input = }, {type(input) = }")
                    # an inputset covers the vulnerability
                    if covered:
                        nbCovered += 1
                        break
            vulnCoverage[config][run] = nbCovered
            vulnCoverage[config]['total'] += nbCovered
        vulnCoverage[config]['ratio'] = vulnCoverage[config]['total']/totalVulns
    return vulnCoverage

# count for each configuration and run the size of the minimized inputset
def get_sizes(runs: Dict[str, Dict[str, List[int]]], verbose: Optional[bool] = False) -> Dict[str, Dict[str, int]]:
    if verbose:
        print("compute inputset sizes")
    sizes = {}
    for config, configRuns in runs.items():
        sizes[config] = {}
        sizes[config]['total'] = 0# assume 'total' is not a run ID
        for run, inputset in configRuns.items():
            size = len(inputset)
            sizes[config][run] = size
            sizes[config]['total'] += size
    return sizes

# count for each configuration and run the total cost of the minimized inputset
def get_costs(inputCosts: Dict[str, int], runs: Dict[str, Dict[str, List[int]]], verbose: Optional[bool] = False) -> Dict[str, Dict[str, int]]:
    if verbose:
        print("compute inputset costs")
    costs = {}
    for config, configRuns in runs.items():
        costs[config] = {}
        costs[config]['total'] = 0# assume 'total' is not a run ID
        for run, inputset in configRuns.items():
            cost = 0
            for input in inputset:
                cost += inputCosts[str(input)]
            costs[config][run] = cost
            costs[config]['total'] += cost
    return costs

def get_times(exeTime: Dict[str, Dict[str, int]], verbose: Optional[bool] = False) -> Dict[str, Dict[str, int]]:
    if verbose:
        print("compute AIM execution times")
    times = {}
    for config, configRuns in exeTime.items():
        times[config] = {}
        times[config]['total'] = 0# assume 'total' is not a run ID
        for run, time in configRuns.items():
            times[config][run] = time
            times[config]['total'] += time
    return times
