import csv
from jobspy import scrape_jobs

def clean_data(df):
    # Keep only relevant columns : id, site, job_url, title, company, location, job_type, job_level, job_function, description, company_indutry, skills, experience_range 
    df_clean = df[["id", "site", "job_url", "title", "company", "location", "job_type", "job_level", "job_function", "description", "company_industry", "skills", "experience_range"]]
    return df_clean

#list of search terms for job postings for our experience framework 
search_terms_forexp = ['software engineer', 'IT Officer', 'Teacher', 'Doctor', 'Nurse', 'Paralegal', 'Administrative Assistant']
google_search_terms_forexp = ['software engineer', 'IT Officer', 'Teacher', 'Doctor', 'Nurse', 'Paralegal', 'Administrative Assistant']

#function that saves all the job offers to csv files. 
def scraping_offers( search_terms, google_search_terms ,site_name = ["indeed"], location = "London", results_wanted = 10, hours_old = 240, country_indeed = 'UK'):
    for search_term, google_search_term in zip(search_terms, google_search_terms):
        print(f"Scraping {search_term} jobs...")
        jobs = scrape_jobs(
            site_name=site_name,
            search_term=search_term,
            google_search_term=google_search_term,
            location=location,
            results_wanted=results_wanted,
            hours_old=hours_old,
            country_indeed=country_indeed)
        jobs = clean_data(jobs)
        file_name = search_term.replace(" ", "_") + ".csv"
        jobs.to_csv(file_name, quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel
        print(f"Saved {len(jobs)} {search_term} jobs to {file_name}")

scraping_offers(search_terms_forexp, google_search_terms_forexp)


