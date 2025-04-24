#### This is just a proof of concept to recover the similarity score form a given resume.

import json
import os


from ..Resume-Matcher.scripts.similarity.get_score import *


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
