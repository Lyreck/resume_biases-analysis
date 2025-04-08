# Organization of the code

For the sake of clarity and readbility, we split the code in 4 main folders:
- resume_generation: all code related to generating standardized Resumes, based on a specific skillset (given a given CV, we change some select social cues, one at a time)
- job-posting_generation: all code related to generating standardized job offers from real (scraped) job offers
- cv-job_parsing: all code that relates to the automated parsing of Resumes
- score-analysis-pipeline: all the statistical work after parsing to produce our analysis.


This code uses [Resume-Matcher](https://github.com/srbhr/Resume-Matcher) for resume parsing, and Mistral-small 3 for resume generation.
