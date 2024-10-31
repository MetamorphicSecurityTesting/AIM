from typing import Dict, Tuple, Union, Optional, Any

# this procedure gather vulnerability coverage from Jenkins and Joomla to generate the corresponding LaTeX table in a string representation
# the colors of the configurations/baselines are also gathered to be used in duel tables
def get_table_vulns(analysis1: Dict[str, Dict[str, Dict[str, int]]], analysis2: Dict[str, Dict[str, Dict[str, int]]], system1: str, system2: str, verbose: Optional[bool] = False) -> Tuple[str, Dict[str, str]]:
    # check keys are the same
    if set(analysis1.keys()) != set(analysis2.keys()):
        raise ValueError("The configurations/baselines are not the same.")
    # initialize variables
    sut1, label1 = get_sut_label(system1)# label1 is not used
    sut2, label2 = get_sut_label(system2)# label2 is not used
    # table content
    table = r"""\begin{table}[t]
\centering
\footnotesize
\caption{Coverage of the 9""" + sut1 + r""" and the 3""" + sut2 + r""" vulnerabilities after 50 runs for each configuration and baseline.}
\label{tab:vulnsCoverage}
\begin{tabular}{|c|c|c|c|c|}
\hline
    Vulnerability
    & \multicolumn{4}{c|}{System under test}\\
\cline{2-5}
    Coverage
    & \multicolumn{2}{c|}{""" + sut1 + r"""}
    & \multicolumn{2}{c|}{""" + sut2 + r"""}\\
\hline
    Configurations & Number & Percentage & Number & Percentage \\
    or & of covered & of covered & of covered & of covered \\
    baselines & vulnerabilities & vulnerabilities & vulnerabilities & vulnerabilities \\
\hline
"""
    colors = {}
    for config in analysis1:
        configName = getLatexName(config)
        totalCover1 = analysis1[config]['vulns']['total']
        ratioCover1 = analysis1[config]['vulns']['ratio']
        totalCover2 = analysis2[config]['vulns']['total']
        ratioCover2 = analysis2[config]['vulns']['ratio']
        if ratioCover1 == 1.0:
            color1 = "green"
        else:
            color1 = "red"
        if ratioCover2 == 1.0:
            color2 = "green"
        else:
            color2 = "red"
        if color1 == "green" and color2 == "green":
            color3 = "green"
        elif color1 == "red" and color2 == "red":
            color3 = "red"
        else:
            color3 = "yellow"
        table += r"\cellcolor{" + color3 + "!50} " + configName
        table += r" & \cellcolor{" + color1 + "!50} " + str(totalCover1) + r" & \cellcolor{" + color1 + "!50} " + str(round(100*ratioCover1, 1)) + r"\%"
        table += r" & \cellcolor{" + color2 + "!50} " + str(totalCover2) + r" & \cellcolor{" + color2 + "!50} " + str(round(100*ratioCover2, 1)) + r"\%"
        table += r" \\" + "\n"
        colors[config] = color3
    table += r"""\hline
\end{tabular}
\end{table}
"""
    return table, colors

