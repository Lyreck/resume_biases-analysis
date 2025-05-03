import re

## Given a description that looks like this:

# **Job Experience**  - **Senior Software Engineer at Dyson**   - Developed and maintained software solutions for Dyson's innovative products, focusing on embedded systems and IoT technologies.  - Collaborated with cross-functional teams to integrate hardware and software components seamlessly.  - Implemented agile methodologies to ensure timely delivery of high-quality software updates.  -  Conducted thorough testing and debugging to enhance product performance and reliability.  - Contributed to the development of user-friendly interfaces and intuitive control systems for Dyson's smart home devices. 
## Get something that looks like this:
# Title = Senior Software Engineer
# Company = Dyson
# item1 = Developed and maintained software solutions for Dyson's innovative products, focusing on embedded systems and IoT technologies.
# item2 = Collaborated with cross-functional teams to integrate hardware and software components seamlessly.
# item3 = Implemented agile methodologies to ensure timely delivery of high-quality software updates.
# item4 = Conducted thorough testing and debugging to enhance product performance and reliability.
# item5 = Contributed to the development of user-friendly interfaces and intuitive control systems for Dyson's smart home devices.

def process_markdown_job(experience_description):
    # Extract title and company
    experience_description = experience_description[18:] # Remove the first 18 Characters; "**Job Experience**"
    title_company_match = re.search(r"\*\*(.*?)\*\*", experience_description)
    if not title_company_match:
        raise ValueError("Title and company not found in the description")
    title = title_company_match.group(1).strip()

    # Split the content into title and company using " at "
    if " at " not in title:
        raise ValueError("Expected ' at ' separator between title and company")
    
    title, company = title.split(" at ", 1)
    title = title.strip()
    company = company.strip()
    # company = title_company_match.group(2).strip()

    # Extract bullet points
    items = re.findall(r"- (.*?)(?=  -|$)", experience_description)
    items = [item.strip() for item in items]
    # Remove the first item, which is the title and company
    items = items[1:] if len(items) > 1 else []

    return title, company, items


## Now, the same thing for associations:
# **Volunteering Experience at Saint John's Choir**  - Dedicated volunteer at Saint John's Choir, actively participating in weekly rehearsals and performances. -  Contributing to community events, and fostering a collaborative musical environment while honing leadership skills through section management. 
## Get something that looks like this:
# Assocation_name = Saint John's Choir
# item1 = Dedicated volunteer at Saint John's Choir, actively participating in weekly rehearsals and performances.
# item2 = Contributing to community events, and fostering a collaborative musical environment while honing leadership skills through section management.
def process_markdown_association(association):
    # Extract association name
    association_name_match = re.search(r"\*\*(.*?)\*\*", association)
    if not association_name_match:
        raise ValueError("Association name not found in the description")
    association_name = association_name_match.group(1).strip()

    # Extract bullet points
    #items = re.findall(r"- (.*?)(?=  -|$)", association)
    items = re.findall(r"- (.*?)(?=\s*-|$)", association, flags=re.DOTALL)

    items = [item.strip() for item in items]

    return association_name, items


if __name__ == "__main__":

    # Example usage for job experience parsing
    description = """**Job Experience**  - **Senior Software Engineer at Dyson**   - Developed and maintained software solutions for Dyson's innovative products, focusing on embedded systems and IoT technologies.  - Collaborated with cross-functional teams to integrate hardware and software components seamlessly.  - Implemented agile methodologies to ensure timely delivery of high-quality software updates.  -  Conducted thorough testing and debugging to enhance product performance and reliability.  - Contributed to the development of user-friendly interfaces and intuitive control systems for Dyson's smart home devices."""
    title, company, items = process_markdown_job(description)

    print(title)
    print(company)
    print(items)


    # Example usage for association parsing
    # description = """**Volunteering Experience at Saint John's Choir**  - Dedicated volunteer at Saint John's Choir, actively participating in weekly rehearsals and performances. -  Contributing to community events, and fostering a collaborative musical environment while honing leadership skills through section management. """
    association = "**Volunteering Experience at African Impact** - Dedicated over 100 hours to African Impact, a leading volunteer organization in Africa. - Assisted in community development projects, including education and conservation efforts. - Collaborated with local teams to implement sustainable initiatives that positively impacted rural communities. - Facilitated educational workshops for children, enhancing their learning experiences and fostering a love for education. - Participated in environmental conservation activities such as tree planting and beach clean-ups, promoting ecological sustainability. - Engaged with diverse cultural groups, gaining valuable insights into African traditions and lifestyles while contributing to meaningful community projects. "

    association_name, items = process_markdown_association(association)

    print(association_name)
    print(items)