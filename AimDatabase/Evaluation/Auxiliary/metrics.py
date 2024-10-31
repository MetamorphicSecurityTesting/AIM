from typing import Tuple, List, Dict, Optional, Any
from scipy.stats import mannwhitneyu, wilcoxon

# compute statistical metrics comparing each configuration with each other
def get_duels(analysis: Dict[str, Dict[str, Dict[str, int]]], configurations: List[str], verbose: Optional[bool] = False) -> Dict[str, Dict[str, Dict[str, Dict[str, Any]]]]:
    if verbose:
        print("compute duel metrics")
    if len(configurations) == 0:
        raise ValueError("configurations is empty.")
    alpha = 0.05# significance level
    duels = {}
    for aspect in ['sizes', 'costs', 'times']:
        duels[aspect] = {}
        for i in range(0, len(configurations) - 1):# the last one cannot duel
            config1 = configurations[i]
            sample1 = get_sample(config1, analysis, aspect)
            duels[aspect][config1] = {}
            for j in range(i + 1, len(configurations)):# cannot duel itself
                # compute p-value and Vargha & Delaney's A12 metric for effect size
                config2 = configurations[j]
                sample2 = get_sample(config2, analysis, aspect)
                pValue, vda = get_stats(sample1, sample2)
                duels[aspect][config1][config2] = {
                    'pValue': pValue,
                    'vda': vda
                }
                # compute secondary values useful for representing the data
                if pValue > alpha:
                    color = 'white'
                    duels[aspect][config1][config2]['color'] = color
                else:
                    intensity = round(abs(2*vda - 1), 2)# is abs(delta), where delta is Cliff's metric, rounded
                    if vda > 0.5:# we want size, cost, and execution time to be smaller
                        color = 'red'
                    else:
                        color = 'green'
                    duels[aspect][config1][config2]['color'] = color
                    duels[aspect][config1][config2]['intensity'] = intensity
    return duels

# get sample of values for a given configuration and aspect
def get_sample(config: str, analysis: Dict[str, Dict[str, Dict[str, int]]], aspect: str) -> List[int]:
    record = analysis[config][aspect]
    # convert dictionary to list, without the 'total' key
    sample = [record[run] for run in record if run != 'total']
    return sample

# perform a U test then return the corresponding statistics
def get_stats(sample1: list, sample2: list) -> Tuple[float, float]:
    if len(sample1) == 0:
        raise ValueError("sample1 is empty.")
    if len(sample2) == 0:
        raise ValueError("sample2 is empty.")
    # Mann–Whitney–Wilcoxon U test, with null hypothesis X1 == X2
    uStat, pValue = mannwhitneyu(sample1, sample2, alternative = 'two-sided')
    if not (0 <= pValue and pValue <= 1):
        raise ValueError(f"{pValue = } is out of range.")
    # uStat counts the number of cases when x1 > x2, and 0.5 for each tie
    # so uStat/(len(sample1)*len(sample2)) is Vargha and Delaney's A12 metric,
    # which is an approximate of P(X1 > X2) + 0.5*P(X1 == X2)
    vda = uStat/(len(sample1)*len(sample2))
    if not (0 <= vda and vda <= 1):
        raise ValueError(f"{vda = } is out of range.")
    return pValue, vda

# compute statistical metrics comparing each genetic algorithm with each other
def get_algo_duels(data: Dict[str, Dict[str, Dict[str, int]]], verbose: Optional[bool] = False) -> Dict[str, Dict[str, Dict[str, Any]]]:
    if verbose:
        print("compute paired statistics")
    alpha = 0.05# significance level
    duels = {}
    algos = list(data.keys())
    samples = [[data[algo][run] for run in data[algo]] for algo in algos]
    for i in range(0, len(algos)):
        algo1 = algos[i]
        sample1 = samples[i]
        duels[algo1] = {}
        for j in range(0, len(algos)):
            if i != j:# cannot be compared with itself
                algo2 = algos[j]
                sample2 = samples[j]
                pValue, effectSize = get_paired_stats(sample1, sample2)
                duels[algo1][algo2] = {
                    'pValue': pValue,
                    'effectSize': effectSize
                }
                # compute secondary values useful for representing the data
                if pValue > alpha:
                    color = 'white'
                    duels[algo1][algo2]['color'] = color
                else:
                    intensity = round(abs(2*effectSize - 1), 2)# is abs(difference), where difference is (Tplus - Tminus)/(Tplus + Tminus)
                    if effectSize > 0.5:# we want cost to be smaller
                        color = 'red'
                    elif effectSize < 0.5:
                        color = 'green'
                    else:
                        color = 'white'
                    duels[algo1][algo2]['color'] = color
                    duels[algo1][algo2]['intensity'] = intensity
    return duels