# get_table is a procedure mapping aspect data to a string representing the corresponding LaTeX table
# colors from the vulnerability coverage are used to set in bold configurations with full vulnerability coverage in both systems
def get_table_duels(data: Dict[str, Dict[str, Dict[str, Any]]], aspect: str, system: Optional[str] = "", colors: Optional[Dict[str, str]] = None, verbose: Optional[bool] = False) -> str:
    sut, label = get_sut_label(system)
    # list of configurations with full coverage
    first_config = list(data.keys())[0]
    configurations_names = [first_config] + list(data[first_config].keys())
    configurations_latex = [getLatexName(config) for config in configurations_names]
    # table content
    table = r"""\begin{table}[t]
\centering
\footnotesize
\caption{Comparison of""" + sut + r""" """ + aspect + r""" for configurations with full vulnerability coverage.}
\label{tab:""" + label + r"""duels:""" + aspect + r"""}
\begin{tabular}{cc|"""
    for config in configurations_latex:
        table += r"c|"
    table += r"""}
\hline
\multicolumn{2}{|c|}{""" + aspect + r"""} """
    for i in range(len(configurations_names)):
        configNames = configurations_names[i]
        configLatex = configurations_latex[i]
        if colors[configNames] == "green":
            table += r"& \textbf{" + configLatex + "} "
        else:
            table += r"& " + configLatex + " "
    table += r"\\" + "\n"
    for i in range(len(configurations_names)):
        configNamesRow = configurations_names[i]
        configLatexRow = configurations_latex[i]
        # content for p-value
        if colors[configNamesRow] == "green":
            table += r"""\hline
\multicolumn{1}{|c|}{\multirow{2}{*}{\textbf{""" + configLatexRow + r"""}}} & $\pValue$
"""
        else:
            table += r"""\hline
\multicolumn{1}{|c|}{\multirow{2}{*}{""" + configLatexRow + r"""}} & $\pValue$
"""
        for j in range(len(configurations_names)):
            configNamesCol = configurations_names[j]
            table += "\t & "
            if i < j:# upper right side of the matrix
                duel = data[configNamesRow][configNamesCol]
                pValue = '{:0.1e}'.format(duel['pValue'])# one digit after dot
                color = duel['color']
                if color in ["green", "red"]:
                    intensity = str(int(100*duel['intensity']))
            elif i > j:# lower left side of the matrix
                duel = data[configNamesCol][configNamesRow]
                pValue = '{:0.1e}'.format(duel['pValue'])# one digit after dot
                color = duel['color']
                if color == "green":
                    color = "red"
                    intensity = str(int(100*duel['intensity']))
                elif color == "red":
                    color = "green"
                    intensity = str(int(100*duel['intensity']))
            if i != j:# fill the cell
                if color in ["green", "red"]:
                    table += r"\cellcolor{" + color + "!" + intensity + "}"
                table += r"\num{" + pValue + "}"
            if j == len(configurations_names) - 1:# is the last cell
                table += r"\\" + "\n"
            else:
                table += "\n"
        # content for VDA
        table += r"""\multicolumn{1}{|c|}{} & $\vda$
"""
        for j in range(len(configurations_names)):
            configNamesCol = configurations_names[j]
            table += "\t & "
            if i < j:# upper right side of the matrix
                duel = data[configNamesRow][configNamesCol]
                vda = str(round(duel['vda'], 2))
                color = duel['color']
                if color in ["green", "red"]:
                    intensity = str(int(100*duel['intensity']))
            elif i > j:# lower left side of the matrix
                duel = data[configNamesCol][configNamesRow]
                vda = str(round(1.0 - duel['vda'], 2))
                color = duel['color']
                if color == "green":
                    color = "red"
                    intensity = str(int(100*duel['intensity']))
                elif color == "red":
                    color = "green"
                    intensity = str(int(100*duel['intensity']))
            if i != j:# fill the cell
                if color in ["green", "red"]:
                    table += r"\cellcolor{" + color + "!" + intensity + "}"
                table += vda
            if j == len(configurations_names) - 1:# is the last cell
                table += r"\\" + "\n"
            else:
                table += "\n"
    # end of the table content
    table += r"""\hline
\end{tabular}
\end{table}
"""
    return table

def get_sut_label(system: str) -> Tuple[str, str]:
    # precompute some variables
    if system == "":
        sut = ""
        label = ""
    else:
        sut = " \\" + system
        label = system + ":"
    return sut, label

translation = {
    'Lev': "Lev",
    'Bag': "Bag",
    'Kmeans': "Kmeans",
    'DBSCAN': "Dbscan",
    'HDBSCAN': "Hdbscan",
    'RT': "Rt",
    'ART': "Art"
}

# transform a configuration name into its LaTeX counterpart
def getLatexName(configName: str) -> str:
    latexName = "\\"
    for word in configName.split("_"):
        latexName += translation[word]
    return latexName

