import sys

from code.resume_generation.snippet_generation import generate_descriptions
# en gros dans le init je mets direct les packages que je veux importer :)))))))))))

if __name__ == "__main__":
    # To run, you need to specify the following parameters:
    resume_characteristics = sys.argv[1] # filepath to a .csv containing everything we need to generate resumes.
    # This .csv should have the following columns: name,surname,british,volunteering,gender,tech_comp,med_comp,educ_comp,field_study
    # Convention: 1 is british, 0 is not. 1 is female, 0 is male.