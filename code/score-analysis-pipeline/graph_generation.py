# Imports 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns 
import os
from scipy.stats import ttest_ind
from example_data_analysis import load_and_process_data_files 
from scipy.stats import f_oneway


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

#folder_path = "data/scores_experiments/name/"
#df = concatenate_dataframes_with_jobtype(folder_path)
#print(df.columns) 
def generate_graphs(name = True, job = True, volunteering = True):
    # graph generation (gender bias and score difference per jobtype)

 
    # Ensure required columns exist
    #required_columns = ['job_type', 'adapted', 'gender', 'british', 'Score']
    #for col in required_columns:
    #    if col not in df.columns:
    #        raise ValueError(f"Column '{col}' is missing in the DataFrame.")

    # Ensure the output directories exist
    os.makedirs("graphs/name", exist_ok=True)
    os.makedirs("graphs/job", exist_ok=True)
    os.makedirs("graphs/volunteering", exist_ok=True)
    

    green_color = "#78a97f"
    orange_color = "#e28460"
    custom_colors = [green_color, orange_color]

    color1 =  "#15616D"
    color2 = "#E08530"
    color3 = '#DE6137'
    color4 = "#3A6C90"

    gender_colors = [color1, color2]
    adapt_colors = [color3, color4]
    if name: 
        folder_path_name = "data/scores_experiments/name/"
        df = concatenate_dataframes_with_jobtype(folder_path_name)
        df['gender'] = df['gender'].replace({0: 'M', 1: 'F'})


        # 1. Mean scores for adapted == 1 and adapted == 0 per job type
        adapted_scores = df.groupby(['job_type', 'adapted'])['Score'].mean().unstack()
        adapted_scores.plot(kind='bar', figsize=(10, 6),color = adapt_colors, title="Mean Scores by Adapted Status and Job Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Job Type")
        plt.title("Mean compatibility scores by adapted resume status and job type")
        plt.tight_layout()
        plt.savefig("graphs/name/mean_scores_adapted_vs_not_adapted_per_jobtype.png")
        plt.show()

        # 2. Mean scores for gender == 0 and gender == 1 per job type
        gender_scores = df.groupby(['job_type', 'gender'])['Score'].mean().unstack()
        gender_scores.plot(kind='bar', figsize=(10, 6),color = gender_colors, title="Mean Scores by Gender and Job Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Job Type")
        plt.title("Mean compatibility scores by gender and job type")
        plt.tight_layout()
        plt.savefig("graphs/name/mean_scores_gender_per_jobtype.png")
        plt.show()

        british_scores = df.groupby(['job_type', 'british'])['Score'].mean().unstack()
        british_scores.plot(kind='bar', figsize=(10, 6), color = custom_colors, title="Mean Scores by British Status and Job Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Job Type")
        plt.title("C⁠ompatibility scores by name origin and job type")
        plt.tight_layout()
        plt.savefig("graphs/name/mean_scores_british_per_jobtype.png")
        plt.show()

        # 3. Max and min scores per gender
        gender_min_max = df.groupby('gender')['Score'].agg(['min', 'max'])
        gender_min_max.plot(kind='bar', figsize=(8, 5),color = gender_colors, title="Max and Min Scores by Gender")
        plt.ylabel("Score")
        plt.xlabel("Gender")
        plt.title('C⁠ompatibility scores by gender')
        plt.tight_layout()
        plt.savefig("graphs/name/max_min_gender_overall.png")
        plt.show()

        gender_mean = df.groupby('gender')['Score'].mean()
        gender_mean.plot(kind='bar', figsize=(8, 5), color = gender_colors, title="Mean Scores by Gender")
        plt.ylabel("Score")
        plt.xlabel("Gender")
        plt.title('Mean c⁠ompatibility scores by gender')
        plt.tight_layout()
        plt.savefig("graphs/name/mean_gender_overall.png")
        plt.show()

        # 4. Max and min scores per british == 0 or == 1
        british_min_max = df.groupby('british')['Score'].agg(['min', 'max'])
        british_min_max.plot(kind='bar', figsize=(8, 5), color = custom_colors,title="Max and Min Scores by British Status")
        plt.ylabel("Score")
        plt.xlabel("British Name")
        plt.title('C⁠ompatibility scores by name origin')
        plt.tight_layout()
        plt.savefig("graphs/name/max_min_british_overall.png")
        plt.show()

        british_mean = df.groupby('british')['Score'].mean()
        british_mean.plot(kind='bar', figsize=(8, 5), color = custom_colors,title="Mean Scores by British status")
        plt.ylabel("Score")
        plt.xlabel("British Name")
        plt.title('Mean c⁠ompatibility scores by name origin')
        plt.tight_layout()
        plt.savefig("graphs/name/mean_british_overall.png")
        plt.show()

    if job:  
        df = concatenate_dataframes_with_jobtype("data/scores_experiments/job/")
       
        clivant_scores = df.groupby(['job_type', 'clivant'])['Score'].mean().unstack()
        clivant_scores.plot(kind='bar', figsize=(10, 6),color = adapt_colors, title="Mean Scores by Adapted Status and Job Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Job Type")
        plt.title("Mean compatibility scores by volunteering type and per job type")
        plt.tight_layout()
        plt.savefig("graphs/job/mean_scores_clivant_vs_not_clivant_per_jobtype.png")
        plt.show()

        
        # Mean scores by comp_type
        comp_type_scores = df.groupby('comp_type')['Score'].mean()
        comp_type_scores.plot(kind='bar', figsize=(10, 6), color=green_color, title="Mean Scores by Company Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Company Type")
        plt.tight_layout()
        plt.savefig("graphs/job/mean_scores_by_comp_type.png")
        plt.show()


         # Mean scores by comp_name
        comp_name_scores = df.groupby('comp_name')['Score'].mean()
        comp_name_scores.plot(kind='bar', figsize=(10, 6), color=orange_color, title="Mean Scores by Company Name")
        plt.ylabel("Mean Score")
        plt.xlabel("Company Name")
        plt.tight_layout()
        plt.savefig("graphs/job/mean_scores_by_comp_name.png")
        plt.show()

        











    if volunteering: 
        df = concatenate_dataframes_with_jobtype("data/scores_experiments/volunteering/")

        #adapted vs not adapted per jobtype
        adapted_scores = df.groupby(['job_type', 'adapted'])['Score'].mean().unstack()
        adapted_scores.plot(kind='bar', figsize=(10, 6),color = adapt_colors, title="Mean Scores by Adapted Status and Job Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Job Type")
        plt.title("Mean compatibility scores by adapted resume status and job type")
        plt.tight_layout()
        plt.savefig("graphs/volunteering/mean_scores_adapted_vs_not_adapted_per_jobtype.png")
        plt.show()

        association_scores = df.groupby('association')['Score'].mean()
        association_scores.plot(kind='bar', figsize=(10, 6), color=green_color, title="Mean Scores by Association")
        plt.ylabel("Mean Score")
        plt.xlabel("Association")
        plt.tight_layout()
        plt.savefig("graphs/volunteering/mean_scores_by_association.png")
        plt.show()

        ideology_scores = df.groupby('ideology')['Score'].mean()
        ideology_scores.plot(kind='bar', figsize=(10, 6), color=[green_color, orange_color, color4], title="Mean Scores by Ideology type (0 = neutral, 1 = political, 2 = religious)")
        plt.ylabel("Mean Score")
        plt.xlabel("Ideology type")
        plt.tight_layout()
        plt.savefig("graphs/volunteering/mean_scores_by_ideology.png")
        plt.show()

        ideology_scores_per_job = df.groupby(['job_type', 'ideology'])['Score'].mean().unstack()
        ideology_scores_per_job.plot(kind='bar', figsize=(10, 6),color = [green_color, orange_color, color4], title="Mean Scores by Ideological affiliation and Job Type")
        plt.ylabel("Mean Score")
        plt.xlabel("Job Type")
        plt.title("Mean compatibility scores by Ideological affiliation and job type")
        plt.tight_layout()
        plt.savefig("graphs/volunteering/mean_scores_ideology_per_jobtype.png")
        plt.show()






         


        
        


        # clivant vs non clivant per jobtype 
        # 
        # 
    # clivant vs non clivant - jobtype and gender   



