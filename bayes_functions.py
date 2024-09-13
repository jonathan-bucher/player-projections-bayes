import numpy as np
import pandas as pd

import logging

# Configure logging to show messages of DEBUG level or higher
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def probability(df, col: str, operator: str, value: str) -> float:
    # calculates the probability of a specific event
    # later, input feedback for improper parameters
    # how to handle null values?

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
    # handle null values

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

    
def conditional_probability(df, conditions: list[tuple]) -> float:
    """
    Calculates the probability of an event occurring given that conditions have been met.
    
    Args:
        df (pd.DataFrame): The dataframe containing the data.
        conditions (list[tuple]): A list of three-tuples where:
            - The first element is the column name (str).
            - The second element is the operator (e.g., 'geq', 'eq', 'leq', etc.).
            - The third element is the value for the condition.
            The event is the first tuple, and the conditions are the subsequent tuples.
            
    Returns:
        float: The conditional probability.
    """

    # put in an option to print the number of rows that met the condition
    
    # Step 1: Get the indices where the event occurs (first condition in the list)
    event_indices = condition_indices(df, conditions[0][0], conditions[0][1], conditions[0][2])

    # Step 2: Create a set for condition indices based on the first condition after the event
    condition_indices_set = condition_indices(df, conditions[1][0], conditions[1][1], conditions[1][2])
    logging.debug(f"Initial Condition: {condition_indices_set}")

    # Step 3: Check for additional conditions and find intersection of indices
    for i in range(2, len(conditions)):
        condition_indices_set &= condition_indices(df, conditions[i][0], conditions[i][1], conditions[i][2])
        logging.debug(f"Condition {i}: {condition_indices_set}")

    # Step 4: Calculate the number of rows where the condition occurs (event space)
    event_space_size = len(condition_indices_set)

    # Step 5: Find the rows where both the event and conditions occur
    joint_indices = condition_indices_set & event_indices
    logging.debug(f"Condition and Event: {joint_indices}")

    # Step 6: Calculate the conditional probability
    conditional_prob = len(joint_indices) / event_space_size if event_space_size > 0 else 0

    return conditional_prob


def bayes(df, col_1, operator_1, value_1, col_2, operator_2, value_2) -> float:
    # baye's theorem
    # P(1|2) = P(2|1) * P(1) / P(2)
    num = conditional_probability(df, [(col_2, operator_2, value_2), (col_1, operator_1, value_1)]) * probability(df, col_1, operator_1, value_1)
    # denominator is the overall chance of rain
    denom = probability(df, col_2, operator_2, value_2)

    return (num / denom)
