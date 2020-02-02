"""Main module."""
from typing import List

import pandas as pd
from scipy.stats import fisher_exact, chi2_contingency


def test_hypothesis(data: pd.DataFrame, expression_1: str, expression_2: str,
                    threshold: float = 0.05):
    """
    Perform an hypothesis test of independence between expression_1 and
    expression_2. The expression can be column names, in that case each
    category of the column is considered, or boolean tests.

    Depending on the frequencies a fisher test or a chi square test will
    be performed.

    Args:
        data (pd.DataFrame): The data frame containing the data under 
        study

        expression_1 (str): A column name or a boolean test

        expression_2 (str): A column name or a boolean test

        threshold (float): p-value threshold under which the test is 
        considered significant
    
    Returns:
        Dict: Containing the p-value, the contengency table, the test 
        used and if the result is significant

    Examples:
        >>> medstat.test_hypothesis(data, 'sex', 'age < 30')
        {'contingency_table': 
            age < 30  False  True  All
            sex                       
            Female       26    22   48
            Male         24     8   32
            All          50    30   80,
         'test': 'Fisher',
         'p-value': 0.06541995357625573,
         'significant': False}

    """
    result = {}
    contengency_table = __make_contingency_table(data,
                                                 expression_1,
                                                 expression_2)
    result['contengency_table'] = contengency_table

    value_table = contengency_table.iloc[:-1, :-1].values
    min_freq = value_table.min()
    if min_freq >= 10:
        result['test'] = "Chi-squared"
        _, result['p-value'], _, _ = chi2_contingency(value_table)
    else:
        result['test'] = "Fisher"
        try:
            c, result['p-value'] = fisher_exact(value_table)
        except ValueError as e:
            result["error"] = f"Fisher test cannot be used: {e}"
            return result

    result['significant'] = False
    if result['p-value'] < threshold:
        result['significant'] = True

    return result


def analyse_dataset(data: pd.DataFrame, hypothesis: List[tuple],
                    threshold:float = 0.05, file=None):
    """
    Provide a data set and a list of couple of factor for which you want
    to check the independence and it will perform the appropriate test 
    for each hypothesis. The results will also be printed on the screen
    and can be saved to a file.
 
    Args:
        data: The data set.

        hypothesis: List of 2-tuples containing the factor to tests

        threshold (optional): p-value threshold under which the test
        result is considered significant

        file (optional): A file where to write a report of the results
    
    Returns:
        List: A list of dictionnary containing for each test the result, the 
        contingency table etc (see test_hypothesis output)

    Examples:
        >>> medstat.analyse_dataset(data,[('sex', 'age < 30'),
                                          ('sex', 'test_a')],
                                    file='report.txt')
        [{'contengency_table':
            age < 30  False  True  All
            sex                       
            Female       21    18   39
            Male         29    12   41
            All          50    30   80,
            'test': 'Chi-squared',
            'p-value': 0.18407215636751517,
            'significant': False},
            {'contengency_table': 
            test_a  negative  positive  All
            sex                            
            Female        25        14   39
            Male          25        16   41
            All           50        30   80,
            'test': 'Chi-squared',
            'p-value': 0.9539453144224308,
            'significant': False}]

    """
    results = []
    reports = []
    for i, hypo in enumerate(hypothesis):
        result = test_hypothesis(data, *hypo, threshold)
        report = __make_result_report(result, i)
        print(report)
        results.append(result)
        reports.append(report)
    
    if file is not None:
        with open(file, "w") as f:
            for report in reports:
                f.write(report)

    return results


def __make_result_report(result, i):
    exp_1 = result['contengency_table'].index.name
    exp_2 = result['contengency_table'].columns.name
    report = "-" * 20 + f" Test {i + 1} " + "-" * 20 + "\n"
    report += f"Test independence between {exp_1} and {exp_2}. \n"
    report += f"Use {result['test']} test.\n"
    report += f"Result is {(not result['significant']) * 'not '}significant.\n"
    report += f"p-value: {result['p-value']}\n"
    report += f"Contingency table: \n {result['contengency_table']} \n \n"
    return report



def __make_contingency_table(data, expression_1, expression_2):
    """Prepare the contingency table"""
    factors = []

    for expression in [expression_1, expression_2]:
        if expression in data.columns.values:
            factor =  data[expression].astype('category')
        else:
            factor = data.eval(expression)
            factor =  pd.Categorical(factor, categories=[False, True])            

        factors.append(factor)

    contengency_table = pd.crosstab(factors[0],
                                    factors[1],
                                   dropna=False,
                                   margins=True)
    contengency_table.index.name = expression_1
    contengency_table.columns.name = expression_2
    return contengency_table
