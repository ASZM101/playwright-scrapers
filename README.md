# Playwright Scrapers

<div align="center">
   <p>A collection of open-source web scraping programs created with the Playwright library on Python</p>
    <a href="https://shipwrecked.hackclub.com/?r=163" target="_blank">
        <img src="https://hc-cdn.hel1.your-objectstorage.com/s/v3/739361f1d440b17fc9e2f74e49fc185d86cbec14_badge.png" alt="This project is part of Shipwrecked, the world's first hackathon on an island!" style="width: 35%;">
    </a>
    <br><br>
    <img src="https://hackatime-badge.hackclub.com/U07DMCJTB8Q/playwright-scrapers" alt="Hackatime Badge">
</div>

### Table of Contents

- [College Searcher](https://github.com/aszm101/playwright-scrapers?tab=readme-ov-file#college-searcher)

- [Job Seeker](https://github.com/aszm101/playwright-scrapers?tab=readme-ov-file#job-seeker)

- [Scholarship Finder](https://github.com/aszm101/playwright-scrapers?tab=readme-ov-file#scholarship-finder)

<details>
    <summary><h2 style="display: inline;">College Searcher</h2></summary><br>
    <p>Explore <b>colleges</b> on <a href="https://goingmerry.com">Going Merry</a> (a free platform with an extensive database of scholarships and colleges) by using the <code>college_searcher.py</code> script to:</p>
    <ol>
        <li>Log in to your account on Going Merry</li><br>
        <li>Apply search parameters to filter the results</li><br>
        <li>Scrape college details, storing the data in a CSV file</li>
    </ol>
</details>

## College Searcher

Explore **colleges** on [Going Merry](https://goingmerry.com) (a free platform with an extensive database of scholarships and colleges) by using the `college_searcher.py` script to:

1. Log in to your account on Going Merry

2. Apply search parameters to filter the results

3. Scrape college details, storing the data in a CSV file

### Technical Requirements

Before running this program, ensure you have the following installed:

- Python 3.x

-  `playwright-sync` library

- `scrapy` library

- `pandas` library

- `rich` library

- `click` library

### How to Run

1. Clone this repository, and open it in your favorite IDE

2. Open the `colleges_config.yaml` file in the `college_searcher` directory, and prepare this configuration file with your [Going Merry](https://goingmerry.com) login credentials and desired search parameters using the following template:

    ```yaml
    email: GOING_MERRY_EMAIL
    password: GOING_MERRY_PASSWORD
    params:
        - gmMajorName: All majors
          orderColumn: value
          orderType: desc
    ```

    _**Note**: Replace `GOING_MERRY_EMAIL` and `GOING_MERRY_PASSWORD` with your login credentials._

    **Parameters Explained**:

    - `gmMajorName: All majors` displays all colleges that offer any major. You can replace `All majors` with one of the majors listed on Going Merry's [Explore Colleges](https://app.goingmerry.com/colleges) page to filter your results by your desired major

    - `orderColumn: value` orders the results by Going Merry's value score, which is further explained on their website in the [Explore Colleges](https://app.goingmerry.com/colleges) page

    - `orderType: desc` sorts the results in descending order

    You may include as many of these parameters for each entry as desired, but always make sure to include at least one entry with at least one parameter, and be careful with the indentation. The above parameters are intended to set up the least restrictive filters, serving as a guideline for a broad search.

3. Navigate to the cloned repository, and open a terminal or command prompt inside the `college_searcher` folder

4. Run the `college_searcher.py` script with the following command:

    ```bash
    python3 college_searcher.py
    ```

    By default, the maximum colleges scraped is 5, the configuration file path is `colleges_config.yaml`, and the program runs in headless mode.

    If you want to specify the maximum number of colleges to scrape, the path to the YAML configuration file, and/or whether the program runs in headless mode, run the following command:

    ```bash
    python3 college_searcher.py --max MAX_COLLEGES --config PATH/TO/CUSTOM_CONFIG.yaml --headless/--no-headless
    ```

    _**Note**: Replace `MAX_COLLEGES` and `PATH/TO/CUSTOM_CONFIG.yaml`, and choose either `--headless` or `no-headless`._

5. Wait for the script to finish running, and open the `colleges_data.csv` file to review all of the scraped colleges

    **Troubleshooting**:

    Depending on your internet speed and personal preference, you may need to adjust the argument in the `page.wait_for_timeout(milliseconds)` functions used throughout the script. The number in between the parentheses is the time (in milliseconds) that the program will wait before proceeding with the rest of the script.

    - If you experience issues with the script quitting before the page finishes loading, you may want to increase this time

    - If the automated process feels too slow, you may want to slightly decrease this time, but keep in mind that you may encounter issues if the timeouts are too short

## Job Seeker

Discover **jobs** on [LinkedIn](https://www.linkedin.com) (a platform with an extensive database of job listings) by using the `job_seeker.py` script to:

1. Log in to your account on LinkedIn

2. Apply search parameters to filter the results

3. Scrape job details, storing the data in a CSV file

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

2. Open the `jobs_config.yaml` file in the `job_seeker` directory, and prepare this configuration file with your [LinkedIn](https://www.linkedin.com) login credentials and desired search parameters using the following template:
    
    ```yaml
    email: LINKEDIN_EMAIL
    password: LINKEDIN_PASSWORD
    params:
      - keywords: KEYWORD_1 KEYWORD_2
        location: CITY_NAME
        currentJobId: JOB_ID
        geoId: GEO_ID
      - keywords: KEYWORD_3
        location: CITY_NAME
        currentJobId: JOB_ID
        geoId: GEO_ID
    ```

    _**Note**: Replace `LINKEDIN_EMAIL` and `LINKEDIN_PASSWORD` with your login credentials._

    **Parameters Explained**:

    - `keywords` allow you to specify any keywords you want to use to filter your results. You can put spaces in between words, similarly to using the search bar to look for jobs on LinkedIn

    - `location` allows you to narrow your search to a certain city

    - `currentJobId` is for when you are looking for a specific job and you already have its job ID, which is a 10-digit number that can be found in the URL of a job description

    - `geoId` is for when you are looking for a specific geographic location and you already have its geo ID, which is a 9-digit number that can be found in the URL of a job search when you use the search bar that is specifically for locations

    You may include as many of these parameters for each entry as desired, but always make sure to include at least one entry with at least one parameter, and be careful with the indentation.

3. Navigate to the cloned repository, and open a terminal or command prompt inside the `job_seeker` folder

4. Run the `job_seeker.py` script with the following command:

    ```bash
    python3 job_seeker.py
    ```

    By default, the maximum jobs scraped is 5, the configuration file path is `jobs_config.yaml`, the program runs in headless mode, and no additional filters are applied outside of the configuration file.

    If you want to specify the maximum number of jobs to scrape, the path to the YAML configuration file, whether the program runs in headless mode, and/or whether the results should be filtered to only include job listings posted in the last 24 hours, run the following command:

    ```bash
    python3 job_seeker.py --max MAX_JOBS --config PATH/TO/CUSTOM_CONFIG.yaml --headless/--no-headless --last24h
    ```

    _**Note**: Replace `MAX_JOBS` and `PATH/TO/CUSTOM_CONFIG.yaml`, choose either `--headless` or `--no-headless`, and only include the `--last24h` flag if you want to filter your results._

5. Wait for the script to finish running, and open the `jobs_data.csv` file to review all of the scraped jobs

    **Troubleshooting**:

    Depending on your internet speed and personal preference, you may need to adjust the argument in the `page.wait_for_timeout(milliseconds)` functions used throughout the script. The number in between the parentheses is the time (in milliseconds) that the program will wait before proceeding with the rest of the script.

    - If you experience issues with the script quitting before the page finishes loading, you may want to increase this time

    - If the automated process feels too slow, you may want to slightly decrease this time, but keep in mind that you may encounter issues if the timeouts are too short

## Scholarship Finder

Find **high-match scholarships** on [Going Merry](https://goingmerry.com) (a free platform with an extensive database of scholarships and colleges) by using the `scholarship_finder.py` script to:

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

2. Open the `scholarships_config.yaml` file in the `scholarship_finder` directory, and prepare this configuration file with your [Going Merry](https://goingmerry.com) login credentials and desired search parameters using the following template:

    ```yaml
    email: GOING_MERRY_EMAIL
    password: GOING_MERRY_PASSWORD
    params:
        - eg: mat
          hide: COS
    ```

    _**Note**: Replace `GOING_MERRY_EMAIL` and `GOING_MERRY_PASSWORD` with your login credentials._

    **Parameters Explained**:

    - `eg: mat` filters scholarships by only showing the ones where you have a high match for eligibility, based on your profile

    - `hide: COS` hides scholarships that are specific to certain colleges.

    You may include as many of these parameters for each entry as desired, but always make sure to include at least one entry with at least one parameter, and be careful with the indentation.

3. Navigate to the cloned repository, and open a terminal or command prompt inside the `scholarship_finder` folder

4. Run the `scholarship_finder.py` script with the following command:

   ```bash
   python3 scholarship_finder.py
   ```

   By default, the maximum scholarships scraped is 5, the configuration file path is `scholarships_config.yaml`, and the program runs in headless mode.
   
   If you want to specify the maximum number of scholarships to scrape, the path to the YAML configuration file, and/or whether the program runs in headless mode, run the following command:

   ```bash
   python3 scholarship_finder.py --max MAX_SCHOLARSHIPS --config PATH/TO/CUSTOM_CONFIG.yaml --headless/--no-headless
   ```

   _**Note**: Replace `MAX_SCHOLARSHIPS` and `PATH/TO/CUSTOM_CONFIG.yaml`, and choose either `--headless` or `--no-headless`._

5. Wait for the script to finish running, and open the `scholarships_data.csv` file to review all of the scraped scholarships

    **Troubleshooting**:

    Depending on your internet speed and personal preference, you may need to adjust the argument in the `page.wait_for_timeout(milliseconds)` functions used throughout the script. The number in between the parentheses is the time (in milliseconds) that the program will wait before proceeding with the rest of the script.

    - If you experience issues with the script quitting before the page finishes loading, you may want to increase this time

    - If the automated process feels too slow, you may want to slightly decrease this time, but keep in mind that you may encounter issues if the timeouts are too short