# Planning

## Web Scraper Ideas
- ⏸️ Screenshotter (on pause, add more unique features)
- ⏸️ Sitemap scanner (on pause, add more unique features)
- ✅ College searcher (MVP done)
- ✅ Job seeker (MVP done)
- ✅ Scholarship finder (MVP done)

## General Updates
- Add dropdowns to readme
- Test all scrapers as external user (starting with downloading repo from GitHub)
- Remove redundant instructions on readme
- Update all screenshots and recordings with any changes
- Enable scrolling in all scrapers
- Implement way to access multiple pages (stops when pages run out or max reached, whichever comes first)
- Allow user to specify what details they want to collect with each scraper (explain options available in readme)
- Update readme with options for all possible URL params for each scraper
- Add comments to explain what each imported library/module is for in each Python file (remove not used)
- Enable scraping programs to search in multiple pages
- ✅ Add table of contents
- ✅ Take new screenshot with outputs of all scrapers together, upload to #cdn and bay
- ✅ Create video combining demos of all scrapers, upload to YouTube and bay
- ✅ Add more logger info updates throughout each process (especially useful for headless mode)
- ✅ Add more details about how to run to each section on readme
- ✅ Ensure comments are consistent in all scrapers
- ✅ Add note to readme about possibly having to adjust timeout times to adapt to different internet speeds and each user's preference (though need to keep in mind that script could fail if timeouts too short)

## College Searcher
- Future plan (add find mode): Find information on specific colleges based on full name provided by user (more similar to using platform to search for college on platform, but easier to mass-collect info using terminal)
    - Input full name of college into search bar
    - Collect info from each college
    - Add info to CSV
    - Have failsafe in case college name mistyped or not available on platform
    - Mode specified as flag, similar to last24h for job seeker
- Create YAML template file (separate from personal file)
    - Full names of colleges (only find, required)
    - ✅ Login credentials (both modes, required)
    - ✅ URL parameters (only explore, required)
- ✅ MVP plan (only explore mode): Find information on colleges that meet criteria provided by user
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

## Job Seeker
- ✅ Update readme with info about job seeker
    - ✅ Overall description
    - ✅ Technical requirements
    - ✅ How to run
- ✅ MVP plan
    - ✅ Apply parameters provided by user
    - ✅ Collect info from each job listing
    - ✅ Add info to CSV
- ✅ Create YAML template file (separate from personal file)
    - ✅ Login credentials (required)
    - ✅ URL parameters (default includes examples of params)
- ✅ Create experienceable build
    - ✅ Record video of job seeker in action
    - ✅ Take screenshot of job seeker alone

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