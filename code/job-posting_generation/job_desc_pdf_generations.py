import pandas as pd

from pylatex import Document, Section, Itemize, Command
from pylatex.utils import NoEscape

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

def to_pdf(csv):
    pass

# Example usage
csv_file = "Doctor.csv"  # Replace with your CSV file path
output_pdf = "job_descriptions"  # Output PDF file name (without extension)
generate_pdf_from_dataframe(csv_file, output_pdf)