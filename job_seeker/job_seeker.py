# Finds jobs on LinkedIn (job database) using provided credentials and parameters/filters

import yaml
from urllib.parse import urlencode, urljoin, quote
from playwright.sync_api import sync_playwright
from scrapy import Selector
from dataclasses import dataclass
import pandas as pd
import logging
import re
from rich.logging import RichHandler
import click
import sys

# logging module is for better log outputs; rich library enhances logging with additional formatting (ex. colors)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
rich_handler = RichHandler(rich_tracebacks=True)
logging.getLogger().handlers = [rich_handler]

# dataclass (decorator from dataclasses module, automatically generates special methods) stores info about each job listing
@dataclass
class Job:
    job_title: str
    company_name: str
    job_location: str
    job_id: int
    url: str

PAGE_NUMBER = 1 # Global var keeps track of current pg num while scraping job listings

def login(page, email, password, headless): # Log in to LinkedIn using provided credentials (need to set up jobs_config.yaml first)
    page.goto("https://www.linkedin.com/login") # Go to LinkedIn login page
    page.wait_for_load_state("load")

    # Fill in login credentials
    page.get_by_label("Email or phone").click()
    page.get_by_label("Email or phone").fill(email)
    page.get_by_label("Password").click()
    page.get_by_label("Password").fill(password)

    page.locator("#organic-div form").get_by_role("button", name="Sign in").click() # Click login btn
    page.wait_for_timeout(3000) # Wait for 3 sec to ensure page loads
    page.wait_for_load_state("load")

    if "checkpoint/challenge" in page.url and not headless: # Detects if CAPTCHA page encountered
        logger.warning("CAPTCHA page: Human intervention is required")
        while True: # Polling loop to check if CAPTCHA is solved
            if "checkpoint/challenge" not in page.url:
                logger.info("CAPTCHA solved. Continuing with the rest of the job scraping process...")
                break
            page.wait_for_timeout(2000) # Wait 2 sec before polling again
        page.wait_for_timeout(5000) # Wait 5 sec after CAPTCHA solved
    else:
        logger.error("CATPCHA page: Aborting due to headless mode...")
        sys.exit(1)

def scrape_jobs(max, page, params, last24h): # Scrape job listings based on provided search parameters (include in jobs_config.yaml)
    global PAGE_NUMBER
    base_url = "https://www.linkedin.com/jobs/search/"
    # url = f"{base_url}?{urlencode(params)}" Still need to uncomment this

    job_list = [] # List for storing job data

    page.goto(base_url) # Go to search results page, still need to replace arg with url
    page.wait_for_load_state("load")
    page.wait_for_timeout(3000) # Wait for 3 sec to ensure page loads
    if last24h: # Apply "last 24 hours" filter if requested
        page.get_by_role("button", name="Show all filters. Clicking this button displays all available filter options.").click()
        page.locator('label[for="advanced-filter-timePostedRange-r86400"]').filter(has_text="Past 24 hours").click()
        page.locator('button[data-test-reusables-filters-modal-show-results-button="true"]').click()
        page.wait_for_timeout(3000) # Wait for 3 sec to ensure page loads
    
    results = page.locator("li.ember-view.AwLoWPpuChmYRACOainfIeJFpSNEnXzKuVjsg.occludable-update.p0.relative.scaffold-layout__list-item")
    for i in range(results.count()): # Loop through job listings
        listing = results.nth(i)
        listing.locator("a").click() # More for visual effect when in no-headless mode; could be useful for collecting more info in future
        selector = Selector(text=listing.inner_html())

        info = Job(
            job_title = selector.css("div.artdeco-entity-lockup__title strong ::text").get() if selector.css("div.artdeco-entity-lockup__title strong ::text").get() else None,

            company_name = listing.locator("div.artdeco-entity-lockup__subtitle span").inner_text() if listing.locator("div.artdeco-entity-lockup__subtitle span").inner_text() else None,

            job_location = listing.locator("div.artdeco-entity-lockup__caption span").inner_text() if listing.locator("div.artdeco-entity-lockup__caption span").inner_text() else None,

            job_id = selector.css("div.job-card-container--clickable ::attr(data-job-id)").get() if selector.css("div.job-card-container--clickable ::attr(data-job-id)").get() else None,

            url = "https://www.linkedin.com/jobs/view/" + selector.css("div.job-card-container--clickable ::attr(data-job-id)").get() if selector.css("div.job-card-container--clickable ::attr(data-job-id)").get() else None
        ) # Scrapes details of each job
        job_list.append(info)
        logger.info(f"Scraped job: {info.job_title} at {info.company_name} in {info.job_location}")

        page.wait_for_timeout(500) # Wait for 0.5 sec to ensure job details load
        page.mouse.wheel(0, 100) # deltaX: horizontal scroll amount (+ = right, - = left); deltaY = vertical scroll amount (+ = down, - = up)
        page.wait_for_timeout(500) # Wait for 0.5 sec to ensure job details load

        if i == max - 1: # Stops scraping once max jobs found
            break
    
    return job_list

# Define CLI to use click for scraping process
@click.command()
@click.option("--max", default=5, help="Specify a maximum number of jobs to scrape")
@click.option("--config", type=click.Path(exists=True), default="jobs_config.yaml", help="Path to the YAML config file")
@click.option("--headless/--no-headless", default=True, help="Run the browser in headless mode or not")
@click.option("--last24h", is_flag=True, default=False, help="Make the browser scrape for last 24h jobs only")

def main(max, config, headless, last24h):
    with open(config, "r") as f: # Load YAML file with list of search params
        data = yaml.safe_load(f)

    email = data.get("email")
    password = data.get("password")
    params_list = data.get("params")
    
    with sync_playwright() as p: # Start browser
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()

        login(page, email, password, headless) # Login to LinkedIn

        # Still need to uncomment this, just testing login
        all_jobs = []
        # for params in params_list:
        #     logger.info(f"Crawl starting... Params: {params}")
        #     jobs = scrape_jobs(max, page, params, last24h)
        #     all_jobs.extend(jobs)

        # Still need to remove this, just for testing
        logger.info(f"Initiating search...") # Still need to add params
        jobs = scrape_jobs(max, page, params_list, last24h) # Still need to replace params_list with params
        all_jobs.extend(jobs)
        
        df = pd.DataFrame([job.__dict__ for job in all_jobs]) # Create DataFrame from combined job_list

        csv_file_path = 'jobs_data.csv'
        df.to_csv(csv_file_path, index=False) # Save DataFrame to CSV file

        logger.info(f"Scraped {len(all_jobs)} jobs and saved to jobs_data.csv") # Log the number of jobs scraped and saved

        browser.close()

if __name__ == '__main__':
    main()