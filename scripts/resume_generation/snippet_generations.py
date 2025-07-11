import pandas as pd
import os 
from random import choice, randint
import logging

from ollama import chat
from ollama import ChatResponse

import logging
logger = logging.getLogger(__name__)



def generate(prompt, model='mistral-small'):
    response = chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response.message.content

def generate_descriptions(source_data_filename, out_filename="default", model='mistral-small', tech=True, med=True, edu=True, asso=True):
    """
    Function to generate descriptions for the different types of companies and associations, using mistral-small 3 and ollama.
    ollama and mistral-small 3 need to be installed locally.

    To use a different model, you will have to download it locally first, and check that your system meets the minimal requirements to run it.
    """

    logging.info(f"Fetching data from source file {source_data_filename}.csv...")
    people, comps_tech, comps_med, comps_edu, associations = read_df(source_data_filename)
    logging.info("Data fetched successfully.")

    with open(f'data/{out_filename}.csv','w') as file:

        logging.info("Starting the generation of descriptions for companies and associations with mistral-small (might take a while).")
        logging.info("Note: running the LLM locally requires at least 16GB of GPU RAM.")

        if tech: 
            for comp in comps_tech["Tech_comp"]: #add progress bar
                logging.info(f"Generating description for tech company: {comp}")
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Job experience (Tech Company): {comp}"""

                output = generate(prompt)

                file.write(comp + "," + output)
                file.write('\n')
            logging.info("Descriptions for tech companies generated.")

        if med: 
            for comp in comps_med["Med_comp"]:
                logging.info(f"Generating description for medical company: {comp}")
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Job experience (Medical): {comp}"""

                output = generate(prompt)

                file.write(comp + "," + output)
                file.write('\n')
            logging.info("Descriptions for medical companies generated.")

        if edu:
            for comp in comps_edu["Edu_comp"]:
                logging.info(f"Generating description for education-related company: {comp}")
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Job experience (Education-related company): {comp}"""

                output = generate(prompt)

                file.write(comp + "," + output)
                file.write('\n')
            logging.info("Descriptions for education-related companies generated.")

        if asso:
            for volun in associations["Volunteering"]:
                logging.info(f"Generating description for association: {volun}")
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Volunteering Experience: {volun}"""

                output = generate(prompt)

                file.write(volun + "," + output)
                file.write('\n')
            logging.info("Descriptions for associations generated.")

        logging.info("Descriptions for companies and associations generated successfully.")



def read_df(filename):
    """
    filename (str): name of the file to read. Should be located in the "data" folder.

    Returns:
        names (pd.DataFrame): DataFrame containing the names, surnames and gender of every person in the dataset
        Tech, med and edu companies, as well as association names.
    """
    
    #make filepath relative to project root.
    data_path = os.path.join(os.path.dirname(__file__), "data", f"{filename}.csv")
    data_path = os.path.abspath(data_path)
    
    names = pd.read_csv(data_path)
    names.columns=["Name", "Surname", "British", "Volunteering", "Gender", "Tech_comp", "Med_comp", "Edu_comp", "Field_study"]


    people = names[["Name", "Surname", "Gender"]].dropna()#.to_list()
    associations = names[["Volunteering"]].dropna()#.to_list()

    comps_tech = names[["Tech_comp"]].dropna().drop_duplicates()#.to_list()
    comps_med = names[["Med_comp"]].dropna().drop_duplicates()#.to_list()
    comps_edu = names[["Edu_comp"]].dropna().drop_duplicates()#.to_list()

    return people, comps_tech, comps_med, comps_edu, associations #To keep track of who is being generated



 
if __name__ == "__main__":

    names = pd.read_csv("data/names_clean.csv")
    names.columns=["Name", "Surname", "British", "Volunteering", "Gender", "Tech_comp", "Med_comp", "Edu_comp", "Field_study"]
 
                    
    people = names[["Name", "Surname", "Gender"]].dropna()#.to_list()
    associations = names[["Volunteering"]].dropna()#.to_list()

    comps_tech = names[["Tech_comp"]].dropna().drop_duplicates()#.to_list()
    comps_med = names[["Med_comp"]].dropna().drop_duplicates()#.to_list()
    comps_edu = names[["Edu_comp"]].dropna().drop_duplicates()#.to_list()

    tech, med, edu, asso = False, False, False, True
    print(tech, med, edu, asso) #To keep track of who is being generated

    generate_descriptions(comps_tech, comps_med, comps_edu, associations, tech=tech, med=med, edu=edu, asso=asso)