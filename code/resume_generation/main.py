## main file that takes the generated descriptions and build 
# - the CVs 
# the corresponding databases: 
# 1. CVkey, JobDescKey, Score
# 2. JobDesc Name, .... ??? + key
# 3. CV Name, Education Sector, .... (genre mettre dans la database toutes les infos importantes du CV) + key

import pandas as pd

from descriptions_to_pdf import insert_descriptions_to_pdf
from database_generation import create_resume_database





if __name__ == "__main__":
    data_cv=pd.read_csv('data/data_decoding.csv')
    data_desc=pd.read_csv('data/description_offers.csv')

    data_for_generation = create_resume_database(data_cv, data_desc, to_csv=False) #this gives us the database.
