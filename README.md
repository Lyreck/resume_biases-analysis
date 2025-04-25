# Installation

/!\ To clone the repository properly, please ensure you clone **recursively**. Otherwise, Resume-Matcher will not be copied properly.

`git clone --recursive https://github.com/Lyreck/resume_biases-analysis.git`

/!\ Resume-Matcher works with Python 3.11.0. 
You can install it using pyenv: `pyenv install python 3.11.0`

And then create a virtual environment using this python version: `pyenv virtualenv 3.11.00 env-name`

# Organization of the code

For the sake of clarity and readbility, we split the code in 4 main folders:
- resume_generation: all code related to generating standardized Resumes, based on a specific skillset (given a given CV, we change some select social cues, one at a time)
- job-posting_generation: all code related to generating standardized job offers from real (scraped) job offers
- cv-job_parsing: all code that relates to the automated parsing of Resumes
- score-analysis-pipeline: all the statistical work after parsing to produce our analysis.

# Methodology and disclaimers
For the moment this code only works bit-by-bit and is more a proof-of-concept than a production-ready package.
The resume sections are LLM-generated and post-processed automatically, but still require manual review in some cases (missing "-" to separate experiences for example) if one is to have a "perfect" CV generator.
We are currently working on resolving some dependcy version issues between Resume-Matcher and our own programs. *This is a work in progress*.


This code uses [Resume-Matcher](https://github.com/srbhr/Resume-Matcher) for resume parsing, and Mistral-small 3 for resume generation.
