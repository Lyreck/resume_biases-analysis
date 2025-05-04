## Import 
import pandas as pd 
import numpy as np
import re 


def create_resume_database(data_decoding, data_desc, to_csv=False):
    """
    This function creates a database from the given data_decoding and data_desc DataFrames.
    It processes the data to extract relevant information and combines it into a final DataFrame.
    
    Args:
        data_decoding (pd.DataFrame): DataFrame containing CV data.
        data_desc (pd.DataFrame): DataFrame containing job descriptions.
        
    Returns:
        pd.DataFrame: Final combined DataFrame with names, demographics, experience, and volunteering information.
    """
    #creating database only with job descriptions 
    #separation at line 112 
    #data_desc = data_desc[data_desc['description'].str.contains("Job Experience", case=False, na=False)]

    #creating database only with job descriptions and only with volunteering decriptions 
    #separation at line 112 


    experience_desc = data_desc[data_desc['description'].str.contains("Job Experience", case=False, na=False)]
    #print(experience_desc)

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
    experience_type = experience_type[~experience_type['company'].str.contains("NONE", case=False, na=False)]

    #print(experience_type)


    #merging experience and experience_desc databases 

    experience = pd.merge( experience_type, experience_desc, left_on='company', right_on= 'comp_name', how='outer')
    experience.drop_duplicates(subset=['nb'], inplace=True) 

    #deleting columns that are not useful anymore and renaming columns for clarity
    experience = experience.drop(columns = ['nb', 'company'])
    experience = experience.rename(columns={ "description": "job_desc"})
    #print(experience)

    #creating volunteering database 
    volunteering = data_desc[data_desc['description'].str.contains("volunteering experience", case=False, na=False)]
    volunteering= volunteering.drop(columns = ['nb'])
    #renaming columns for clarity 
    volunteering = volunteering.rename(columns={"comp_name": "association", "description": "vol_desc"})



    #creating names and demogrphics database  

    data_names = data_decoding[['name', 'surname', 'british','gender']].copy()

    #capitalizing only first letters of names and surnames 
    data_names['name'] = data_names['name'].str.capitalize()
    data_names['surname'] = data_names['surname'].str.capitalize()

    # Change "british" and "gender" to integer
    
    data_names['british'] = data_names['british'].astype(int)
    data_names['gender'] = data_names['gender'].astype(int)

    #print(data_names.head())


    #joining final database : names, demographics experience and volunteering : 
    #creating all the possible combinations 
    data_name_exp = data_names.merge(volunteering, how = "cross")
    data_for_generation = data_name_exp.merge(experience, how ='cross')

    #adding field of study column, where when it is comp_type = 'educ_comp' we add field of study = 'Liberal Arts', 
    #when it is 'tech_comp' we add field of study = 'Computer Science', and when it is 'med_comp' we add field of study = 'Medicine'
    data_for_generation['field_of_study'] = np.where(data_for_generation['comp_type'] == 'educ_comp', 'Liberal Arts',
                                            np.where(data_for_generation['comp_type'] == 'tech_comp', 'Computer Science',
                                                    np.where(data_for_generation['comp_type'] == 'med_comp', 'Medicine', None)))



    if to_csv:
        data_for_generation.to_csv('database_all_cv_combinations.csv', index=False)

    return data_for_generation

if __name__ == "__main__":
    # Example usage
    data_decoding=pd.read_csv('data/data_decoding.csv')
    data_desc=pd.read_csv('data/data_desc.csv')

    data_for_generation = create_resume_database(data_decoding, data_desc, to_csv=False) #this gives us the database.

    #exporting the database in csv format 
    print(data_for_generation.head())
    print(data_for_generation.columns)