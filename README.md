# NBA Analysis

This GitHub repo contains code for the final project submission for USF MSAN's Natural Language Processing summer elective.

**Problem Statement:**

This project looks to understand how the media reports on the NBA season. We want to examine how both teams and individuals players are reported - both in terms of the number of mentions they receive and the associated sentiment with this mention.

The core aims of this project are to visualise this data for human exploration and to fit models that allow us to assess feature importance - which factors are most important to be represented in the media?

**Environment:**

An adapted version of [Brian Spiering's Environment](https://github.com/brianspiering/nlp-course/tree/master/resources) is providing for your use - this should contain all packages in the Python 3.6 environment required to run the code.

**Repo Structure:**
- `NBA Media Analysis - Alex Howard.ipynb` -- final project report
- `/Notebooks/` -- experimental notebooks, referenced at length in report
- `/nyt_scrape/` -- code to scrape articles from New York Times and raw `.txt` files for articles
- `/espn_scrape/` -- code to scrape from ESPN (although server currently down, maybe it will be up in future!)
- `/player_stats/` -- various player and team stats referenced through the repo. In particular, it contains season schedules scraped from Basektball Reference and 2017-18 regular season player stats scraped from ESPN.

### Data:

All of the applicable data for this project was scraped from online sources.

**Media articles:  **
  
- ESPN: fully functioning code is available in the `/espn_scrape/` directory of this project to scrape ESPN's NBA articles. Unfortunately the ESPN server for this portion of the website is currently down, so we are unable to use these results.  
  
  
- New York Times: the text corpus of our dataset comprises every article in the NBA section of the New York Times website. The `/nyt_scrape/` directory contains all of the source code used to scrape this, including `nyt_scrape.py` which scrapes a list of article urls and `parse_article.py` which parses the raw HTML and saves the data as a .txt file. These files are also available in the `/nyt_scrape/articles/` directory.
  
  
  
  
**NBA Stats:  **
  
All scraped stats data is listed in `/player_stats/` directory.  
  
  
- BasketBall Reference: the 2017-18 schedule for each team can be scraped and processed using `! python team_results_scrape.py GSW` where 'GSW' is the appropriate team acronym. This code can actually be run by the user from the Jupyter console and the output csvs saved in the stats directory.  
  
  
- ESPN: individual player statistics were scraped using `espn_player_scrape.py` and the output is stored in `player_stats.csv`
  
  
- `team_names.csv` contains only an index of teams

Note: the scope of this project only covers the reporting of teams within the media, this repo contains the full data to do the equivalent analysis for players though (requiring identical code), we leave this as an exercise to the reader ;-)

