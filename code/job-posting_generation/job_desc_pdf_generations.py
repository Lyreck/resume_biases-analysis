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

def jobdesc_to_pdf(csv_file, out_directory):

    df = pd.read_csv(csv_file)

    # Ensure the output directory exists
    os.makedirs(out_directory, exist_ok=True)

    for index, row in df.iterrows(): #for each job description
        doc = Document("basic")

        jobtitle = row["title"]
        company = row["company"]
        description = row["description"]
        filename = "".join( (jobtitle+company).split())

        if not isinstance(jobtitle, str) or not isinstance(company,str):
            print(jobtitle,company)

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




if __name__ == "__main__":

    # Generate all job descriptions
    for jobdesc_type in ['software_engineer', 'IT_Officer', 'Teacher', 'Doctor', 'Nurse', 'Paralegal', 'Administrative_Assistant']:
        csv_file = jobdesc_type + ".csv"

        output_pdf = jobdesc_type + "_job_descriptions"

        jobdesc_to_pdf(csv_file, "data")