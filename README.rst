=======
medstat
=======


.. image:: https://img.shields.io/pypi/v/medstat.svg
        :target: https://pypi.python.org/pypi/medstat

.. image:: https://img.shields.io/travis/monferrand/medstat.svg
        :target: https://travis-ci.org/monferrand/medstat

.. image:: https://readthedocs.org/projects/medstat/badge/?version=latest
        :target: https://medstat.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


medstat is a library aiming to make basic hypothesis testing as simple as 
possible. 

Getting started
----------------

This project is available on PyPI you can just:

.. code::

    pip install medstat


Quick Example
----------------

Load your data in a dataframe using for instance `pd.read_csv()` or
`pd.read_excel()`.

.. code:: python

    data = pd.read_csv("my_data.csv")


Test a single hypothesis:

.. code:: python

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


Or test many hypothesis at the same time:

.. code:: python

    result = medstat.analyse_dataset(data,
                                     [('sex', 'age < 30'),
                                      ('sex', 'test_a'),
                                      ('test_a', 'age > 50'),
                                     ])

It prints the output:

.. code::

    -------------------- Test 1 --------------------
    Test independence between sex and age < 30. 
    Use Chi-squared test.
    Result is not significant.
    p-value: 0.18407215636751517
    Contingency table: 
     age < 30  False  True  All
    sex                       
    Female       21    18   39
    Male         29    12   41
    All          50    30   80 
     
    
    -------------------- Test 2 --------------------
    Test independence between sex and test_a. 
    Use Chi-squared test.
    Result is not significant.
    p-value: 0.9539453144224308
    Contingency table: 
     test_a  negative  positive  All
    sex                            
    Female        25        14   39
    Male          25        16   41
    All           50        30   80 
     
    
    -------------------- Test 3 --------------------
    Test independence between test_a and age > 50. 
    Use Fisher test.
    Result is significant.
    p-value: 6.392910983822276e-12
    Contingency table: 
     age > 50  False  True  All
    test_a                    
    negative     46     4   50
    positive      5    25   30
    All          51    29   80 


You can also save it to a text file using the file argument.

.. code::

    result = medstat.analyse_dataset(data,
                                     [('sex', 'age < 30'),
                                      ('sex', 'test_a'),
                                      ('test_a', 'age > 50'),
                                     ],
                                    file='report.txt')


--------------------------------

* Free software: MIT license
* Documentation: https://medstat.readthedocs.io.
