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



    # Ensure the output directories exist
    os.makedirs("data/dataframe/name", exist_ok=True)
    os.makedirs("data/dataframe/job", exist_ok=True)
    os.makedirs("data/dataframe/volunteering", exist_ok=True)

    # Selected Job Offers (one per category - for the moment at least)
    job_offers = {"AdminAssistant": "JobDescription-Administrative_AssistantAdminAssistant(ChineseSpeaking)LoonFungLtd.pdf9dca1198-65f6-4d63-97a3-3603ee46e2ef.json", 
                  "ItOfficer": "JobDescription-IT_OfficerLossPreventionOfficerHomeSense.pdf50683fd5-e774-484d-9598-204405d0fe0e.json",
                  "Doctor": "JobDescription-DoctorMikeEdmondsDiabeticFootClinicalFellowshipKing'sCollegeHospitalNHSFoundationTrust.pdf03ccadeb-f61c-4a36-a21b-2236bab6dae9.json",
                  "Nurse": "JobDescription-NurseRegisteredNurse(RMNorRGN)EdenBrookHomeCare.pdf3daa186b-baa2-4903-91cf-1c716758d65c.json",
                  "SoftwareEng": "JobDescription-software_engineerLeadSoftwareEngineer-DeveloperPlatformJPMorganChase.pdfc6c46738-bfe0-4aa1-a2fd-3a98a60e5c85.json",
                  "Teacher": "JobDescription-TeacherSingingTeacherVictoria’sVoices.pdf50bf0fda-fb85-44e2-bf31-0f5eab0092c6.json"
                  }
    
    correspondences_names = {"AdminAssistant": {"adapted": ["AFRICAN IMPACT", "EUROPEAN COMMISSION"], "not_adapted": ["AFRICAN IMPACT", "GUY'S HOSPITAL"]}, 
                  "ItOfficer": {"adapted": ["E-GAME SOCIETY", "GOOGLE"], "not_adapted": ["E-GAME SOCIETY", "TEACHER LYCEE FRANCAIS CHARLES DE GAULLE"]},
                  "Doctor": {"adapted": ["BRITTISH RED CROSS", "ST THOMAS HOSPITAL"], "not_adapted": ["BRITTISH RED CROSS", "BAIDU"]},
                  "Nurse": {"adapted": ["VOLUNTEER IN THE LOCAL CATHOLIC CHURCH", "ST. BARTHOLOMEW'S HOSPITAL"], "not_adapted": ["VOLUNTEER IN THE LOCAL CATHOLIC CHURCH", "FREELANCE"]},
                  "SoftwareEng": {"adapted": ["JEWISH CARE", "MISTRAL"], "not_adapted": ["JEWISH CARE", "TOKYO UNIVERSITY'S HOPITAL"]},
                  "Teacher": {"adapted": ["LANGUAGE EXCHANGE SOCIETY", "TEACHING ASSISTANT KING'S COLLEGE"], "not_adapted": ["LANGUAGE EXCHANGE SOCIETY", "JOHNSONANDJONHSON"]}
                  }

    ############### ATTENTION TREAT COMPANY NAMES AND VOLUN WITH ANTI & ETC
    # comp_name = row['comp_name'].capitalize().replace("&", r"and")
    # association_name = row['association'].capitalize().replace("&", r"and")
    ############### ATTENTION TREAT COMPANY NAMES AND VOLUN WITH ANTI & ETC

    ### First experiment: make names change and fix the rest
    ## For each job offer:

    for job_offer in job_offers.keys():

    # 1: job XP is adapted to job offer
        job_XP = 

    # 2: job XP is not adapted to job offer


    ### Second experiment: make volunteering change and fix the rest
    ## For each job offer:

    # 1: job XP is adapted to job offer

    # 2: job XP is not adapted to job offer


    ### Third experiment: make job XP change and fix the rest
    ## For each job offer:

    # 1: volunteering XP is not politically clivant

    # 2: volunteering XP is politically clivant


    

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



