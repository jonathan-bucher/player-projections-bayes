import pytest
import pandas as pd
import numpy as np
import bayes_functions as bf


test_data = {
    'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
    'Age': [24, 27, 0, 22, 30]
}

test_df = pd.DataFrame(test_data)

test_data_2 = {
    'City': ['Seattle', 'Las Vegas', 'New York'],
    'Rain': [0.5, 0.1, 0.3]
}

test_df_2 = pd.DataFrame(test_data_2)

# fake runningback stats
test_data_3 = {
    'yards': [100, 180, 75, 200],
    'd_rank': [2, 3, 1, 4],
}

test_df_3 = pd.DataFrame(test_data_3)

def test_probability():
    assert bf.probability(test_df, 'Name', 'eq', 'David') == 0.20
    assert bf.probability(test_df, 'Name', 'eq', 'David') != 0.10
    assert bf.probability(test_df, 'Age', 'geq', 22) == 0.8

test_probability()

def test_condition_indices():
    assert len(bf.condition_indices(test_df, 'Name', 'eq', 'David')) == 1
    assert len(bf.condition_indices(test_df, 'Age', 'geq', 22)) == 4

test_condition_indices()

def test_joint_probability():
    assert bf.joint_probability(test_df, 'Name', 'eq', 'David', 'Age', 'leq', 25) == 0.2
    assert bf.joint_probability(test_df, 'Name', 'eq', 'Bob', 'Age', 'l', 25) == 0

test_joint_probability()

def test_conditional_probability():
    # given that your age is less than or equal to 25, what is the chance your name is David?
    assert bf.conditional_probability(test_df, 'Name', 'eq', 'David', 'Age', 'leq', 25) == (1 / 3)

test_conditional_probability()

def test_bayes():
    # a runningback plays the first game of the season, and rushes for 170 yards
    # what are the odds, based on historical data, that this team is the worst in a four team league
    assert bf.bayes(test_df_3, 'd_rank', 'eq', 4, 'yards', 'geq', 170) == 0.5

test_bayes()

# test independence()
    # want to determine if two events are statistically independent