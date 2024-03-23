import requests
from bs4 import BeautifulSoup
import time
import random
from requests.exceptions import HTTPError, ConnectionError

class Job:
    def __init__(self, title, company, location, link):
        self.title = title
        self.company = company
        self.location = location
        self.link = link

def linkedin_scraper(webpage_url, position, start, limit, keywords='', location='', trk='', page_number=0):
    """Scrapes job listings from LinkedIn based on provided parameters."""
    if not webpage_url:
        raise ValueError("webpage_url cannot be None")

    next_page = f"{webpage_url}?keywords={keywords}&location={location}&start={start}&trk={trk}&position={position}&pageNum={page_number}&limit={limit}"
    print(f"Scraping page: {next_page}")

    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        # Add more user-agents here
    ]

    try:
        headers = {'User-Agent': random.choice(user_agents)}
        response = requests.get(next_page, headers=headers)
        response.raise_for_status()
    except HTTPError as err:
        if err.response.status_code == 429:
            print(f"Rate limit encountered. Sleeping for 60 seconds and retrying...")
            time.sleep(60)
            return linkedin_scraper(webpage_url, position, start, limit, keywords, location, trk, page_number)
        else:
            print(f"Error fetching page: {err}")
            return
    except ConnectionError as err:
        print(f"Connection error: {err}. Retrying...")
        return linkedin_scraper(webpage_url, position, start, limit, keywords, location, trk, page_number)

    soup = BeautifulSoup(response.content, 'html.parser')
    jobs = []

    job_elements = soup.find_all('div', class_='job-search-card__card-list--element')
    for job_elem in job_elements:
        try:
            title_elem = job_elem.find('h3', class_='base-card__title')
            company_elem = job_elem.find('h4', class_='job-search-card__subtitle')
            location_elem = job_elem.find('span', class_='job-search-card__location')
            link_elem = job_elem.find('a', class_='base-card__full-link')

            if all([title_elem, company_elem, location_elem, link_elem]):
                title = title_elem.text.strip()
                company = company_elem.text.strip()
                location = location_elem.text.strip()
                link = link_elem['href']

                job_data = Job(title, company, location, link)
                jobs.append(job_data)
            else:
                print(f"Error parsing job details: Skipping current entry.")

        except AttributeError:
            pass

    return jobs

# Example usage:
jobs = linkedin_scraper("https://www.linkedin.com/jobs-guest/jobs/api/seeMoreJobPostings/search", position=1, start=0, limit=5, keywords="Python", location="Nairobi", trk="")
for job in jobs:
    print(vars(job))
