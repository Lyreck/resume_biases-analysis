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

 
    # Ensure required columns exist
    #required_columns = ['job_type', 'adapted', 'gender', 'british', 'Score']
    #for col in required_columns:
    #    if col not in df.columns:
    #        raise ValueError(f"Column '{col}' is missing in the DataFrame.")

    # Ensure the output directories exist
    os.makedirs("graphs/name", exist_ok=True)

    # 1. Mean scores for adapted == 1 and adapted == 0 per job type
    adapted_scores = df.groupby(['job_type', 'adapted'])['Score'].mean().unstack()
    adapted_scores.plot(kind='bar', figsize=(10, 6), title="Mean Scores by Adapted Status and Job Type")
    plt.ylabel("Mean Score")
    plt.xlabel("Job Type")
    plt.legend(title="Adapted")
    plt.tight_layout()
    plt.savefig("graphs/name/mean_scores_adapted_vs_not_adapted_per_jobtype.png")
    plt.show()

    # 2. Mean scores for gender == 0 and gender == 1 per job type
    gender_scores = df.groupby(['job_type', 'gender'])['Score'].mean().unstack()
    gender_scores.plot(kind='bar', figsize=(10, 6), title="Mean Scores by Gender and Job Type")
    plt.ylabel("Mean Score")
    plt.xlabel("Job Type")
    plt.legend(title="Gender")
    plt.tight_layout()
    plt.savefig("graphs/name/mean_scores_gender_per_jobtype.png")
    plt.show()

    british_scores = df.groupby(['job_type', 'british'])['Score'].mean().unstack()
    british_scores.plot(kind='bar', figsize=(10, 6), title="Mean Scores by British Status and Job Type")
    plt.ylabel("Mean Score")
    plt.xlabel("Job Type")
    plt.legend(title="British Status")
    plt.tight_layout()
    plt.savefig("graphs/name/mean_scores_british_per_jobtype.png")
    plt.show()

    # 3. Max and min scores per gender
    gender_min_max = df.groupby('gender')['Score'].agg(['min', 'max'])
    gender_min_max.plot(kind='bar', figsize=(8, 5), title="Max and Min Scores by Gender")
    plt.ylabel("Score")
    plt.xlabel("Gender")
    plt.tight_layout()
    plt.savefig("graphs/name/max_min_gender_overall.png")
    plt.show()

    # 4. Max and min scores per british == 0 or == 1
    british_min_max = df.groupby('british')['Score'].agg(['min', 'max'])
    british_min_max.plot(kind='bar', figsize=(8, 5), title="Max and Min Scores by British Status")
    plt.ylabel("Score")
    plt.xlabel("British Status")
    plt.tight_layout()
    plt.savefig("graphs/name/max_min_british_overall.png")
    plt.show()

    # ehnicity difference per jobtype 


    #adapted vs not adapted (jobtype - if adapted exists as column)
    


    # clivant vs non clivant per jobtype 
    # 
    # 
    # clivant vs non clivant - jobtype and gender   

folder_path = "data/scores_experiments/name/"
df = concatenate_dataframes_with_jobtype(folder_path)
generate_graphs(df)