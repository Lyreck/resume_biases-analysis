import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_and_process_data_files(database_path = "data/database_all_cv_combinations_with_keys.csv", experiment_path = "data/name/Nurse_Freelance_Jehovah_switnesses.csv"):

    resume_database = pd.read_csv(database_path)
    resume_database.dropna(subset=['key'], inplace=True)
    resume_database.drop_duplicates(subset=['key'], inplace=True)
    resume_database['key'] = resume_database['key'].apply(lambda x: x.replace(" ","").lower())

    # Load the experiment where we modify names, and have a job experience that is not adapted to the job offer.
    name_experiment_nurse_not_adapted = pd.read_csv(experiment_path)
    name_experiment_nurse_not_adapted['Resume'] = name_experiment_nurse_not_adapted['Resume'].apply(lambda x:  x.replace(" ","").lower())

    df = pd.merge(name_experiment_nurse_not_adapted, resume_database, how='inner', left_on='Resume', right_on='key')
    # print(df[['gender', 'british', 'field_of_study', 'Score']]) #data for analysis

    return df

if __name__ == "__main__":
    ## Example code for data analysis for the website. ------
    
    df = load_and_process_data_files()

    print(df[['gender', 'british', 'field_of_study', 'Score']]) #data for analysis


    ## You can put descriptive statistics / exploratory data analysis here

    # Mean score by gender (0 = male, 1 = female)
    print(df.groupby('gender', as_index = False).agg(mean_score = ("Score", 'mean')).sort_values(by = "mean_score", ascending = False))
    # women have better score than men by approx. 2 points on this example.

    # between ethnicities
    print(df.groupby('british', as_index = False).agg(mean_score = ("Score", 'mean')).sort_values(by = "mean_score", ascending = False))

    # compare british and non-british
    print(f'british mean: {df[df["british"] == 1][["Score"]].mean()}')
    print(f'non-british mean: {df[df["british"] != 1][["Score"]].mean()}')

    ## You can put nice graphs here


    ## You can do fancy kmeans clustering and visualization here