### In this code, we build the functions to take a set of selected descriptions (job, name, association...) and put them in a given .tex format. ###
### The function then outputs a .pdf file which will be analyzed in the next step (cv_job_parsing). ################################################
### The name of the pdf resume file is built as follows: name + surname + company_name + association_name .pdf. This allows for a **unique** name for each resume.
### Other functions allow us to create databases to make our analysis. ###########################


from .utils.process_markdown_description import process_markdown_job, process_markdown_association
import os
import subprocess
import logging
logger = logging.getLogger(__name__)

def insert_descriptions_to_pdf(name, company_name, job_desc, association_name, association_desc, field_of_study, out_directory="data/generated_resumes", resume_filename= "output_resume", verbose=False): 
    """
    Takes the info from our database, and LLM-generated descriptions, and insert them into a LaTeX template then rendered into a PDF.
    Outputs by default the .pdf resume in the data/generated_resumes directory (subject to change in the future).
    resume_filename should be the hash of the whole concatenated line of the database.
    """

    email = f"{'.'.join(name.split())}@gmail.com"
    linkedin = f"linkedin.com/in/{''.join(name.split())}"
    github = f"github.com/{''.join(name.split())}"


    ############## Education Section ############ 
    university, location, field_of_study = "University of Southampton", "Southampton", field_of_study
    # university, location, field_of_study = process_markdown_education(education) #cmd + SHIFT + : pour décommenter les lignes.
    education_section = r'''\resumeSubheading
          {{''' + f"{university}" + r'''}}{{''' + f"{location}" + r'''}}
          {{Bachelor in ''' + f"{field_of_study}" + r'''}}{{Aug. 2018 -- May 2021}}
          '''
    

    ############## Company Section ##############
    #pre-process LLM-generated markdown description
    title, company_name2, items = process_markdown_job(job_desc)
    company_section = r'''\resumeSubheading{{''' + f"{title}" + r'''}}{{June 2020 -- Present}}
          {{''' + f"{company_name}" + r'''}}{{}}
          \resumeItemListStart
          '''
    for item in items: 
      company_section += r'''\resumeItem{{''' + f"{item} " + r'''}}
      '''
    company_section += r'''\resumeItemListEnd''' #end the company section
    

    ############## Association Section ##############
    #pre-process LLM-generated markdown description
    association_name2, items = process_markdown_association(association_desc)
    association_section = r''' \resumeProjectHeading{{ \textbf{{''' + f'{association_name}' + r'''}} }}{{June 2020 -- Present}}
              \resumeItemListStart
              '''
    for item in items:
      association_section += r'''\resumeItem{{''' + f"{item} " + r'''}}
      '''
    association_section += r'''\resumeItemListEnd'''


    ## open tex template
    tex_template_data_path = os.path.join(os.path.dirname(__file__), "data", f"tex_template.tex")
    tex_template_data_path = os.path.abspath(tex_template_data_path)
    with open (tex_template_data_path, "r") as f:
      tex_template = f.read() #processed file with process_tex_string.

    #Replace placeholders {name}, {email}, {association}, etc.. with actual values
    latex_code = tex_template.format(name=name, 
                                     email=email, 
                                     linkedin=linkedin, 
                                     github=github, 
                                     company=company_section, 
                                     association=association_section,
                                     education=education_section)
    
    # Ensure the output directory exists
    os.makedirs(out_directory, exist_ok=True)

    # Name of the resume file
    # resume_filename = "output_resume"  ##CHANGE RESUME NAME

    # Write the LaTeX code to a .tex file
    tex_filename = os.path.join(out_directory, resume_filename + ".tex")
    
    with open(tex_filename, "w") as tex_file:
        tex_file.write(latex_code)

    # Compile the .tex file into a PDF using pdflatex
    try:
        if verbose:
          subprocess.run(["pdflatex", "-output-directory", out_directory, resume_filename + ".tex"], check=True) # with verbose
        else:
          with open(os.devnull, 'w') as devnull: #without verbose
              subprocess.run(
                  ["pdflatex", "-output-directory", out_directory, resume_filename + ".tex"],
                  stdout=devnull,  # Suppress standard output
                  stderr=devnull,  # Suppress error output
                  check=True
              )
        if verbose:
          logging.info(f"PDF generated successfully: {os.path.join(out_directory, resume_filename + '.pdf')}")
    except subprocess.CalledProcessError as e:
        logging.warning(f"Error during PDF generation: {e}")

    # Clean up auxiliary files generated by pdflatex #also clean up the .tex file
    for ext in [".aux", ".log", ".out", ".tex"]:
        aux_file = os.path.join(out_directory, f"{resume_filename}{ext}")
        if os.path.exists(aux_file):
            os.remove(aux_file)







if __name__ == "__main__":
    


    # Example usage to generate a Resume with given name, company expereince and assocation descriptions.
    name = "Jake Ryan"
    company_name = "Dyson"
    comp_desc = "**Job Experience**  - **Senior Software Engineer at Dyson**   - Developed and maintained software solutions for Dyson's innovative products, focusing on embedded systems and IoT technologies.  - Collaborated with cross-functional teams to integrate hardware and software components seamlessly.  - Implemented agile methodologies to ensure timely delivery of high-quality software updates.  -  Conducted thorough testing and debugging to enhance product performance and reliability.  - Contributed to the development of user-friendly interfaces and intuitive control systems for Dyson's smart home devices. "
    association_name="African Impact"
    association_desc = "**Volunteering Experience at African Impact** - Dedicated over 100 hours to African Impact, a leading volunteer organization in Africa. - Assisted in community development projects, including education and conservation efforts. - Collaborated with local teams to implement sustainable initiatives that positively impacted rural communities. - Facilitated educational workshops for children, enhancing their learning experiences and fostering a love for education. - Participated in environmental conservation activities such as tree planting and beach clean-ups, promoting ecological sustainability. - Engaged with diverse cultural groups, gaining valuable insights into African traditions and lifestyles while contributing to meaningful community projects. "
    field_of_study = "Computer Science"
    resume_filename = name + company_name + association_name
    #generate resume in .pdf format
    insert_descriptions_to_pdf(name, company_name, comp_desc, association_name, association_desc, field_of_study, out_directory="data/generated_resumes", resume_filename=resume_filename, verbose=True)
    