# perform a (paired) Wilcoxon signed-rank test then return the corresponding statistics
def get_paired_stats(sample1: list, sample2: list) -> Tuple[float, float]:
    if len(sample1) == 0:
        raise ValueError("sample1 is empty.")
    if len(sample2) == 0:
        raise ValueError("sample2 is empty.")
    # signed-rank test
    # as opposed to scipy.stats.mannwhitneyu, which always returns the Mann-Whitney U statistic corresponding with sample1,
    # see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.mannwhitneyu.html
    # scipy.stats.wilcoxon returns
    #   - the sum of the ranks of the differences above or below zero, whichever is smaller, if alternative = 'two-sided'
    #   - the sum of the ranks of the differences above zero, otherwise.
    # see https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.wilcoxon.html
    # hence, to determine which one was returned, we compute them using an alternative implementation
    Tplus, Tminus = get_rankSums(sample1, sample2)
    # moreover, we choose to split the zero rank between positive and negative ones (as in https://dl.acm.org/doi/10.5555/1248547.1248548 ), hence zero_method = 'zsplit'
    T, pValue = wilcoxon(sample1, sample2, zero_method = 'zsplit', alternative = 'two-sided')
    if T != min(Tplus, Tminus):
        raise ValueError(f"wilcoxon with alternative = 'two-sided' returns {T = } while it should be equal to the minimum value between {Tplus = } and {Tminus = }.")
    if not (0 <= pValue and pValue <= 1):
        raise ValueError(f"{pValue = } is out of range.")
    # effect size is based on rank sums Tplus and Tminus
    n = len(sample1)
    total = n*(n + 1)/2# = Tplus + Tminus
    effectSize = Tplus/total
    if not (0 <= effectSize and effectSize <= 1):
        raise ValueError(f"{effectSize = } is out of range.")
    return pValue, effectSize

# alternative implementation to compute the rank sums and thus the effect size
def get_rankSums(sample1: List[int], sample2: List[int]) -> Tuple[float, float]:
    if len(sample1) != len(sample2):
        raise ValueError("Samples should have equal length.")
    n = len(sample1)
    # compute then rank the absolute differences
    differences = [(abs(sample1[i] - sample2[i]), i, sign(sample1[i] - sample2[i])) for i in range(n)]
    differences.sort()
    # gather ranks for each difference d
    # the index of the original data i is not necessary after sorting, but useful to track issues in case of bugs
    ranks = {}
    for d, i, s in differences:
        tuple = (d, i, s)
        # compute ranks
        r = differences.index(tuple) + 1
        if d not in ranks:
            ranks[d] = []
        tuple = (r, i, s)
        ranks[d].append(tuple)
    # average ranks for each difference d
    for d in ranks:
        sum_ranks = 0
        for r, i, s in ranks[d]:
            sum_ranks += r
        r_avg = sum_ranks/len(ranks[d])
        list_avg = []
        for r, i, s in ranks[d]:
            tuple = (r_avg, i, s)
            list_avg.append(tuple)
        ranks[d] = list_avg
    # compute rank sums
    posSum = 0.0
    negSum = 0.0
    for d in ranks:
        for r, i, s in ranks[d]:
            if s == 0:
                posSum += r/2.0
                negSum += r/2.0
            elif s == 1:
                posSum += r
            elif s == -1:
                negSum += r
            else:
                raise ValueError(f"Sign {s = } is incorrect.")
    # return positive and negative rank sums
    return posSum, negSum

# auxiliary sign function
def sign(val: int) -> int:
    if val < 0:
        return -1
    elif val > 0:
        return 1
    else:
        return 0
