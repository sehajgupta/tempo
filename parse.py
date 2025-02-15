import requests
from bs4 import BeautifulSoup
import json
from collections import namedtuple

JobDescription = namedtuple("JobDescription", ["title", "description", "date_posted", "employment_type", "job_location_type", "location_requirements"])

def get_html_content(url):
    """Fetches the HTML content of a given URL.

    Args:
        url: The URL to fetch.

    Returns:
        The HTML content as a string, or None if an error occurred.
    """
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None

def extract_job_details(html_content):
    """Extracts job details from the HTML content using JSON-LD data.
    
    Args:
        soup: A BeautifulSoup object representing the parsed HTML.

    Returns:
        A dictionary containing important attributes of this job profile.
    """
    soup = BeautifulSoup(html_content, "html.parser")

    # --- Extract JSON-LD ---
    # Find the script tag with type="application/ld+json"
    json_ld_script = soup.find("script", type="application/ld+json")

    if json_ld_script:
        try:
            job_data = json.loads(json_ld_script.string)  # Parse the JSON data
            job_title = job_data.get('title', 'Job title not found in JSON-LD')
            job_description = job_data.get('description', 'Job description not found in JSON-LD')

             # Extract additional details from JSON-LD (if available)
            date_posted = job_data.get('datePosted', 'Date posted not found')
            hiring_organization = job_data.get('hiringOrganization', {})
            employment_type = job_data.get('employmentType', 'Employment type not found')
            job_location = job_data.get('jobLocation', 'Job location not found')
            job_location_type = job_data.get('jobLocationType', 'Job location type not found')

             # Get applicant location requirements, handling potential variations
            applicant_location_requirements = job_data.get('applicantLocationRequirements', {})

            return {
                'title': job_title,
                'description': job_description,
                'hire_organization': hiring_organization,
                'date_posted': date_posted,
                'employment_type': employment_type,
                'job_location': job_location,
                'job_location_type': job_location_type,
                'application_location_requirements': applicant_location_requirements
            }


        except json.JSONDecodeError as e:
            print(f"Error decoding JSON-LD: {e}")
            return None
    else:
        print("JSON-LD script tag not found.")
        return None


if __name__ == "__main__":
    url = "https://jobs.ashbyhq.com/cohere/dc7da5f5-a571-42c3-80e8-b2c5ffbf3e8a"
    html_content = get_html_content(url)

    if html_content:
        job_details = extract_job_details(html_content)

        if job_details:
            print(job_details)
            # print(f"Job Title: {job_details['title']}")
            # print(f"Date Posted: {job_details['date_posted']}")
            # print(f"Employment Type: {job_details['employment_type']}")
            # print(f"Job Location Type: {job_details['job_location_type']}")
            # print(f"Location Requirements: {job_details['location_requirements']}")
            # print("-" * 20)
            # print(f"Job Description:\n{job_details['description']}")
        else:
            print("Failed to extract job details.")
    else:
        print("Failed to retrieve HTML content.")
