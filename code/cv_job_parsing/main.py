##################################################################################
### Parse pdf files to json and extract score. ###
##################################################################################

import os
from pdf_to_json import pdf_to_json
from extract_score import extract_score
import pandas as pd
import time as t

pdf_to_json() # parse pdf resumes in Data/Resumes and job descriptions in Data/JobDescription to json format.

n = len(os.listdir("Data/Processed/Resumes"))

df = pd.DataFrame(columns=["Resume", "JobDescription", "Score"])

i=0
t0=t.time()
for resume in os.listdir("Data/Processed/Resumes"):
    i+=1
    for job_description in os.listdir("Data/Processed/JobDescription"):
        score = extract_score(resume, job_description)
        df = pd.concat([df, pd.DataFrame([[resume, job_description, score]], columns=["Resume", "JobDescription", "Score"])])
        print(f"Score between {resume} and {job_description} is: {score}")

    if i == 2:
        print(f"Estimated time to finish generating {n} resumes: {round( ( ((t.time()-t0) / 3600 ) /i)*n,2)} hours")

df.to_csv("../../data/dataframes/all_scores.csv", index=False)


