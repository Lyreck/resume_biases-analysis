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

df.to_csv("../../data/dataframes/presentation_scores.csv", index=False)



resume = "Resume-cv_AMAN_SINGH.pdf7a1f59e9-e81a-43e2-b8a6-b8b230092952.json"
job_description = "JobDescription-Junior Software Engineer.pdfce7a2542-7fb9-4380-87bc-1bbe28f37894.json"

nb_de_tests = 100
scores=[]
for i in range(nb_de_tests):
    score = extract_score(resume, job_description)
    if score not in scores:
        print(f"Score between {resume} and {job_description} is: {score}")
        scores.append(score)