def get_table_algos(data: Dict[str, Dict[str, Dict[str, Any]]], timeBudget: Union[int, float], system: Optional[str] = "", verbose: Optional[bool] = False) -> str:
    sut, label = get_sut_label(system)
    LaTex = {
        'MOCCO': "\\geneticAlgo",
        'MOSA': "\\mosa",
        'NSGA-III': "\\nsgaThree",
        'RandomSearch': "\\algoRandom",
        'GreedySearch': "\\algoGreedy"
    }
    first_algo = list(data.keys())[0]
    algos_names = [first_algo] + list(data[first_algo].keys())
    # control the order of the algos in the table
    if set(algos_names) == {'MOCCO', 'MOSA', 'NSGA-III', 'RandomSearch', 'GreedySearch'}:
        algos_names = ['RandomSearch', 'GreedySearch', 'MOCCO', 'MOSA', 'NSGA-III']
    algos_latex = [LaTex[algo] for algo in algos_names]
    # table content
    table = r"""\begin{table}[t]
\centering
\setlength\tabcolsep{3.5pt}
\footnotesize
\caption{Comparison of genetic algorithms for""" + sut + r""" (""" + timeBudget + r""" s).}
\label{tab:""" + label + r"""algos""" + timeBudget + r"""}
\begin{tabular}{cc|"""
    for algo in algos_latex:
        table += r"c|"
    table += r"""}
\hline
\multicolumn{2}{|c|}{costs} """
    for i in range(len(algos_names)):
        algoNames = algos_names[i]
        algoLatex = algos_latex[i]
        table += r"& " + algoLatex + " "
    table += r"\\" + "\n"
    for i in range(len(algos_names)):
        algoNamesRow = algos_names[i]
        algoLatexRow = algos_latex[i]
        # content for p-value
        table += r"""\hline
\multicolumn{1}{|c|}{\multirow{2}{*}{""" + algoLatexRow + r"""}} & $\pValue$
"""
        for j in range(len(algos_names)):
            algoNamesCol = algos_names[j]
            table += "\t & "
            if i != j:# fill the cell
                duel = data[algoNamesRow][algoNamesCol]
                pValue = '{:0.1e}'.format(duel['pValue'])# one digit after dot
                color = duel['color']
                if color in ["green", "red"]:
                    intensity = str(int(100*duel['intensity']))
                if color in ["green", "red"]:
                    table += r"\cellcolor{" + color + "!" + intensity + "}"
                table += r"\num{" + pValue + "}"
            if j == len(algos_names) - 1:# is the last cell
                table += r"\\" + "\n"
            else:
                table += "\n"
        # content for effect size
        table += r"""\multicolumn{1}{|c|}{} & $\effectSize$
"""
        for j in range(len(algos_names)):
            algoNamesCol = algos_names[j]
            table += "\t & "
            if i != j:# fill the cell
                duel = data[algoNamesRow][algoNamesCol]
                effectSize = str(round(duel['effectSize'], 2))
                color = duel['color']
                if color in ["green", "red"]:
                    intensity = str(int(100*duel['intensity']))
                    table += r"\cellcolor{" + color + "!" + intensity + "}"
                table += effectSize
            if j == len(algos_names) - 1:# is the last cell
                table += r"\\"
            table += "\n"
    # end of the table content
    table += r"""\hline
\end{tabular}
\end{table}
"""
    return table


# ---- OUTDATED ----

# this procedure is outdated, it's usage was: table = get_table_vulns_outdated(analysis, system = system, verbose = verbose)
def get_table_vulns_outdated(analysis: Dict[str, Dict[str, Dict[str, int]]], system: Optional[str] = "", verbose: Optional[bool] = False) -> str:
    sut, label = get_sut_label(system)
    # table content
    table = r"""\begin{table}[t]
\centering
\caption{Coverage of""" + sut + r""" vulnerabilities after 50 runs for each configuration. Configurations and baselines that lead to full vulnerability coverage are in green, while the others are in red.}
\label{tab:""" + label + r"""vulnsCoverage}
\begin{tabular}{|c|c|c|}
\hline
\multirow{2}{*}{Configurations}
    & Number of covered & Percentage of covered \\
    & vulnerabilities & vulnerabilities \\
\hline
"""
    for config in analysis:
        configName = getLatexName(config)
        totalCover = analysis[config]['vulns']['total']
        ratioCover = analysis[config]['vulns']['ratio']
        if ratioCover == 1.0:
            color = "green"
        else:
            color = "red"
        table += r"\rowcolor{" + color + "!50} " + configName + " & " + str(totalCover) + " & " + str(round(100*ratioCover, 1)) + r"\% \\" + "\n"
    table += r"""\hline
\end{tabular}
\end{table}
"""
    return table
