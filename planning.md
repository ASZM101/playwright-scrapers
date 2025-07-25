# Planning

## Web Scraper Ideas
- 🚧 Job seeker (in progress, fix bugs)
- ⏸️ Screenshotter (on pause, add more unique features)
- ⏸️ Sitemap scanner (on pause, add more unique features)
- ✅ College searcher (MVP done)
- ✅ Scholarship finder (MVP done)

## General Updates
- Take new screenshot with outputs of all scrapers together, upload to #cdn and bay
- Create video combining demos of all scrapers, upload to YouTube and bay
- Enable scrolling in all scrapers
- Implement way to access multiple pages (stops when pages run out or max reached, whichever comes first)
- Allow user to specify what details they want to collect with each scraper (explain options available in readme)
- Update readme with options for all possible URL params for each scraper
- Add comments to explain what each imported library/module is for in each Python file (remove not used)
- Enable scraping programs to search in multiple pages
- Test all scrapers as external user (starting with downloading repo from GitHub)
- ✅ Add table of contents
- ✅ Take screenshot of outputs of all scrapers together (main screenshot)

## Job Seeker
- Update readme with info about job seeker
    - Overall description
    - Technical requirements
    - How to run
- MVP plan
    - Apply parameters provided by user
    - Collect info from each job listing
    - Add info to CSV
- Create YAML template file (separate from personal file)
    - Login credentials (required)
    - URL parameters (default is just example)
- Create experienceable build
    - Record video of job seeker in action
    - Take screenshot of job seeker alone

## College Searcher
- Future plan (two modes)
    - **Find**: Find information on specific colleges based on full name provided by user (more similar to using platform to search for college on platform, but easier to mass-collect info using terminal, **_later_**)
        - Input full name of college into search bar
        - Collect info from each college
        - Add info to CSV
        - Have failsafe in case college name mistyped or not available on platform
    - Mode specified as flag, similar to last24h for job seeker
    - ✅ **Explore**: Find information on colleges that meet criteria provided by user (more similar to scholarships, **_start here_**)
        - ✅ Apply parameters provided by user
        - ✅ Collect info from each college
        - ✅ Add info to CSV
- Create YAML template file (separate from personal file)
    - Full names of colleges (only find, required)
    - ✅ Login credentials (both modes, required)
    - ✅ URL parameters (only explore, required)
- ✅ MVP plan (one mode)
    - ✅ Apply parameters provided by user
    - ✅ Collect info from each college
    - ✅ Add info to CSV
- ✅ Update readme with info about college searcher (need to update once both modes finished)
    - ✅ Overall description
    - ✅ Technical requirements
    - ✅ How to run
- ✅ Create experienceable build
    - ✅ Record video of college searcher in action
    - ✅ Take screenshot of college searcher alone

## Scholarship Finder
- ✅ Update readme with info about scholarship finder
    - ✅ Overall description
    - ✅ Technical requirements
    - ✅ How to run
- ✅ MVP plan
    - ✅ Apply parameters provided by user
    - ✅ Collect info from each scholarship
    - ✅ Add info to CSV
- ✅ Create YAML template file (separate from personal file)
    - ✅ Login credentials (required)
    - ✅ URL parameters (eg=mat and hide=COS as default)
- ✅ Create experienceable build
    - ✅ Record video of scholarship finder in action
    - ✅ Take screenshot of college searcher alone
- ✅ Rename YAML file names and update readme