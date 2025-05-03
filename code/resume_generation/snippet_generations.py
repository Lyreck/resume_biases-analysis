import pandas as pd
import os 
from random import choice, randint

from ollama import chat
from ollama import ChatResponse


def generate(prompt):
    response = chat(model='mistral-small', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response.message.content

def generate_descriptions(comps_tech, comps_med, comps_edu, associations, tech=True, med=True, edu=True, asso=True):
    """
    Function to generate descriptions for the different types of companies and associations, using mistral-small 3 and ollama.
    ollama and mistral-small 3 need to be installed locally.
    """

    with open('out_files/out2.csv','w') as file:

        if tech: 
            for i,_ in comps_tech.iterrows():
                comp = comps_tech.iloc[i]["Tech_comp"]
                print(comp)
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Job experience (Tech Company): {comp}"""

                output = generate(prompt)

                file.write(comp + "," + output)
                file.write('\n')

        if med: 
            for i,_ in comps_med.iterrows():
                comp = comps_med.iloc[i]["Med_comp"]
                print(comp)
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Job experience (Medical): {comp}"""

                output = generate(prompt)

                file.write(comp + "," + output)
                file.write('\n')

        if edu:
            for i,_ in comps_edu.iterrows():
                comp = comps_edu.iloc[i]["Edu_comp"]
                print(comp)
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Job experience (Education-related company): {comp}"""

                output = generate(prompt)

                file.write(comp + "," + output)
                file.write('\n')

        if asso:
            for i,_ in associations.iterrows():
                volun = associations.iloc[i]["Associations"]
                print(volun)
                prompt = f"""
                You are a resume section generator. I will give
                you a characteristic. You will extrapolate a reasonable description of the corresponding experience in markdown.

                Output the result in markdown format. Do not write any "," or ";". Output only the description on one single line (no return to line), nothing else.
                
                The characteristic is: Volunteering Experience: {volun}"""

                output = generate(prompt)

                file.write(volun + "," + output)
                file.write('\n')






"""
Here is the information of the person:
Name: {people[0]}
Surname: {people[1]}
Gender: {people[2]}
Association: {association}
Company: {comp}
Location: United Kindgom
Email: {people[0]}.{people[1]}@gmail.com
LinkedIn: linkedin.com/in/{people[0]}{people[1]}"""


 
if __name__ == "__main__":

    names = pd.read_csv("data/names_clean.csv", 
                    names=["Name", "Surname", "Associations", "Gender", "Tech_comp", "Med_comp", "Edu_comp", "field_of_study", "University"])

    people = names[["Name", "Surname", "Gender"]].dropna()#.to_list()
    associations = names[["Associations"]].dropna()#.to_list()

    comps_tech = names[["Tech_comp"]].dropna().drop_duplicates()#.to_list()
    comps_med = names[["Med_comp"]].dropna().drop_duplicates()#.to_list()
    comps_edu = names[["Edu_comp"]].dropna().drop_duplicates()#.to_list()

    tech, med, edu, asso = False, False, False, True
    print(tech, med, edu, asso) #To keep track of who is being generated

    generate_descriptions(comps_tech, comps_med, comps_edu, associations, tech=tech, med=med, edu=edu, asso=asso)