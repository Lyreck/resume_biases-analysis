# Imports 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import os
from example_data_analysis import load_and_process_data_files 

#take a folder and concaenate all the dataames from one experience and add a column for jobtype ! 
def concatenate_dataframes_with_jobtype(folder_path):
    """
    Concatenates all dataframes in a folder and adds a 'jobtype' column based on the file name.

    Args:
        folder_path (str): Path to the folder containing the CSV files.

    Returns:
        pd.DataFrame: A concatenated dataframe with an additional 'jobtype' column.
    """
    all_dataframes = []

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):  # Ensure it's a CSV file
            # Extract job type from the file name (e.g., "Nurse" from "Nurse_Blabla.csv")
            job_type = file_name.split('_')[0]

            # Load the CSV file into a DataFrame
            file_path = os.path.join(folder_path, file_name)
            df=load_and_process_data_files( "data/database_all_cv_combinations_with_keys.csv", file_path)
            # Add the 'jobtype' column
            df['job_type'] = job_type

            # Append to the list of DataFrames
            all_dataframes.append(df)

    # Concatenate all DataFrames into one
    concatenated_df = pd.concat(all_dataframes, ignore_index=True)

    return concatenated_df


# test for the function 

#folder_path = "data/name/"
#df = concatenate_dataframes_with_jobtype(folder_path)
#print(df.columns) 
def generate_graphs(df):
    # graph generation (gender bias and score difference per jobtype)


    # ehnicity difference per jobtype 


    #adapted vs not adapted (jobtype - if adapted exists as column)
    


    # clivant vs non clivant per jobtype 
    # 
    # 
    # clivant vs non clivant - jobtype and gender   

