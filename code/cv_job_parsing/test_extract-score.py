#### This is just a proof of concept to recover the similarity score form a given resume.

import json
import os
import sys




# export PYTHONPATH=/home/lld_fixe/code/resume_biases-analysis/code

# os.chdir("/home/lld_fixe/code/resume_biases-analysis/code/Resume_Matcher")
print(os.getcwd())

# from ..Resume_Matcher.scripts.similarity.get_score import *
# from ....Resume_Matcher.scripts.similarity.get_score import * #choper le Resume_Matcher qui est dehors
from get_score import * ## marche pas


## idéalement il faudrait passer en paramètre le .pdf. Ici je passe directement en json. Voir run_first.py pour le transfert .pdf -> json
resume_name = "Resume-alfred_pennyworth_pm.pdf6f657b71-7a59-43b4-910d-58f217a9bb4b.json" ## Enter the name of the resume (name of the file)
jd_name = "JobDescription-job_desc_front_end_engineer.pdfbe0a7c37-83ef-465d-bee3-c228722a117a.json" ## Enter the name of the job description (name of the file)


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


selected_file = read_json("Data/Processed/Resumes/" + resume_name)
selected_jd = read_json("Data/Processed/JobDescription/" + jd_name)

print(selected_file)


resume_string = " ".join(selected_file["extracted_keywords"])
jd_string = " ".join(selected_jd["extracted_keywords"])
result = get_score(resume_string, jd_string)
similarity_score = round(result[0].score * 100, 2)

print(f"Similarity score between {resume_name} and {jd_name}: {similarity_score}%")