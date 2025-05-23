import pandas as pd

from pylatex import Document, Section, Itemize, Command
from pylatex.utils import NoEscape

import re
import os

######################## Copilot proposal ########################

def transform_description_to_latex(description):
    # Replace **bold** with LaTeX \textbf{}
    description = description.replace("**", "\\textbf{", 1).replace("**", "}", 1)
    # Replace *item with LaTeX itemize format
    items = description.split("*")[1:]  # Split by * and ignore the first part
    if items:
        description = items[0]  # First part before items
        item_list = items[1:]  # Remaining items
        return description, item_list
    return description, []

def generate_pdf_from_dataframe(csv_file, output_pdf):
    # Read the CSV file
    df = pd.read_csv(csv_file)

    # Create a LaTeX document
    doc = Document()

    # Add content to the document
    with doc.create(Section("Job Descriptions")):
        for _, row in df.iterrows():
            description, items = transform_description_to_latex(row["description"])
            doc.append(description)
            if items:
                with doc.create(Itemize()) as itemize:
                    for item in items:
                        itemize.add_item(item)

    # Generate the PDF
    doc.generate_pdf(output_pdf, clean_tex=False)

######################## Copilot proposal ########################


def process_markdown_to_latex(input_string):
    """
    Transforms a string by:
    1. Replacing **XXX** with \textbf{XXX}.
    2. Replacing *XXX* with \begin{itemize} \item XXX \end{itemize}.
    """

    #remove un-necessary \
    input_string = input_string.replace('\\', "")

    # Replace **any text** with \textbf{any text}
    input_string = re.sub(r"\*\*(.*?)\*\*", NoEscape(r"\\textbf{\1}"), input_string)

    # Replace *XXX (only if it starts a new line and is not **XXX**) with \begin{itemize} \item XXX \end{itemize}
    input_string = re.sub(
        r'(?<!\*)\*\s*(?!\*)([^\n]+)',
        NoEscape(r"\\begin{itemize} \\item \1 \\end{itemize}"),
        input_string,
        flags=re.MULTILINE,
    )

    #remove un-necessary % and &
    input_string = input_string.replace("%", "\%")
    input_string = input_string.replace("&", r"and")
    input_string = input_string.replace("#", "")
    input_string = input_string.replace("@", "at")
    input_string = input_string.replace("*", "")



    return input_string

def jobdesc_to_pdf(csv_file, job_name, out_directory):
    #job_name is the name of the job considered: Doctor, IT Officer, etc.

    df = pd.read_csv(csv_file)

    # Ensure the output directory exists
    os.makedirs(out_directory, exist_ok=True)

    nb_of_failed=0

    for index, row in df.iterrows(): #for each job description
        doc = Document("basic")

        jobtitle = row["title"]
        company = row["company"]
        description = row["description"]

        if isinstance(jobtitle, str) and isinstance(company,str): #if the job offer has no jobtitle or company, not interesting.
            
            filename = "".join( (job_name + jobtitle+company).split())

            doc.preamble.append(Command("title", jobtitle))
            doc.preamble.append(Command("author", company)) #c bien ça ?
            doc.preamble.append(Command("date", ""))
            doc.append(NoEscape(r"\maketitle"))

            ## change the description to have:
            # ** XXXX ** => \textbf{XXXX}
            # *XXX* =>\begin{itemize} \item XXX \end{itemize}
            description = process_markdown_to_latex(description)

            doc.append(NoEscape(description))

            try:
                doc.generate_pdf(out_directory + "/" + filename, clean_tex=True)
            except:
                print(description)
                nb_of_failed+=1

                # Clean up auxiliary files generated by pdflatex #also clean up the .tex file
                for ext in [".aux", ".log", ".out", ".tex"]:
                    aux_file = os.path.join(out_directory, f"{filename}{ext}")
                    if os.path.exists(aux_file):
                        os.remove(aux_file)


    return nb_of_failed
    print(f"Number of jobdesc that failed to generate (LaTeX error): {nb_of_failed}")        




if __name__ == "__main__":

    # Generate all job descriptions
    nb_of_failed=0
    for jobdesc_type in ['software_engineer', 'IT_Officer', 'Teacher', 'Doctor', 'Nurse', 'Paralegal', 'Administrative_Assistant']:
        csv_file = jobdesc_type + ".csv"

        output_pdf = jobdesc_type + "_job_descriptions"

        nb_of_failed += jobdesc_to_pdf(csv_file, jobdesc_type, "data")

    print(nb_of_failed)