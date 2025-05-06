##################################################################################
### Parse pdf files to json and extract score. ###
##################################################################################

## Old version, without multiprocessing.

# import os
# from pdf_to_json import pdf_to_json
# from extract_score import extract_score
# import pandas as pd
# import time as t

# # pdf_to_json() # parse pdf resumes in Data/Resumes and job descriptions in Data/JobDescription to json format.

# n = len(os.listdir("Data/Processed/Resumes")) * len(os.listdir("Data/Processed/JobDescription"))

# df = pd.DataFrame(columns=["Resume", "JobDescription", "Score"])

# i=0
# t0=t.time()
# for resume in os.listdir("Data/Processed/Resumes"):
#     i+=1
#     for job_description in os.listdir("Data/Processed/JobDescription"):
#         score = extract_score(resume, job_description)
#         df = pd.concat([df, pd.DataFrame([[resume, job_description, score]], columns=["Resume", "JobDescription", "Score"])])
#         print(f"Score between {resume} and {job_description} is: {score}")

#     if i == 2:
#         print(f"Estimated time to finish scoring {n} resumes, jobdesc couples: {round( ( ((t.time()-t0) / 3600 ) /i)*n,2)} hours")

# df.to_csv("../../data/dataframes/all_scores.csv", index=False)




##################################################################################
### Parse pdf files to json and extract score using multiprocessing. ###
##################################################################################

import os
from pdf_to_json import pdf_to_json
from extract_score import extract_score
import pandas as pd
import time as t
from multiprocessing import Pool, cpu_count

def process_pair(pair):
    resume, job_description = pair
    score = extract_score(resume, job_description)
    # print(f"Score between {resume} and {job_description} is: {score}")
    return (resume, job_description, score)

if __name__ == "__main__":

    

    # Prepare list of all (resume, job_description) pairs
    resume_list = os.listdir("Data/Processed/Resumes")
    job_list = os.listdir("Data/Processed/JobDescription")
    pairs = [(resume, job) for resume in resume_list for job in job_list]

    n = len(pairs)

    ###### Time estimation
    t0 = t.time()

    # Set up the pool - you can adjust the number of processes if needed
    with Pool(processes=cpu_count()-1) as pool:
        results = pool.map(process_pair, pairs[:100])

    elapsed_time = (t.time() - t0) / 3600
    print(f"Time estimation to compute score for {n} pairs (estimation sample: {100}): {(elapsed_time / 100)*n:.2f} hours.")
    ######

    # t0 = t.time()

    # # Set up the pool - you can adjust the number of processes if needed
    # with Pool(processes=cpu_count()-1) as pool:
    #     results = pool.map(process_pair, pairs)

    # elapsed_time = (t.time() - t0) / 3600
    # print(f"Finished scoring {n} pairs in {elapsed_time:.2f} hours.")

    # Convert results to DataFrame
    df = pd.DataFrame(results, columns=["Resume", "JobDescription", "Score"])

    # Ensure the output directory exists
    os.makedirs("data/dataframes/", exist_ok=True)
    df.to_csv("data/dataframes/all_scores.csv", index=False)