def top_and_bottom_associations(df):
    """
    Displays the first 5 and last 5 associations in terms of mean scores.

    Args:
        df (pd.DataFrame): The DataFrame containing the data for volunteering.
    """
    mean_scores = df.groupby('association')['Score'].mean().sort_values()
    print("Bottom 5 Associations by Mean Score:")
    print(mean_scores.head(5))
    print("\nTop 5 Associations by Mean Score:")
    print(mean_scores.tail(5))



def generate_desc_stats(name=True, job=True, volunteering=True):
    """
    Generates descriptive statistics and performs t-tests for gender and British status.
    Prints mean scores for various groupings.
    """
    if name:
        print("=== Descriptive Statistics for Name ===")
        folder_path_name = "data/scores_experiments/name/"
        df = concatenate_dataframes_with_jobtype(folder_path_name)
        df['gender'] = df['gender'].replace({0: 'M', 1: 'F'})

        # T-test for gender
        male_scores = df[df['gender'] == 'M']['Score']
        female_scores = df[df['gender'] == 'F']['Score']
        t_stat_gender, p_value_gender = ttest_ind(male_scores, female_scores, nan_policy='omit')
        print(f"T-test for Gender: t-stat={t_stat_gender:.3f}, p-value={p_value_gender:.3f}")

        # T-test for British status
        british_scores = df[df['british'] == 1]['Score']
        non_british_scores = df[df['british'] == 0]['Score']
        t_stat_british, p_value_british = ttest_ind(british_scores, non_british_scores, nan_policy='omit')
        print(f"T-test for British Status: t-stat={t_stat_british:.3f}, p-value={p_value_british:.3f}")

        # Mean scores
        print("Mean Scores by Gender:")
        print(df.groupby('gender')['Score'].mean())
        print("\nMean Scores by British Status:")
        print(df.groupby('british')['Score'].mean())
        print("\nMean Scores Overall:")
        print(df['Score'].mean())
        print("\nMean Scores by Company Name:")
        print(df.groupby('comp_name')['Score'].mean())
        print("\nMean Scores by Company Type:")
        print(df.groupby('comp_type')['Score'].mean())

        for job_type, group in df.groupby('job_type'):
            print(f"\n--- T-tests for job_type: {job_type} ---")

            # T-test for gender
            scores_m = group[group['gender'] == 'M']['Score']
            scores_f = group[group['gender'] == 'F']['Score']
            if len(scores_m) > 1 and len(scores_f) > 1:
                t_stat, p_val = ttest_ind(scores_m, scores_f, nan_policy='omit')
                print(f"Gender t-test: t={t_stat:.3f}, p={p_val:.3f}")
            else:
                print("Not enough data for gender t-test.")

            # T-test for British status
            scores_0 = group[group['british'] == 0]['Score']
            scores_1 = group[group['british'] == 1]['Score']
            if len(scores_0) > 1 and len(scores_1) > 1:
                t_stat, p_val = ttest_ind(scores_0, scores_1, nan_policy='omit')
                print(f"British status t-test: t={t_stat:.3f}, p={p_val:.3f}")
            else:
                print("Not enough data for British status t-test.")

    if job:
        print("\n=== Descriptive Statistics for Job ===")
        df = concatenate_dataframes_with_jobtype("data/scores_experiments/job/")

        # Mean scores by comp_type
        print("Mean Scores by Company Type:")
        print(df.groupby('comp_type')['Score'].mean())

        # Mean scores by comp_name
        print("\nMean Scores by Company Name:")
        print(df.groupby('comp_name')['Score'].mean())


        
        # t-test for clivant
        print("\nT-test for clivant resumes:")
        scores0 = df[df['clivant'] == 0]['Score']
        scores1 = df[df['clivant'] == 1]['Score']
        if len(scores0) > 1 and len(scores1) > 1:
            t_stat, p_val = ttest_ind(scores0, scores1, nan_policy='omit')
            print(f"t={t_stat:.3f}, p={p_val:.3f}")
        else:
            print("Not enough data for t-test on clivant.")

        # ANOVA for comp_type
        print("\nANOVA on comp_type:")
        groups = [g['Score'].values for _, g in df.groupby('comp_type')]
        if all(len(g) > 1 for g in groups):
            f_stat, p_val = f_oneway(*groups)
            print(f"ANOVA F={f_stat:.3f}, p={p_val:.3f}")
        else:
            print("Not enough data for ANOVA on comp_type.")



        

    if volunteering:
        print("\n=== Descriptive Statistics for Volunteering ===")
        df = concatenate_dataframes_with_jobtype("data/scores_experiments/volunteering/")

        top_and_bottom_associations(df)

        # Mean scores by association
        print("Mean Scores by Association:")
        print(df.groupby('association')['Score'].mean())

        print("Mean Scores by Ideology affiliation type:")
        print(df.groupby('ideology')['Score'].mean())

        # Mean scores by comp_name
        print("\nMean Scores by Company Name:")
        print(df.groupby('comp_name')['Score'].mean())

        # Mean scores by comp_type
        print("\nMean Scores by Company Type:")
        print(df.groupby('comp_type')['Score'].mean())


        print("\nANOVA on ideology (overall):")
        groups = [g['Score'].values for _, g in df.groupby('ideology')]
        if all(len(g) > 1 for g in groups):
            f_stat, p_val = f_oneway(*groups)
            print(f"ANOVA F={f_stat:.3f}, p={p_val:.3f}")
        else:
            print("Not enough data for ANOVA on ideology (overall)")


        print("\nT-test for adapted resumes:")
        scores0 = df[df['adapted'] == 0]['Score']
        scores1 = df[df['adapted'] == 1]['Score']
        if len(scores0) > 1 and len(scores1) > 1:
            t_stat, p_val = ttest_ind(scores0, scores1, nan_policy='omit')
            print(f"t={t_stat:.3f}, p={p_val:.3f}")
        else:
            print("Not enough data for t-test on adapted.")


        for adapted_val in [0, 1]:
            print(f"\nANOVA on ideology for adapted == {adapted_val}:")
            sub = df[df['adapted'] == adapted_val]
            groups = [g['Score'].values for _, g in sub.groupby('ideology')]
            if all(len(g) > 1 for g in groups):
                f_stat, p_val = f_oneway(*groups)
                print(f"ANOVA F={f_stat:.3f}, p={p_val:.3f}")
            else:
                print("Not enough data for ANOVA on ideology (adapted == {adapted_val})")

        



if __name__ == "__main__":
    # Example usage
    #generate_graphs(name=False, job=False, volunteering=True)
    #generate_desc_stats(name = False, job = True, volunteering=True)
    df = concatenate_dataframes_with_jobtype("data/scores_experiments/name/")
    
   
   
    #print(df.columns)
