import logging
# Get the logger
logger = logging.getLogger(__name__)
# Set the logging level
logger.setLevel(logging.INFO)

logger.info("Importing Resume Generation Functions...")

##  LLM generatino of snippets and post-processing
from snippet_generations import generate_descriptions
from process_LLM_generated_data import process_file #have to check if I eventually use it.

## .tex code and PDF creation 
from descriptions_to_pdf import insert_descriptions_to_pdf
from preprocess_tex_template import process_tex_string #this will be used only if the user has not pre-processed their template

## database creation 
from database_generation import create_resume_database

logger.info("Resume Generation Functions fully loaded.")