import logging
# Get the logger
logger = logging.getLogger(__name__)
# Set the logging level
logger.setLevel(logging.INFO)

logger.info("Importing Resume Generation Functions...")

from snippet_generations import generate_descriptions
from process_LLM_generated_data import process_file #have to check if I eventually use it.

logger.info("Resume Generation Functions fully loaded.)