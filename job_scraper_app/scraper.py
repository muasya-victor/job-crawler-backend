import random
import time
import requests
from bs4 import BeautifulSoup
from requests.exceptions import HTTPError, ConnectionError
from job_scraper_app.models import Job  # Import your Job model from models.py

def linkedin_scraper(webpage_url, position, start, limit, keywords='', location='', trk='', page_number=0):
    """Scrapes job listings from LinkedIn based on provided parameters."""

    # Ensure webpage_url has a valid starting URL
    if not webpage_url:
        raise ValueError("webpage_url cannot be None")

    # Construct the next page URL
    next_page = f"{webpage_url}"
    print(f"Scraping page: {next_page}")

    # List of user-agents for header randomization
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    ]

    try:
        # Set headers with a random user-agent
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(next_page, headers=headers)
        response.raise_for_status()  # Raise an exception for non-200 status codes
    except HTTPError as err:
        if err.response.status_code == 429:
            print(f"Rate limit encountered. Sleeping for 60 seconds and retrying...")
            time.sleep(60)  # Adjust delay as needed based on observations
            return linkedin_scraper(webpage_url, position, start, limit, keywords, location, trk, page_number)
        else:
            print(f"Error fetching page: {err}")
            return
    except ConnectionError as err:
        print(f"Connection error: {err}. Retrying...")
        return linkedin_scraper(webpage_url, position, start, limit, keywords, location, trk, page_number)

    # Process the response
    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    # Scraping logic from the fetch_jobs function
    all_jobs_on_this_page = soup.find_all("li")
    for job_item in all_jobs_on_this_page:
        job_details = {}

        # create job_id
        job_id = job_item.find("div", {"class": "base-card"}).get('data-entity-urn').split(":")[3]
        job_details['job_id'] = job_id

        job_url = f'https://www.linkedin.com/jobs-guest/jobs/api/jobPosting/{job_id}'
        resp = requests.get(job_url)
        job_soup = BeautifulSoup(resp.text, 'html.parser')

        # create company_name
        company_name_elem = job_soup.find_all("div", {"class": "top-card-layout__card"})
        if company_name_elem:
            company_name = company_name_elem[0].find("a").find("img").get('alt')
            job_details['job_company_name'] = company_name
        else:
            job_details['job_company_name'] = None

        # Job Description (Targeted Selector Approach)
        # Job Description (Targeted Selector Approach)
        description_elem = job_soup.find("div", {"class": "description__text-content"})
        if description_elem:
            try:
                job_description = description_elem.text.strip()
                job_details['job_description'] = job_description
            except AttributeError:
                job_details['job_description'] = None
        else:
            job_details['job_description'] = None

        # create job_title
        job_title_elem = job_soup.find_all("div", {"class": "top-card-layout__entity-info"})
        if job_title_elem:
            job_title = job_title_elem[0].find("a").text.strip()
            job_details['job_title'] = job_title
        else:
            job_details['job_title'] = None

        # create job_level
        level_elem = job_soup.find_all("ul", {"class": "description__job-criteria-list"})
        if level_elem:
            level_li_elems = level_elem[0].find_all("li")
            for li_elem in level_li_elems:
                if 'Seniority job_level' in li_elem.text:
                    job_details['job_level'] = li_elem.text.replace("Seniority job_level", "").strip()
                    break
            else:
                job_details['job_level'] = None
        else:
            job_details['job_level'] = None

        jobs.append(job_details)

    # Save jobs to the database
    if jobs:
        print(jobs, 'Jobs')
        complete_jobs = []
        # Create Job instances and save them to the database
        jobs_to_create = []
        for job in jobs:
            if job.get('job_title') and job.get('job_company_name') and job.get('job_id'):
                job_instance = Job(
                    job_title=job.get('job_title'),
                    job_company_name=job.get('job_company_name'),
                    job_level=job.get('job_level'),
                    job_description=job.get('job_description'),
                    job_id=job.get('job_id'),
                )
                jobs_to_create.append(job_instance)
                complete_jobs.append(job)

        # Bulk create Job instances
        Job.objects.bulk_create(jobs_to_create)
        print(f"{len(complete_jobs)} jobs saved to database")
