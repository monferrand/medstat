"""Main module."""
import pandas as pd
from scipy.stats import fisher_exact, chi2_contingency


def check(data: pd.DataFrame, expression_1: str, expression_2: str,
          threshold: float=0.05):
    """
    Perform an hypothesis test of independence between expression_1 and 
    expression_2. The expression can be column names, in that case each 
    category of the column is considered, or boolean tests.

    Depending on the frequencies a fisher test or a chi square test will be 
    performed.

    Args:
        data (pd.DataFrame): The data frame containing the data under study
        expression_1 (str): A column name or a boolean test
        expression_2 (str): A column name or a boolean test
        threshold (float): Threshold under which the test is considered 
                           significant
    
    Returns:
        Dict: Containing the p-value, the contengency table, the test used 
              And if the result is significant
    """
    result = {}
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

    result['is-significant'] = False
    if result['p-value'] < threshold:
        result['is-significant'] = True

    return result
