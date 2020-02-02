#!/usr/bin/env python

"""Tests for `medstat` package."""
import itertools
import pytest

import pandas as pd

from medstat import medstat


@pytest.fixture
def make_dataset():

    def _make_dataset(nrows):
        g = itertools.cycle('abc')

        return pd.DataFrame({
            'q1': range(nrows),
            'q2': range(nrows),
            'q3': [next(g) for _ in range(nrows)],
        })

    return _make_dataset


@pytest.mark.parametrize("exp_1", ['q1', 'q1 in [1, 3]', 'q2 >= 5'])
@pytest.mark.parametrize("exp_2", ['q2', 'not q1 in [2, 4]'])
def test_index_names(exp_1, exp_2, make_dataset):
    data = make_dataset(3)
    result = medstat.test_hypothesis(data, exp_1, exp_2)
    assert result["contengency_table"].index.name == exp_1
    assert result["contengency_table"].columns.name == exp_2


def test_missing_boolean_category(make_dataset):
    data = make_dataset(5)
    result = medstat.test_hypothesis(data, 'q1', 'q2 > 10')
    assert True in result["contengency_table"].columns.values
    result = medstat.test_hypothesis(data, 'q1', 'q2 < 10')
    assert False in result["contengency_table"].columns.values


def test_contigency_table_values(make_dataset):
    data = make_dataset(300)
    result = medstat.test_hypothesis(data, 'q1 == 200', 'q2 >= 150')
    assert result["contengency_table"].at[True, True] == 1
    assert result["contengency_table"].at[True, False] == 0
    assert result["contengency_table"].at[False, True] == 149
    assert result["contengency_table"].at[False, False] == 150

    data = make_dataset(4)
    result = medstat.test_hypothesis(data, 'q1 == 1', 'q3')
    assert result["contengency_table"].at[True, 'a'] == 0
    assert result["contengency_table"].at[True, 'b'] == 1
    assert result["contengency_table"].at[False, 'c'] == 1


def test_chisquared_above_10(make_dataset):
    data = make_dataset(300)
    result = medstat.test_hypothesis(data, 'q1 > 200', 'q3')
    assert result['test'] == "Chi-squared"


def test_fisher_below_10(make_dataset):
    data = make_dataset(300)
    result = medstat.test_hypothesis(data, 'q1 < 27', "q3 == 'a'")
    assert result['test'] == "Fisher"


def test_significant(make_dataset):
    data = make_dataset(300)
    result = medstat.test_hypothesis(data, 'q1 % 6 == 0', "q3 == 'a'")
    assert result['significant']
    assert pytest.approx(result['p-value'], 0.1) == 0


def test_not_significant(make_dataset):
    data = make_dataset(300)
    result = medstat.test_hypothesis(data, 'q1 < 100', "q3 == 'a'")
    assert not result['significant']
    assert pytest.approx(result['p-value'], 0.1) == 1


def test_analyse_dataset_results(make_dataset):
    data = make_dataset(10)
    hypothesis = [
        ('q1 < 3', 'q2 < 4'),
        ('q1 < 5', "q3 == 'a'")
    ]
    results = medstat.analyse_dataset(data, hypothesis)
    assert results[0]['significant']
    assert not results[1]['significant']
