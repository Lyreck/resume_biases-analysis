See the project's paper here: https://pouvoirdasha.github.io/Decoding_Biases_in_Resume_Matcher/
This is a work in progress. We are working on a more polished version that will be easy to deploy on any machine with a 16GB GPU.

# Installation

/!\ When cloning the repository, if you wish to get all the functions of Resume-Matcher, please ensure you clone **recursively**. Otherwise, Resume-Matcher will not be copied properly.

=> `git clone --recursive https://github.com/Lyreck/resume_biases-analysis.git`

/!\ Resume-Matcher works with Python 3.11.0. 
- You can install it using pyenv (or other compatible system): `pyenv install python 3.11.0`
- And then create a virtual environment using this python version: `pyenv virtualenv 3.11.00 env-name`

# Organization of the code

For the sake of clarity and readability, we split the code in 4 main folders:
- resume_generation: all code related to generating standardized Resumes, based on a specific skillset (given a given CV, we change some select social cues, one at a time)
- job-posting_generation: all code related to generating standardized job offers from real (scraped) job offers
- cv-job_parsing: all code that relates to the automated parsing of Resumes
- score-analysis-pipeline: all the statistical work after parsing to produce our analysis.

# Methodology and disclaimers
For the moment this code only works bit-by-bit and is more a proof-of-concept than a production-ready package.
The resume sections are LLM-generated and post-processed automatically, but still require manual review in some cases (missing "-" to separate experiences for example) if one is to have a "perfect" CV generator.

## Known issues
1. There is a dependency issue between Resume-Matcher and ollama-python. We are currently working on resolving this. *This is a work in progress*.
2. The resume sections generator omits some parts of the sentences when it encounters a hyphen "-". This should be resolved in the future versions.


This code uses [Resume-Matcher](https://github.com/srbhr/Resume-Matcher) for resume parsing, and [Mistral-small 3](https://ollama.com/library/mistral-small) through [Ollama Python](https://github.com/ollama/ollama-python) for resume generation, though the methodology can of course be adapted to different algorithms, using a different LLM.
