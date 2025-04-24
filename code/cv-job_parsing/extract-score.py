#### This is just a proof of concept to recover the similarity score form a given resume.

import json
import os
import sys




# export PYTHONPATH=/home/lld_fixe/code/resume_biases-analysis/code

os.chdir("/home/lld_fixe/code/resume_biases-analysis/code/Resume_Matcher")
print(os.getcwd())

# from ..Resume_Matcher.scripts.similarity.get_score import *
# from ....Resume_Matcher.scripts.similarity.get_score import * #choper le Resume_Matcher qui est dehors
from scripts.similarity.get_score import * ## marche pas

resume_name = "john_doe.pdf" ## Enter the name of the resume (name of the file)
jd_name = "job_desc_front_end_engineer.pdf" ## Enter the name of the job description (name of the file)


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


selected_file = read_json("Data/Processed/Resumes/" + resume_name)
selected_jd = read_json("Data/Processed/JobDescription/" + jd_name)



resume_string = " ".join(selected_file["extracted_keywords"])
jd_string = " ".join(selected_jd["extracted_keywords"])
result = get_score(resume_string, jd_string)
similarity_score = round(result[0].score * 100, 2)
