##################################################################################
### Parse pdf files to json and extract score. ###
##################################################################################

import os
from pdf_to_json import pdf_to_json
from extract_score import extract_score
import pandas as pd

pdf_to_json() # parse pdf resumes in Data/Resumes and job descriptions in Data/JobDescription to json format.

df = pd.DataFrame(columns=["Resume", "JobDescription", "Score"])

for resume in os.listdir("Data/Processed/Resumes"):
    for job_description in os.listdir("Data/Processed/JobDescription"):
        score = extract_score(resume, job_description)
        df = pd.concat([df, pd.DataFrame([[resume, job_description, score]], columns=["Resume", "JobDescription", "Score"])])
        print(f"Score between {resume} and {job_description} is: {score}")

print(df)