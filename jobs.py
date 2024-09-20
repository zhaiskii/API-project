import aiohttp
from bs4 import BeautifulSoup
import logging
from db import conn

# Function to clean and format text
def clean_text(text: str) -> str:
    return text.strip()

# Async function to fetch job listings
async def fetch_job_listing(session, url):
    try:
        async with session.get(url) as response:
            return await response.text()
    except Exception as e:
        logging.error(f"Error fetching job listing: {e}")
        return None

# Parse and save jobs into the database
async def parse_jobs(html_text: str):
    soup = BeautifulSoup(html_text, 'lxml')
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    for job in jobs:
        job_name = clean_text(job.find('a').text)
        skills = clean_text(job.find('span', class_="srp-skills").text)
        post_date = job.find('span', class_="sim-posted").span.text.strip()

        # Filter only "Posted today" jobs
        if "Posted today" not in post_date:
            continue

        link = job.find('header', class_="clearfix").h2.a['href']
        # Insert job into database
        conn.execute('INSERT INTO jobs (title, skills, date_posted, link) VALUES (?, ?, ?, ?)', 
                     (job_name, skills, post_date, link))
        conn.commit()
