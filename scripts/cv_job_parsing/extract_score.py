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

    if resume_name is None or jd_name is None:
        raise ValueError(f"Error computing score between Resume and Job Description: resume_name and jd_name cannot be None (got {resume_name}, {jd_name})")

    selected_file = read_json("Data/Processed/Resumes/" + resume_name)
    selected_jd = read_json("Data/Processed/JobDescription/" + jd_name)

    resume_string = " ".join(selected_file["extracted_keywords"])
    jd_string = " ".join(selected_jd["extracted_keywords"])
    result = get_score(resume_string, jd_string)
    similarity_score = round(result[0].score * 100, 2)

    return similarity_score


def process_pair(pair):
    """Process a resume, job_description .json pair by computing their similarity score.

    Args:
        pair (tuple): contains .json names of resume and job desc to score.

    Returns:
        tuple: (resume_name, jobdesc_name, and the score between the two)
    """
    resume, job_description = pair
    score = extract_score(resume, job_description)
    # print(f"Score between {resume} and {job_description} is: {score}")
    return (resume, job_description, score)


