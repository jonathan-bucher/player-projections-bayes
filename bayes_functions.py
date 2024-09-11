import numpy as np
import pandas as pd

def probability(df, col: str, operator: str, value: str) -> float:
    # calculates the probability of a specific event
    # later, input feedback for improper parameters
    # how to handle null values?
    # greater than or equal to values

    total_count = df[col].count()
    if operator == 'geq':
        cond_count = len(df.loc[df[str(col)] >= value])
    elif operator == 'g':
        cond_count = len(df.loc[df[col] > value])
    elif operator == 'eq':
        cond_count = len(df.loc[df[col] == value])
    elif operator == 'l':
        cond_count = len(df.loc[df[col] < value])
    elif operator == 'leq':
        cond_count = len(df.loc[df[col] <= value])
    else:
        raise ValueError("Invalid operator. Use one of: 'geq', 'g', 'eq', 'l'.")
    return cond_count / total_count


def condition_indices(df, col, operator, value) -> set:
    # Store the condition result based on the operator
    # in_range operator, with value (lower bound, upper bound)
    # want condition indices to be able to handle an arbitrary number of events
    if operator == 'geq':
        condition_occurs = df.index[df[col] >= value]
    elif operator == 'g':
        condition_occurs = df.index[df[col] > value]
    elif operator == 'eq':
        condition_occurs = df.index[df[col] == value]
    elif operator == 'l':
        condition_occurs = df.index[df[col] < value]
    elif operator == 'leq':
        condition_occurs = df.index[df[col] <= value]
    elif operator == 'in_range':
        condition_occurs = df.index[
            (df[col] >= value[0]) & (df[col] <= value[1])
            ]
    else:
        raise ValueError("Invalid operator. Use one of: 'geq', 'g', 'eq', 'l', 'leq', 'in_range'.")
    
    return set(condition_occurs)


def joint_probability(df, col_1, operator_1, value_1, col_2, operator_2, value_2) -> float:
    # Calculates the probability of two events occurring together
    # Get the total number of rows
    total_count = len(df)
    
    # Find the indices where both conditions hold
    condition_1_indices = condition_indices(df, col_1, operator_1, value_1)
    condition_2_indices = condition_indices(df, col_2, operator_2, value_2)
    
    # Find the intersection of both conditions
    joint_indices = condition_1_indices & condition_2_indices
    
    # Calculate joint probability
    joint_prob = len(joint_indices) / total_count if total_count > 0 else 0
    
    return joint_prob

    
def conditional_probability(df, col_1, operator_1, value_1, col_2, operator_2, value_2) -> float:
    # Calculates the probability of an event occuring given that another event has occured
    # the event is listed first, the condition second

    # Find the indices where both conditions hold
    event = condition_indices(df, col_1, operator_1, value_1)
    condition = condition_indices(df, col_2, operator_2, value_2)

    # find the number of rows that meet the condition
    event_space = len(condition)
    
    # Find the intersection of both conditions
    joint_indices = condition & event
    
    # Calculate conditional probability
    cond_prob = len(joint_indices) / event_space if event_space > 0 else 0
    
    return cond_prob

def bayes(df, col_1, operator_1, value_1, col_2, operator_2, value_2) -> float:
    # baye's theorem
    # P(1|2) = P(2|1) * P(1) / P(2)
    num = conditional_probability(df, col_2, operator_2, value_2, col_1, operator_1, value_1) * probability(df, col_1, operator_1, value_1)
    # denominator is the overall chance of rain
    denom = probability(df, col_2, operator_2, value_2)

    return (num / denom)
