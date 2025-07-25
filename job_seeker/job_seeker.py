# Finds jobs on LinkedIn using provided credentials and parameters/filters; WIP (only found one of two jobs searched before encountering TimeoutError when changing page, unable to retry due to CAPTCHA in both headless and not headless, still need to remove this once done)

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
    # Still need to figure out why first result details collected twice, job location isn't collected in any of them
    for i in range(results.count()): # Loop through job listings
        listing = results.nth(i)
        listingSelector = Selector(text=listing.inner_html())
        detailSelector = Selector(text=page.locator("div.jobs-search__job-details--wrapper").inner_html())
        listing.locator("a").click()

        info = Job(
            job_title = detailSelector.css("div.t-24.job-details-jobs-unified-top-card__job-title a ::text").get() if detailSelector.css("div.t-24.job-details-jobs-unified-top-card__job-title a ::text").get() else None,

            company_name = detailSelector.css("div.job-details-jobs-unified-top-card__company-name a ::text").get() if detailSelector.css("div.job-details-jobs-unified-top-card__company-name a ::text").get() else None,

            job_location = listingSelector.css("div.artdeco-entity-lockup__caption ember-view span ::text").get() if listingSelector.css("div.artdeco-entity-lockup__caption ember-view span ::text").get() else None,

            job_id = listingSelector.css("div.job-card-container--clickable ::attr(data-job-id)").get() if listingSelector.css("div.job-card-container--clickable ::attr(data-job-id)").get() else None,

            url = "https://www.linkedin.com/jobs/view/" + listingSelector.css("div.job-card-container--clickable ::attr(data-job-id)").get() if listingSelector.css("div.job-card-container--clickable ::attr(data-job-id)").get() else None
        ) # Scrapes details of each job
        job_list.append(info)
        logger.info(f"Scraped job: {info.job_id}") # Still need to replace "{info.job_id}" with "{info.job_title} at {info.company_name}"

        page.wait_for_timeout(2000) # Wait for 2 sec to ensure job details load
        page.mouse.wheel(0, 100) # deltaX: horizontal scroll amount (+ = right, - = left); deltaY = vertical scroll amount (+ = down, - = up)
        page.wait_for_timeout(2000) # Wait for 2 sec to ensure job details load

        if i == max - 1: # Stops scraping once max jobs found
            break
    
    return job_list

    # Still need to uncomment or delete
    # while True:
    #     page.locator("div.jobs-search-results-list").click()
    #     logger.info(f"Found results div")
    #     for _ in range(15): # Loop through job listings (underscore is throwaway var)
    #         page.mouse.wheel(0, 250)
    #     page.wait_for_timeout(10000) # Wait for 10 sec before quitting
    #     response = Selector(text=page.content())
        
    #     jobs = response.css("ul.scaffold-layout__list-container li.ember-view")
    #     for job in jobs: # Scrapes details of each job
    #         job_info = Job(
    #             url=urljoin(main_url, job.css("a::attr(href)").get()) if job.css("a::attr(href)").get() else None,
    #             job_title=job.css("a::attr(aria-label)").get(),
    #             job_id=job.css("::attr(data-occludable-job-id)").get(),
    #             company_name=" ".join(job.css("img ::attr(alt)").get().split(" ")[2::]) if job.css("img ::attr(alt)").get() else None,
    #             company_image=job.css("img ::attr(src)").get(),
    #             job_location=" ".join(job.css(".job-card-container__metadata-item ::text").getall()) if job.css(".job-card-container__metadata-item ::text").get() else None
    #         )
    #         job_list.append(job_info)
    #         logger.info(f"Scraped job: {job_info.job_title}")
        
    #     try: # Check if there is "Next" btn to click it
    #         PAGE_NUMBER += 1
    #         page.get_by_role("button", name=f"Page {PAGE_NUMBER}", exact=True).click(timeout=4000)
    #         page.wait_for_timeout(3000) # Wait 3 sec for next page to load
    #         logger.info(f"Moving to page {PAGE_NUMBER}")
    #     except Exception: # Finished scraping
    #         logger.warning("No more pages to scrape")
    #         break

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

        csv_file_path = 'jobs_data.csv' # Still need to figure out why not collecting all info and links are wrong
        df.to_csv(csv_file_path, index=False) # Save DataFrame to CSV file

        logger.info(f"Scraped {len(all_jobs)} jobs and saved to jobs_data.csv") # Log the number of jobs scraped and saved

        browser.close()

if __name__ == '__main__':
    main()