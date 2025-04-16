import pandas as pd
import os 
from random import choice, randint

from ollama import chat
from ollama import ChatResponse
#print(os.getcwd())


names = pd.read_csv("data/names_clean.csv", 
                    names=["Name", "Surname", "Associations", "Gender", "Tech_comp", "Medical_comp", "Education_comp"])

# print(names.head())

def generate(prompt):
    response = chat(model='mistral-small', messages=[
        {
            'role': 'user',
            'content': prompt,
        },
    ])

    return response.message.content


people = names[["Name", "Surname", "Gender"]]#.to_list()
associations = names[["Associations"]]#.to_list()

comps_tech = names[["Tech_comp"]]#.to_list()
comps_med = names[["Medical_comp"]]#.to_list()
comps_edu = names[["Education_comp"]]#.to_list()

with open('out_files/out.csv','w') as file:

    for comp in comps_tech.iterrows():
        print(comp)
        prompt = f"""
        You are a resume section generator. I will give
        you a characteristic. You will extrapolate a reasonable description of the corresponding experience.

        Output the result in .csv format, with the following columns: "Characteristic", "Description". Di not write the columns, only the data.
        
        The characteristic is: Job experience (Tech Company): {comp}"""

        output = generate(prompt)

        file.write(output)
        file.write('\n')

    for comp in comps_med.iterrows():
        print(comp)
        prompt = f"""
        You are a resume section generator. I will give
        you a characteristic. You will extrapolate a reasonable description of the corresponding experience.

        Output the result in .csv format, with the following columns: "Characteristic", "Description". Di not write the columns, only the data.
        
        The characteristic is: Job experience (Medical): {comp}"""

        output = generate(prompt)

        file.write(output)
        file.write('\n')

    for comp in comps_edu.iterrows():
        print(comp)
        prompt = f"""
        You are a resume section generator. I will give
        you a characteristic. You will extrapolate a reasonable description of the corresponding experience.

        Output the result in .csv format, with the following columns: "Characteristic", "Description". Di not write the columns, only the data.
        
        The characteristic is: Job experience (Education-related company): {comp}"""

        output = generate(prompt)

        file.write(output)
        file.write('\n')

    for volun in associations.iterrows():
        print(volun)
        prompt = f"""
        You are a resume section generator. I will give
        you a characteristic. You will extrapolate a reasonable description of the corresponding experience.

        Output the result in .csv format, with the following columns: "Characteristic", "Description". Di not write the columns, only the data.
        
        The characteristic is: Volunteering Experience: {volun}"""

        output = generate(prompt)

        file.write(output)
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


""" 
if __name__ == "__main__":
    # Run the function to generate the resume
    generate_resume() """