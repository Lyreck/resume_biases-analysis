from extract_score import extract_score

resume = "Resume-AlexanderRobertsAberdeen royal infirmaryAfrican impact.pdf5acaaa05-2f11-4674-9e57-4e75403eeeaf.json" #changes if resumes are parsed into json again.
job_description = "JobDescription-Administrative_AssistantAdministrativeAssistantDoneviSoftware.pdfb52c20b0-dcc4-471c-9a6c-5447cfad28b6.json" #changes if job descriptions are parsed into json again.

nb_de_tests = 1000
scores=[]
for i in range(nb_de_tests):
    score = extract_score(resume, job_description)
    if score not in scores:
        print(f"Score between {resume} and {job_description} is: {score}")
        scores.append(score)


print(f"There are {len(scores)} different scores for {nb_de_tests} tests.") #if it outputs 1, it means the score is deterministic.