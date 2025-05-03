import pandas as pd

def process_file(input_file, output_file, keywords):
    """
    Processes a file by putting all content on a single line and creating a newline
    every time a keyword from the provided list is detected.

    Args:
        input_file (str): Path to the input file.
        output_file (str): Path to save the processed file.
        keywords (list): List of keywords to split the content on.
    """
    with open(input_file, "r", encoding="utf-8") as infile:
        # Read the entire file content and put it on a single line
        raw_data = infile.read().replace("\n", " ")

    # Create a regex pattern to match any of the keywords
    pattern = r"(" + "|".join(keywords) + r")"

    # Insert a newline before each keyword
    processed_data = raw_data
    for keyword in keywords:
        processed_data = processed_data.replace(f"{keyword},", f"\n{keyword};")

    # Remove all commas
    raw_data = raw_data.replace(",", "")

    # Write the processed data to the output file
    with open(output_file, "w", encoding="utf-8") as outfile:
        outfile.write(processed_data.strip())


if __name__ == "__main__":
    names = pd.read_csv("data/names_clean.csv", 
                    names=["Name", "Surname", "Associations", "Gender", "Tech_comp", "Med_comp", "Edu_comp"])

    associations = names["Associations"].dropna().drop_duplicates().tolist()
    comps_tech = names["Tech_comp"].dropna().drop_duplicates().tolist()#.to_list()
    comps_med = names["Med_comp"].dropna().drop_duplicates().tolist()#.to_list()
    comps_edu = names["Edu_comp"].dropna().drop_duplicates().tolist()#.to_list()

    print(associations + comps_edu + comps_tech + comps_med)
    
    # Example usage
    input_file = "out_files/out2.csv"  # Replace with the path to your input file
    output_file = "out_files/processed.csv"  # Replace with the desired output path
    keywords = associations + comps_edu + comps_tech + comps_med  # Replace with your list of keywords
    process_file(input_file, output_file, keywords)


    df = pd.read_csv(output_file, sep=";", header=None)
    df.columns= ["Experience", "Description"]
    print(df.head())
    df.to_excel("out_files/processed.xlsx", index=False)
