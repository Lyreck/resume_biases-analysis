## main file that takes the generated descriptions and build 
# - the CVs 
# the corresponding databases: 
# 1. CVkey, JobDescKey, Score
# 2. JobDesc Name, .... ??? + key
# 3. CV Name, Education Sector, .... (genre mettre dans la database toutes les infos importantes du CV) + key

## Please download the files data_decoding.csv and data_desc.csv and put them in the data folder.

import pandas as pd
import hashlib
import time as t


from .descriptions_to_pdf import insert_descriptions_to_pdf
from .database_generation import create_resume_database
from .utils.progress_bar import progress
from rich.progress import track

import logging
logger = logging.getLogger(__name__)


def generate_pdfs(data_for_generation, out_directory, verbose=False):
    """_summary_

    Args:
        data_for_generation (_type_): _description_
        out_directory (_type_): _description_
        verbose (bool, optional): Put True if you want the LaTeX rendering logs printed in stdout (in the terminal). Defaults to False.
    """


    n = len(data_for_generation)

    keys=["NaN" for _ in range(n)] #this list will contain the keys (=name) of every resume generated.
    # the objective is to append this as a column to the database of data_for_generation.

    # Iterate through the database and create a resume for each entry
    t0= t.time()
    for index, row in track(data_for_generation.iterrows()):
        # Extract the necessary information from the row
        name = row['name']
        surname = row['surname']
        comp_name = row['comp_name'].capitalize().replace("&", r"and")
        job_desc = row['job_desc']
        association_name = row['association'].capitalize().replace("&", r"and")
        association_desc = row['vol_desc']
        field_of_study = row['field_of_study']

        #data_names['name'] = data_names['name'].str.capitalize()

        
        whole_line = name + surname + comp_name + association_name #these 4 variables uniquely identify the Resume.
        keys[index] = whole_line
        # # convert the unique line to a hash using hashlib sha256
        # hash_object = hashlib.sha256(whole_line.encode())
        # resume_key = str(hash(hash_object.hexdigest())) #has to be a string to be used as a filename.

        insert_descriptions_to_pdf(name+ " " + surname, comp_name, job_desc, association_name, association_desc, field_of_study, out_directory=out_directory, resume_filename=whole_line, verbose=verbose)

        if index == 100:
            logging.info(f"Estimated time to finish generating {n} resumes: {round( ( ((t.time()-t0) / 3600 ) /index)*n,2)} hours")
        # if index > 100 and verbose:
        #     progress(int((index+1)/n*100))


    logging.info(f"Finished creating {n} PDFS in {round( (t.time()-t0) / 3600,2)} hours")
        
    data_for_generation['key'] = keys #add the keys to the database.



if __name__ == "__main__":
    # Load the necessary data to create all the possible resumes based on our companies, names, and associative experiences.
    verbose=True #False if you don't want the progress bar and timing information printed in the terminal.
    data_decoding=pd.read_csv('data/data_decoding.csv')
    data_desc=pd.read_csv('data/data_desc.csv')

    data_for_generation = create_resume_database(data_decoding, data_desc, to_csv=False) #this gives us the database.
    n = len(data_for_generation)

    keys=["NaN" for _ in range(n)] #this list will contain the keys (=name) of every resume generated.
    # the objective is to append this as a column to the database of data_for_generation.

    # Iterate through the database and create a resume for each entry
    t0= t.time()
    for index, row in data_for_generation.iterrows():
        # Extract the necessary information from the row
        name = row['name']
        surname = row['surname']
        comp_name = row['comp_name'].capitalize().replace("&", r"and")
        job_desc = row['job_desc']
        association_name = row['association'].capitalize().replace("&", r"and")
        association_desc = row['vol_desc']
        field_of_study = row['field_of_study']

        #data_names['name'] = data_names['name'].str.capitalize()

        
        whole_line = name + surname + comp_name + association_name #these 4 variables uniquely identify the Resume.
        keys[index] = whole_line
        # # convert the unique line to a hash using hashlib sha256
        # hash_object = hashlib.sha256(whole_line.encode())
        # resume_key = str(hash(hash_object.hexdigest())) #has to be a string to be used as a filename.

        insert_descriptions_to_pdf(name+ " " + surname, comp_name, job_desc, association_name, association_desc, field_of_study, out_directory="data/generated_resumes", resume_filename=whole_line, verbose=verbose)

        if index == 100 and verbose:
            print(f"Estimated time to finish generating {n} resumes: {round( ( ((t.time()-t0) / 3600 ) /index)*n,2)} hours")
        if index > 100 and verbose:
            progress(int((index+1)/n*100))

    if verbose:
        print(f"Finished creating {n} PDFS in {round( (t.time()-t0) / 3600,2)} hours")
        
    data_for_generation['key'] = keys #add the keys to the database.

    # print(data_for_generation.head())

    # Save the database with the keys to a CSV file
    data_for_generation.to_csv('data/database_all_cv_combinations_with_keys.csv', index=False)
