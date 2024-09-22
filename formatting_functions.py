import numpy as np
import pandas as pd
import re

import logging

# Configure logging to show messages of DEBUG level or higher
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# general filtering for a dataframe with quarterback, runningback, or wide receiver data:


def qb_column_transform(df):
    """
    Formats and cleans a pro football reference dataframe with quarterback data

    Args:
        df: a pandas dataframe containing the data

    Returns:
        df: relevant columns of the dataframe, renamed for clarity 
    """

    # keep only relevant columns
    df = df[['Rk', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Unnamed: 7', 'GS',
                                    'Att', 'Yds', 'TD', 
                                    'Rec', 'Yds.2', 'TD.1']].copy()
    
    # rename columns for clarity
    df.rename(columns = {'Yds': 'PassYds'}, inplace = True)
    df.rename(columns = {'TD': 'PassTD'}, inplace = True)
    df.rename(columns = {'Yds.2': 'RushYds'}, inplace = True)
    df.rename(columns = {'TD.1': 'RushTD'}, inplace = True)
    df.rename(columns = {'Unnamed: 7': 'Home'}, inplace = True)
    df.rename(columns = {'Rk': 'Time'}, inplace = True)
    df.rename(columns = {'GS': 'Started'}, inplace = True)

    # convert columns to numeric datatype
    df['PassYds'] = pd.to_numeric(df['PassYds'], errors='coerce')
    df['PassTD'] = pd.to_numeric(df['PassTD'], errors='coerce')
    df['RushYds'] = pd.to_numeric(df['RushYds'], errors='coerce')
    df['RushTD'] = pd.to_numeric(df['RushTD'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    return df


def rb_column_transform(df):
    """
    Formats and cleans a pro football reference dataframe with runningback data

    Args:
        df: a pandas dataframe containing the data

    Returns:
        df: relevant columns of the dataframe, renamed for clarity 
    """

    # keep only relevant columns
    df = df[['Rk', 'Year', 'Date', 'Week', 'Tm', 'Opp', 'Result', 'Unnamed: 7', 'GS',
                                    'Att', 'Yds', 'TD', 
                                    'Rec', 'Yds.1', 'TD.1']].copy()
    
    # rename columns for clarity
    df.rename(columns = {'Yds': 'RushYds'}, inplace = True)
    df.rename(columns = {'TD': 'RushTD'}, inplace = True)
    df.rename(columns = {'Yds.1': 'RecYds'}, inplace = True)
    df.rename(columns = {'TD.1': 'RecTD'}, inplace = True)
    df.rename(columns = {'Unnamed: 7': 'Home'}, inplace = True)
    df.rename(columns = {'Rk': 'Time'}, inplace = True)
    df.rename(columns = {'GS': 'Started'}, inplace = True)

    # convert columns to numeric datatype
    df['RecYds'] = pd.to_numeric(df['RecYds'], errors='coerce')
    df['RecTD'] = pd.to_numeric(df['RecTD'], errors='coerce')
    df['RushYds'] = pd.to_numeric(df['RushYds'], errors='coerce')
    df['RushTD'] = pd.to_numeric(df['RushTD'], errors='coerce')
    df['Year'] = pd.to_numeric(df['Year'], errors='coerce')

    return df


def format(df, position: str):
    """
    Formats and cleans a pro football reference dataframe

    Args:
        df: a pandas dataframe containing the data
        position: a string indicating the position of the player

    Returns:
        df: a formatted and cleaned pandas dataframe 
    """

    # keep only relevant data for each position
    if position == 'RB':
        df = rb_column_transform(df)

    elif position == 'QB':
        df = qb_column_transform(df)

    # Iterating over the DataFrame rows
    for index, row in df.copy().iterrows():

    # create a column of True or False values for Home:
        if row['Home'] == '@':
            df.loc[index, 'Home'] = False
        else:
            df.loc[index, 'Home'] = True

        # enter a boolean value for the 'started' column
        if row['Started'] == '*':
            df.loc[index, 'Started'] = True
        else:
            df.loc[index, 'Started'] = False

        # Split the 'Result' column's value by hyphen and space
        results_list = re.split(r'[- ]', row['Result'])
    
        # Assigning the split values back to the DataFrame
        if len(results_list) == 3:  # Ensure there are 3 parts in the result (e.g., 'W 20-17')
            df.loc[index, 'Outcome'] = results_list[0]  # 'W' or 'L'
            df.loc[index, 'Team Score'] = float(results_list[1])  # '20'
            df.loc[index, 'Opponent Score'] = float(results_list[2])  # '17'
            df.loc[index, 'Point Total'] = float(results_list[1]) + float(results_list[2])    
            df.loc[index, 'Margin'] = float(results_list[1]) - float(results_list[2])

    df.reset_index(inplace = True, drop = True)
        
    return df