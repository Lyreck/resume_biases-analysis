## In this code, I intend to manage to fetch for specific resumes in the Data/Processed/Resumes folder (and the same with Job Descriptions).
## Ideally, we want this to be efficient, so avoinding to go through the whole directory of Resumes/job desc).


import pandas as pd
import os
import time as t

def add_json_names_to_database(out_name):
    """
    This function reads the JSON files in the Data/Processed/Resumes directory and adds their names to a CSV file.
    The CSV file is saved in the data/dataframes directory.
    """

    # dataframe where we will add the names of json resumes ("the database")
    df = pd.read_csv("data/dataframes/database_all_cv_combinations_with_keys.csv") 

    #list of json filenames in the Data/Processed/Resumes directory
    resume_json_filenames = [f for f in os.listdir(os.path.join("Data", "Processed", "Resumes")) if f.endswith('.json')]
    # It should be in the same order in df and in the list.

    # add the column
    df["json_filename"] = resume_json_filenames 

    df.to_csv(out_name, index=False)




def fetch_resume(resume_name):
    """
    Fetch a specific resume from the Data/Processed/Resumes folder.

    Args:
        resume_name (str): The name of the resume file to fetch. Should be in the format: name + surname + comp_name + association_name

    Returns:
        resume_json (string): The name of the JSON file for the given resume.
    """

    # matching_files = []
    for filename in os.listdir("Data/Processed/Resumes"):
        if filename.endswith('.json'):
            if resume_name in filename:
                return filename
    

if __name__ == "__main__":
    #Example usage:
    dataframe_filepath = "data/dataframes/"
    processed_data_filepath = "Data/Processed/"

    # add_json_names_to_database("database_all_cv_combinations_with_keys_and_json.csv") #difficult because database size changed with pdf then  json generation !!!

    # CV Name at the end of the directory
    t0 = t.time()
    for i in range(1000):
        resume_name = "EmmaFarbenHuman rights watchOxfam"
        fetch_resume(resume_name) # this should return the name of the json file for the given resume.

    elapsed_time = (t.time() - t0) 
    print(f"Time estimation to compute score for 1000: {elapsed_time:.2f} seconds.")


    # CV Name at the beginning of the directory

    # CV Name in the middle of the directory