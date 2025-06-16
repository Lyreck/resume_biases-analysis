## Import 
import pandas as pd 
import numpy as np
import re 
import os


def create_resume_database(data_decoding, data_desc, out_filename='database_all_cv_combinations_with_keys', to_csv=False):
    """
    This function creates a database from the given data_decoding and data_desc DataFrames.
    It processes the data to extract relevant information and combines it into a final DataFrame.
    
    Args:
        data_decoding (pd.DataFrame): DataFrame containing CV data Columns should contain: name,surname,british,volunteering,gender,tech_comp,med_comp,educ_comp,field_study
        data_desc (pd.DataFrame): DataFrame containing job descriptions. They are generated using company and association names, using the LLM.
        
    Returns:
        pd.DataFrame: Final combined DataFrame with everything needed for data analysis and resume generation. Columns: name,surname,british,gender,association,vol_desc,comp_type,comp_name,job_desc,field_of_study,key


    """
    #creating database only with job descriptions 
    #separation at line 112 (between companies and associations)
    #data_desc = data_desc[data_desc['description'].str.contains("Job Experience", case=False, na=False)]

    #creating database only with job descriptions and only with volunteering decriptions 
    #separation at line 112 (between companies and associations)


    experience_desc = data_desc[data_desc['description'].str.contains("Job Experience", case=False, na=False)]

    #creating experience database - column from med_comp, tech_comp and educ_comp columns 

    comp_columns = ['tech_comp', 'med_comp', 'educ_comp']

    experience_type = data_decoding.melt(
        id_vars=['name', 'surname'],  # on ne garde que les colonnes à transformer
        value_vars=comp_columns,
        var_name='comp_type',
        value_name='company'
    ).dropna(subset=['company']) 
    #droping unused columns 
    experience_type = experience_type.drop(columns= ['name', 'surname'])
    #deleting all the lines that are empty in the company column
    experience_type.dropna(subset=['company'], inplace=True)

    #deleting all the lines that contain NONE in the company column
    experience_type = experience_type[~experience_type['company'].str.contains("NO PREVIOUS EXPERIENCE", case=False, na=False)]


    #merging experience and experience_desc databases 
    experience = pd.merge( experience_type, experience_desc, left_on='company', right_on= 'comp_name', how='left') #outer?
    experience.drop_duplicates(subset=['nb'], inplace=True) 

    #deleting columns that are not useful anymore and renaming columns for clarity
    # experience = experience.drop(columns = ['nb', 'company', 'ideology']) #### WHY IDEOLOGY NOT FOUND ANYMORE?
    experience = experience.drop(columns = ['nb', 'company'])
    experience = experience.rename(columns={ "description": "job_desc"})

    #creating volunteering database 
    volunteering = data_desc[data_desc['description'].str.contains("volunteering experience", case=False, na=False)]
    volunteering= volunteering.drop(columns = ['nb'])
    #renaming columns for clarity 
    volunteering = volunteering.rename(columns={"comp_name": "association", "description": "vol_desc"})



    #creating names and demographics database  

    data_names = data_decoding[['name', 'surname', 'british','gender']].copy()

    #capitalizing only first letters of names and surnames 
    data_names['name'] = data_names['name'].str.capitalize()
    data_names['surname'] = data_names['surname'].str.capitalize()

    # Change "british" and "gender" to integer
    data_names['british'] = data_names['british'].astype(int)
    data_names['gender'] = data_names['gender'].astype(int)


    #joining final database : names, demographics experience and volunteering : 
    #creating all the possible combinations (there might be a a lot)
    data_name_exp = data_names.merge(volunteering, how = "cross")
    data_for_generation = data_name_exp.merge(experience, how ='cross')

    #adding field of study column, where when it is comp_type = 'educ_comp' we add field of study = 'Liberal Arts', 
    #when it is 'tech_comp' we add field of study = 'Computer Science', and when it is 'med_comp' we add field of study = 'Medicine'
    data_for_generation['field_of_study'] = np.where(data_for_generation['comp_type'] == 'educ_comp', 'Liberal Arts',
                                            np.where(data_for_generation['comp_type'] == 'tech_comp', 'Computer Science',
                                                    np.where(data_for_generation['comp_type'] == 'med_comp', 'Medicine', None)))

    #keys to identify each resume uniquely (name + surname + comp_name + association_name)
    keys = [name + surname + comp_name + association_name for name, surname, comp_name, association_name in zip(
        data_for_generation['name'],
        data_for_generation['surname'],
        data_for_generation['comp_name'],
        data_for_generation['association']
    )]
    data_for_generation['key'] = keys

    if to_csv:
        data_path = os.path.join(os.path.dirname(__file__), "data", f"{out_filename}.csv")
        data_path = os.path.abspath(data_path)
        data_for_generation.to_csv(data_path, index=False)

    return data_for_generation


if __name__ == "__main__":
    # Example usage. Generate the database with keys.
    data_decoding=pd.read_csv('data/data_decoding.csv')
    data_desc=pd.read_csv('data/data_desc.csv')

    data_for_generation = create_resume_database(data_decoding, data_desc, to_csv=True) #this gives us the database.

    #exporting the database in csv format 
    print(data_for_generation.head())
    print(data_for_generation.columns)