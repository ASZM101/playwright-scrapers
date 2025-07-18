# Playwright Scrapers

<div align="center">
   <p>Open-source web scraping programs created with the Playwright library on Python</p>
    <a href="https://shipwrecked.hackclub.com/?r=163" target="_blank">
        <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" alt="This project is part of Shipwrecked, the world's first hackathon on an island!" style="width: 35%;">
    </a>
    <br><br>
    <img src="https://hackatime-badge.hackclub.com/U07DMCJTB8Q/playwright-scrapers" alt="Hackatime Badge">
</div>

## Scholarship Finder

Find **high-match scholarships** on [Going Merry](https://goingmerry.com/) (a free scholarship site) by using the `scholarship_finder.py` script to:

1. Log in to your account on Going Merry

2. Apply search parameters to filter the results

3. Scrape scholarship details, storing the data in a CSV file

### Technical Requirements

Before running this program, ensure you have the following installed:

- Python 3.x

- `playwright-sync` library

- `scrapy` library

- `pandas` library

- `rich` library

- `click` library

### How to Run

1. Clone this repository, and open it in your favorite IDE

2. Open the `config.yaml` file in the root directory, and prepare this configuration file with your [Going Merry](https://goingmerry.com/) login credentials and desired search parameters using the provided template

3. Open a terminal or command prompt, and navigate to the root directory of the cloned repository

4. Run the `scholarship_finder.py` script with the following command:

   ```
   python3 scholarship_finder.py
   ```

   By default, the maximum scholarships scraped is 5, the configuration file path is `config.yaml`, and the program runs in headless mode.
   
   If you want to specify the maximum number of scholarships to scrape, the path to the YAML configuration file, and/or whether the program runs in headless mode, run the following command:

   ```
   python3 scholarship_finder.py --max MAX_SCHOLARSHIPS --config PATH/TO/CUSTOM_CONFIG.yaml --headless/--no-headless
   ```

   (Replace `MAX_SCHOLARSHIPS` and `PATH/TO/CUSTOM_CONFIG.yaml`, and choose either `--headless` or `--no-headless`)

5. Wait for the script to finish running, and open the `scholarships_data.csv` file to review all of the scraped scholarships