from extract_score import extract_score

resume = "Resume-cv_AMAN_SINGH.pdf2382af65-15c7-4eb8-b9e8-c7360b0c1a65.json" #changes if resumes are parsed into json again.
job_description = "JobDescription-Junior Software Engineer.pdfed68cfce-72fe-4845-9872-3f96a11f39c7.json" #changes if job descriptions are parsed into json again.

nb_de_tests = 1000
scores=[]
for i in range(nb_de_tests):
    score = extract_score(resume, job_description)
    if score not in scores:
        print(f"Score between {resume} and {job_description} is: {score}")
        scores.append(score)


print(f"There are {len(scores)} different scores for {nb_de_tests} tests.") #if it outputs 1, it means the score is deterministic.