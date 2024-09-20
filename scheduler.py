import asyncio
import aiohttp
from jobs import fetch_job_listing, parse_jobs
from config import SCRAPE_INTERVAL

# Function to start job scheduler
async def scheduler():
    url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=Home_Search&from=submit&asKey=OFF&txtKeywords=&cboPresFuncArea=35'
    
    async with aiohttp.ClientSession() as session:
        while True:
            html_text = await fetch_job_listing(session, url)
            if html_text:
                await parse_jobs(html_text)
            await asyncio.sleep(SCRAPE_INTERVAL)

def start_scheduler():
    loop = asyncio.get_event_loop()
    loop.create_task(scheduler())
