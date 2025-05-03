import pandas as pd 
import numpy as np
import re 

data_cv=pd.read_csv('data_decoding.csv')
data_desc=pd.read_csv('description_offers.csv')

#creating database only with job descriptions and only with volunteering decriptions 
 #separation at line 112 

volunteering_desc = data_desc[data_desc['description'].str.contains("volunteering experience", case=False, na=False)]
experience_desc = data_desc[~data_desc['description'].str.contains("Job Experience", case=False, na=False)]


#parsing job descriptions in the database : 

def parse_description(desc):
    lines = desc.split("  - ")
    # Enlever les étoiles et blancs
    title = re.sub(r"\*\*", "", lines[0]).strip() if len(lines) > 0 else None
    position = re.sub(r"\*\*", "", lines[1]).strip() if len(lines) > 1 else None
    tasks = [line.strip() for line in lines[2:]] if len(lines) > 2 else []
    return pd.Series([title, position, tasks])

# Appliquer à la colonne
experience_desc[['job_title', 'job_position', 'task_list']] = data_desc['description'].apply(parse_description)
print(experience_desc['job_position'])
#creating names and demogrphics database  

data_names = data_cv[['name', 'surname', 'british','gender']]

#capitalizing only first letters of names and surnames 

data_names['name'] = data_names['name'].str.capitalize()
data_names['surname'] = data_names['surname'].str.capitalize()
#print(data_names.head())


#creating experience database - column from med_comp, tech_comp and educ_comp columns 

comp_columns = ['tech_comp', 'med_comp', 'educ_comp']

experience = data_cv.melt(
    id_vars=[],  # on ne garde que les colonnes à transformer
    value_vars=comp_columns,
    var_name='comp_type',
    value_name='comp_name'
).dropna(subset=['comp_name'])  # on enlève les lignes où comp_name est NaN

#creating volunteering experience database : 
volunteering = data_cv

#

"""