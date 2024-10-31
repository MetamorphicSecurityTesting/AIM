from scipy.stats import mannwhitneyu

def main():
    # sample example
    sample1 = [4, 2, 1]
    sample2 = [3, 2, 0]
    # test the Mann–Whitney–Wilcoxon U test
    uStat, pValue = mannwhitneyu(sample1, sample2)
    print(f"(sample1, sample2), no option:\t{uStat = }, {pValue = }")
    uStat, pValue = mannwhitneyu(sample2, sample1)
    print(f"(sample2, sample1), no option:\t{uStat = }, {pValue = }")
    for alternative in ['two-sided', 'less', 'greater']:
        uStat, pValue = mannwhitneyu(sample1, sample2, alternative = alternative)
        print(f"(sample1, sample2), {alternative}:\t{uStat = }, {pValue = }")
        uStat, pValue = mannwhitneyu(sample2, sample1, alternative = alternative)
        print(f"(sample2, sample1), {alternative}:\t{uStat = }, {pValue = }")

# not executed if the module is imported
if __name__ == '__main__':
    main()
