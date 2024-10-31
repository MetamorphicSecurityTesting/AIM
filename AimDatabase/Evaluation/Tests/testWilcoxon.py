# usage
# python3 Evaluation/Tests/testWilcoxon.py

from scipy.stats import mannwhitneyu, wilcoxon

def main():
    # sample example
    sample1 = [-1, 0, 3, 1, -2]
    sample2 = [0, 0, 0, 0, 0]
    print(f"{sample1 = }")
    print(f"{sample2 = }")
    # compare mannwhitneyu and wilcoxon
#    uStat, pValue1 = mannwhitneyu(sample1, sample2, alternative = 'two-sided')
#    vda = round(100*uStat/(len(sample1)*len(sample2)), 2)
#    stat, pValue2 = wilcoxon(sample1, sample2, alternative = 'two-sided')
#    print(f"{vda = }%,\t{pValue1 = }")
#    print(f"{stat = },\t{pValue2 = }")
    # wilcoxon with different alternatives
#    stat0, pValue0 = wilcoxon(sample1, sample2, alternative = 'two-sided')
#    stat1, pValue1 = wilcoxon(sample1, sample2, alternative = 'less')
#    stat2, pValue2 = wilcoxon(sample1, sample2, alternative = 'greater')
#    print(f"two-sided:\t{stat0 = },\t{pValue0 = }")
#    print(f"less:\t\t{stat1 = },\t{pValue1 = }")
#    print(f"greater:\t{stat2 = },\t{pValue2 = }")
#    print(f"{stat0 = },\t{min(stat1, stat2) = }")
    # effect size
    n = len(sample1)
    total = n*(n + 1)/2# wilcoxon raises an error if len(sample1) != len(sample2)
    T, pVal = wilcoxon(sample1, sample2, zero_method = 'zsplit', alternative = 'two-sided')
    print(f"{T = }")
#    effectSize = 4.0*Tplus/(n*(n + 1)) - 1.0# = (Tplus - Tminus)/(Tplus + Tminus)
    effectSize = T/total# = Tplus/(Tplus + Tminus)
    print(f"{effectSize = },\t{pVal = }")

# not executed if the module is imported
if __name__ == '__main__':
    main()
