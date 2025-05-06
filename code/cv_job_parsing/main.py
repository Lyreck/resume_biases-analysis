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

from fetch_specific_resumes import fetch_resume, fetch_job_offer

def process_pair(pair):
    resume, job_description = pair
    score = extract_score(resume, job_description)
    # print(f"Score between {resume} and {job_description} is: {score}")
    return (resume, job_description, score)

if __name__ == "__main__":
    first_experiment, second_experiment, third_experiment = True, True, True
    

    database = pd.read_csv("data/dataframes/database_all_cv_combinations_with_keys.csv") #this gives us the database.
    

    # Ensure the output directories exist
    os.makedirs("data/dataframes/name", exist_ok=True)
    os.makedirs("data/dataframes/job", exist_ok=True)
    os.makedirs("data/dataframes/volunteering", exist_ok=True)

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
                  "Nurse": {"adapted": ["JEHOVAH'S WITNESSES", "QUEEN ELIZABETH HOSPITAL BIRMINGHAM"], "not_adapted": ["JEHOVAH'S WITNESSES", "FREELANCE"]},
                  "SoftwareEng": {"adapted": ["JEWISH CARE", "MISTRAL"], "not_adapted": ["JEWISH CARE", "TOKYO UNIVERSITY'S HOPITAL"]},
                  "Teacher": {"adapted": ["LANGUAGE EXCHANGE SOCIETY", "TEACHING ASSISTANT KING'S COLLEGE"], "not_adapted": ["LANGUAGE EXCHANGE SOCIETY", "JOHNSONANDJONHSON"]}
                  }
    
    correspondences_volunteering = {"AdminAssistant": {"adapted": ["OLIVER SMITH", "EUROPEAN COMMISSION"], "not_adapted": ["OLIVER SMITH", "GUY'S HOSPITAL"]}, 
                  "ItOfficer": {"adapted": ["KAMRAN AHMED", "GOOGLE"], "not_adapted": ["KAMRAN AHMED", "TEACHER LYCEE FRANCAIS CHARLES DE GAULLE"]},
                  "Doctor": {"adapted": ["WILLIAM MONTGOMERY", "ST THOMAS HOSPITAL"], "not_adapted": ["WILLIAM MONTGOMERY", "BAIDU"]},
                  "Nurse": {"adapted": ["IRINA IVANOVA", "QUEEN ELIZABETH HOSPITAL BIRMINGHAM"], "not_adapted": ["IRINA IVANOVA", "FREELANCE"]},
                  "SoftwareEng": {"adapted": ["SOPHIA PHILLIPS", "MISTRAL"], "not_adapted": ["SOPHIA PHILLIPS", "TOKYO UNIVERSITY'S HOPITAL"]},
                  "Teacher": {"adapted": ["JACK JONES", "TEACHING ASSISTANT KING'S COLLEGE"], "not_adapted": ["JACK JONES", "JOHNSONANDJONHSON"]}
                  }
    
    correspondences_company = {"AdminAssistant": {"clivant": ["OLIVER SMITH", "CHILDREN OF ABRAHAM"], "not_clivant": ["OLIVER SMITH", "AFRICAN IMPACT"]}, 
                  "ItOfficer":  {"clivant": ["KAMRAN AHMED", "GREEN PARTY OF ENGLAND AND WALES"], "not_clivant": ["KAMRAN AHMED", "E-GAME SOCIETY"]},
                  "Doctor":  {"clivant": ["OLIVIA DUPONT", "ANIME SOCIETY"], "not_clivant": ["OLIVIA DUPONT", "BRITTISH RED CROSS"]},
                  "Nurse": {"clivant": ["IRINA IVANOVA", "JEHOVAH'S WITNESSES"], "not_clivant": ["IRINA IVANOVA", "IMPROVISATION THEATER SOCIETY"]},
                  "SoftwareEng": {"clivant": ["MOHAMMED KHAN", "JEWISH CARE"], "not_clivant": ["MOHAMMED KHAN", "E-GAME SOCIETY"]},
                  "Teacher":  {"clivant": ["JACK JONES", "MIGRANT HELP"], "not_clivant": ["JACK JONES", "LANGUAGE EXCHANGE SOCIETY"]}
                  }

    # Stuff through which we iterate
    namessurnames = database[['name', 'surname']].drop_duplicates()
    names = namessurnames['name'].tolist()
    surnames = namessurnames['surname'].tolist()
    names = [names[i] + " " + surnames[i] for i in range(len(names))]
    job_experiences = [string.capitalize().replace("&", r"and") for string in database['comp_name'].drop_duplicates()]
    association_names = [string.capitalize().replace("&", r"and") for string in database['association'].drop_duplicates()]

    ############### ATTENTION TREAT COMPANY NAMES AND VOLUN WITH ANTI & ETC
    # comp_name = row['comp_name'].capitalize().replace("&", r"and")
    # association_name = row['association'].capitalize().replace("&", r"and")
    ############### ATTENTION TREAT COMPANY NAMES AND VOLUN WITH ANTI & ETC


    if first_experiment:
        ### First experiment: make names change and fix the rest
        print(f"################## Beginning of Experiment 1 (making names vary) ##################")
        ## For each job offer:

        for job_type in job_offers.keys():
            job_offer_json_name = fetch_job_offer(job_offers[job_type])

        # 1: job XP is adapted to job offer
            volunteering_XP, job_XP = correspondences_names[job_type]["adapted"]

            #Compute the score on ALL names from our database and add these scores to the score database.
            scores, resume_names, non_generated_resumes = [], [], 0
            for name in names:
                resume_name = name + job_XP + volunteering_XP #reminder: in this particular case, name = name + surname, so we don't need to add the surname again.
                try:
                    resume_json_name = fetch_resume(resume_name)
                    resume_names.append(resume_name)

                    scores.append(extract_score(resume_json_name, job_offer_json_name))

                except ValueError as e:
                    non_generated_resumes+=1 #if fetching fails and raises a ValueError, we count it as a non generated resume (it means it was in the database, but the .tex was bugged). 

            # Save the scores to a CSV file
            data = {"Resume": resume_names, "JobDescription": [job_offer_json_name for _ in resume_names], "Score": scores, "adapted": [1 for _ in resume_names]} #job_offer_json_name should change to the pdf file if we want to automate the whole thing and stay coherent with the key for the Resume database.
            df = pd.DataFrame(data=data)
            df.to_csv(f"data/dataframes/name/{job_type}_{job_XP.replace(' ', '').capitalize()}_{volunteering_XP.replace(' ', '').capitalize()}.csv", index=False) #format: type of job offer, job experience, and volunteering. This is done to be able to trace experiments.

            print(f"Finished part 1 of Experiment 1 (making names vary) for {job_type}. While fetching json files, we found {non_generated_resumes} non-generated resumes.")

        # 2: job XP is not adapted to job offer
        for job_type in job_offers.keys():
            job_offer_json_name = fetch_job_offer(job_offers[job_type])
            volunteering_XP, job_XP = correspondences_names[job_type]["not_adapted"]

            #Compute the score on ALL names from our database and add these scores to the score database.
            scores, resume_names, non_generated_resumes = [], [], 0
            for name in names:
                resume_name = name + job_XP + volunteering_XP #reminder: in this particular case, name = name + surname, so we don't need to add the surname again.
                try:
                    resume_json_name = fetch_resume(resume_name)
                    resume_names.append(resume_name)

                    scores.append(extract_score(resume_json_name, job_offer_json_name))

                except ValueError as e:
                    non_generated_resumes+=1 #if fetching fails and raises a ValueError, we count it as a non generated resume (it means it was in the database, but the .tex was bugged). 

            # Save the scores to a CSV file
            data = {"Resume": resume_names, "JobDescription": [job_offer_json_name for _ in resume_names], "Score": scores, "adapted": [0 for _ in resume_names]} #job_offer_json_name should change to the pdf file if we want to automate the whole thing and stay coherent with the key for the Resume database.
            df = pd.DataFrame(data=data)
            df.to_csv(f"data/dataframes/name/{job_type}_{job_XP.replace(' ', '').capitalize()}_{volunteering_XP.replace(' ', '').capitalize()}.csv", index=False) #format: type of job offer, job experience, and volunteering. This is done to be able to trace experiments.

            print(f"Finished part 2 (not_adapted) of Experiment 1 (making names vary) for {job_type}. While fetching json files, we found {non_generated_resumes} non-generated resumes.")



    ### Second experiment: make volunteering change and fix the rest
    if second_experiment :
        print(f"################## Beginning of Experiment 2 (making volunteering XP vary) ##################")
        ## For each job offer:
        for job_type in job_offers.keys():
            job_offer_json_name = fetch_job_offer(job_offers[job_type])

        # 1: job XP is adapted to job offer
            name, job_XP = correspondences_volunteering[job_type]["adapted"]

            scores, resume_names, non_generated_resumes = [], [], 0
            for asso in association_names:
                resume_name = name + job_XP + asso

                try:
                    resume_json_name = fetch_resume(resume_name)
                    resume_names.append(resume_name)

                    scores.append(extract_score(resume_json_name, job_offer_json_name))

                except ValueError as e:
                    non_generated_resumes+=1 #if fetching fails and raises a ValueError, we count it as a non generated resume (it means it was in the database, but the .tex was bugged). 

            # Save the scores to a CSV file
            data = {"Resume": resume_names, "JobDescription": [job_offer_json_name for _ in resume_names], "Score": scores, "adapted": [1 for _ in resume_names]} #job_offer_json_name should change to the pdf file if we want to automate the whole thing and stay coherent with the key for the Resume database.
            df = pd.DataFrame(data=data)
            df.to_csv(f"data/dataframes/volunteering/{job_type}_{job_XP.replace(' ', '').capitalize()}_{name.replace(' ', '').capitalize()}.csv", index=False) #format: type of job offer, job experience, and volunteering. This is done to be able to trace experiments.

            print(f"Finished part 1 of Experiment 2 (making volunteering XPs vary) for {job_type}. While fetching json files, we found {non_generated_resumes} non-generated resumes.")


        # 2: job XP is not adapted to job offer

        for job_type in job_offers.keys():
            job_offer_json_name = fetch_job_offer(job_offers[job_type])

            name, job_XP = correspondences_volunteering[job_type]["not_adapted"]

            scores, resume_names, non_generated_resumes = [], [], 0
            for asso in association_names:
                resume_name = name + job_XP + asso

                try:
                    resume_json_name = fetch_resume(resume_name)
                    resume_names.append(resume_name)

                    scores.append(extract_score(resume_json_name, job_offer_json_name))

                except ValueError as e:
                    non_generated_resumes+=1 #if fetching fails and raises a ValueError, we count it as a non generated resume (it means it was in the database, but the .tex was bugged). 

            # Save the scores to a CSV file
            data = {"Resume": resume_names, "JobDescription": [job_offer_json_name for _ in resume_names], "Score": scores, "adapted": [0 for _ in resume_names]} #job_offer_json_name should change to the pdf file if we want to automate the whole thing and stay coherent with the key for the Resume database.
            df = pd.DataFrame(data=data)
            df.to_csv(f"data/dataframes/volunteering/{job_type}_{job_XP.replace(' ', '').capitalize()}_{name.replace(' ', '').capitalize()}.csv", index=False) #format: type of job offer, job experience, and volunteering. This is done to be able to trace experiments.

            print(f"Finished part 2 (not_adapted) of Experiment 2 (making volunteering XPs vary) for {job_type}. While fetching json files, we found {non_generated_resumes} non-generated resumes.")



    ### Third experiment: make job XP change and fix the rest
    if third_experiment:
        print(f"################## Beginning of Experiment 3 (making job XP vary) ##################")
        ## For each job offer:
        for job_type in job_offers.keys():
            job_offer_json_name = fetch_job_offer(job_offers[job_type])

        # 1: volunteering XP is not politically clivant
            name,asso = correspondences_company[job_type]["not_clivant"]

            scores, resume_names, non_generated_resumes = [], [], 0
            for job_XP in job_experiences:
                resume_name = name + job_XP + asso

                try:
                    resume_json_name = fetch_resume(resume_name)
                    resume_names.append(resume_name)

                    scores.append(extract_score(resume_json_name, job_offer_json_name))

                except ValueError as e:
                    non_generated_resumes+=1 #if fetching fails and raises a ValueError, we count it as a non generated resume (it means it was in the database, but the .tex was bugged). 

            # Save the scores to a CSV file
            data = {"Resume": resume_names, "JobDescription": [job_offer_json_name for _ in resume_names], "Score": scores, "clivant": [0 for _ in resume_names]} #job_offer_json_name should change to the pdf file if we want to automate the whole thing and stay coherent with the key for the Resume database.
            df = pd.DataFrame(data=data)
            df.to_csv(f"data/dataframes/job/{job_type}_{job_XP.replace(' ', '').capitalize()}_{name.replace(' ', '').capitalize()}.csv", index=False) #format: type of job offer, job experience, and volunteering. This is done to be able to trace experiments.

            print(f"Finished part 1 (not_clivant) of Experiment 3 (making volunteering XPs vary) for {job_type}. While fetching json files, we found {non_generated_resumes} non-generated resumes.")

        # 2: volunteering XP is politically clivant

        for job_type in job_offers.keys():
            job_offer_json_name = fetch_job_offer(job_offers[job_type])

            name,asso = correspondences_company[job_type]["clivant"]

            scores, resume_names, non_generated_resumes = [], [], 0
            for job_XP in job_experiences:
                resume_name = name + job_XP + asso

                try:
                    resume_json_name = fetch_resume(resume_name)
                    resume_names.append(resume_name)

                    scores.append(extract_score(resume_json_name, job_offer_json_name))

                except ValueError as e:
                    non_generated_resumes+=1 #if fetching fails and raises a ValueError, we count it as a non generated resume (it means it was in the database, but the .tex was bugged). 

            # Save the scores to a CSV file
            data = {"Resume": resume_names, "JobDescription": [job_offer_json_name for _ in resume_names], "Score": scores, "clivant": [1 for _ in resume_names]} #job_offer_json_name should change to the pdf file if we want to automate the whole thing and stay coherent with the key for the Resume database.
            df = pd.DataFrame(data=data)
            df.to_csv(f"data/dataframes/job/{job_type}_{job_XP.replace(' ', '').capitalize()}_{name.replace(' ', '').capitalize()}.csv", index=False) #format: type of job offer, job experience, and volunteering. This is done to be able to trace experiments.

            print(f"Finished part 2 (clivant) of Experiment 3 (making volunteering XPs vary) for {job_type}. While fetching json files, we found {non_generated_resumes} non-generated resumes.")


    




    ##################### CODE FOR MULTIPROCESSING EVERYTHING VERSON ######################

    # Prepare list of all (resume, job_description) pairs
    # resume_list = os.listdir("Data/Processed/Resumes")
    # job_list = os.listdir("Data/Processed/JobDescription")
    # pairs = [(resume, job) for resume in resume_list for job in job_list]

    # n = len(pairs)

    # ###### Time estimation
    # t0 = t.time()

    # # Set up the pool - you can adjust the number of processes if needed
    # with Pool(processes=cpu_count()-1) as pool:
    #     results = pool.map(process_pair, pairs[:100])

    # elapsed_time = (t.time() - t0) / 3600
    # print(f"Time estimation to compute score for {n} pairs (estimation sample: {100}): {(elapsed_time / 100)*n:.2f} hours.")
    ######

    # t0 = t.time()

    # # Set up the pool - you can adjust the number of processes if needed
    # with Pool(processes=cpu_count()-1) as pool:
    #     results = pool.map(process_pair, pairs)

    # elapsed_time = (t.time() - t0) / 3600
    # print(f"Finished scoring {n} pairs in {elapsed_time:.2f} hours.")

    # Convert results to DataFrame
    # df = pd.DataFrame(results, columns=["Resume", "JobDescription", "Score"])

    # Ensure the output directory exists
    # os.makedirs("data/dataframes/", exist_ok=True)
    # df.to_csv("data/dataframes/all_scores.csv", index=False)



