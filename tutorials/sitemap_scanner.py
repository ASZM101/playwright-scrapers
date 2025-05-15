# Scans sitemap of website and prepares CSV file with all found links; WIP (csv created is blank)

import requests
from bs4 import BeautifulSoup as Soup
import os
import csv

ATTRS = ["loc", "lastmod", "priority"] # Constants for attributes to be extracted from sitemap

def parse_sitemap(url, csv_filename="urls.csv"):
    """Parse the sitemap at the given URL and append the data to a CSV file."""

    if not url: # If URL is not provided
        return False
    
    response = requests.get(url) # Attempt to get content from URL

    if response.status_code != 200: # If response status is not 200 (ok)
        return False
    
    soup = Soup(response.content, "lxml") # Parse XML content of response; originally used xml, switched to lxml to resolve bs4.exceptions.FeatureNotFound error

    for sitemap in soup.find_all("sitemap"): # Recursively parse nested sitemaps
        loc = sitemap.find("loc").text
        parse_sitemap(loc, csv_filename)
    
    root = os.path.dirname(os.path.abspath(__file__)) # Define root dir for saving CSV file

    urls = soup.find_all("url") # Find all URL entries in sitemap

    rows = []
    for url in urls:
        row = []
        for attr in ATTRS:
            found_attr = url.find(attr)
            row.append(found_attr.text if found_attr else "n/a") # Use n/a if attribute not found, otherwise get its text
        rows.append(row)
    
    file_exists = os.path.isfile(os.path.join(root, csv_filename)) # Check if file already exists

    with open(os.path.join(root, csv_filename), "a+", newline="") as csvfile: # Append data to CSV file
        writer = csv.writer(csvfile)
        if not file_exists: # Write header only if file doesn't exist
            writer.writerow(ATTRS)
        writer.writerows(rows)

parse_sitemap("") # Insert URL