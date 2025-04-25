import json
import os

from get_score import *


def read_json(filename):
    with open(filename) as f:
        data = json.load(f)
    return data


    # This function is not implemented in the provided code.
    pass

def extract_score(resume_name, jd_name):
    """
    The function `extract_score` calculates the similarity score between a resume and a job description
    using the `get_score` function.

    Args:
        resume_name (str): The name of the resume file.
        jd_name (str): The name of the job description file.

    Returns:
        float: The similarity score between the resume and job description.
    """
    selected_file = read_json("Data/Processed/Resumes/" + resume_name)
    selected_jd = read_json("Data/Processed/JobDescription/" + jd_name)

    resume_string = " ".join(selected_file["extracted_keywords"])
    jd_string = " ".join(selected_jd["extracted_keywords"])
    result = get_score(resume_string, jd_string)
    similarity_score = round(result[0].score * 100, 2)

    return similarity_score


