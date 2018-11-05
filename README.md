# NBA Enricher
**version 1.0 RC**

A small (mostly) Python project to gather NBA related statistics, find the best player 9based on chosen criteria) and 
eventually scan Twitter for mentions of these players. Then the tweets are enriched with additional info about the players. 

## Required packages and other requirements
Postgres DB server (tested with 9.5, should work with 9+)

Twitter developer account to be able to use Twitter API

Python (tested with 3.6, effort made to make it 2.7 compatible)

### Python Packages
* requests
* tweepy
* psycopg2


## Configuration
1. Install or choose Postgres Server
1. Create or choose existing database (let's call it **_nbadb_**)
1. Create user **_nba_** on the server and add him CONNECT and CREATE privileges to the database from step #2 (_nbadb_)
1. run script **_deploy.sh_** from the _DB_ directory (_deploy.sh --host=localhost --dbname=nbadb --username=nba --password=???_); on Windows WSL can be used
1. Change DB_CONNECTION in **_src/configuration.py_** to reflect the database set up
1. Add Twitter API keys and secrets into TWITTER_CONNECTION in **_src/configuration.py_**
1. Change any other configuration in **_src/configuration.py_** according to your privileges 
 
## Run
### Logical steps
1. Get players
1. Get players' stats
1. Identify the top players
1. Gather the tweets
1. Enrich the tweets matching
1. Output the enriched tweets

* Execute **_run_01_get_players.py_** (can be run repeatedly)
* Execute **_run_02_get_player_stats.py_** (can be run repeatedly)
* Start **_run_03_enrich_tweets.py_**

## Tests
* Execute **_runt_tests.py_**

##Highlights
* both statistics gathering and Tweet scanning steps are created as multi-threaded
* the threads communicate via  command queue(s)
* Tweet scanning for multiple different string occurrences is done using Aho-Corasick algorithm, which searches a text wiht one pass, 
replacement is then another, two in total (in case of at least one hit)
* Database part is implemented as a service, not tightly sewn in into the program
* Key parts that can be expected to change or be enhanced are clearly separated to allow easy alternation (statistics gathering,
 best players criteria, enriching rules, output of the enriched tweets, ...) 

## Known issues and TODOs
* Aho Corasick - use smarter result accumulation, so no sorting is needed (use cache of size equal to longest searched word)
* Some stats are back-computed from per game stats, better source would be more prices (points, time player, shots)
* Increased robustness in calling NBA API (retries, thread recreation) 
* More tests
* Components are tight together somewhat closely which complicates testing 
* Deploy script can be much more sophisticated
* Tweets scanning/enriching could be multi-processed instead of multi-threaded
* Add threads to initial players load (step 1)

## ... and Beyond
The _enriching_ part (03) was designed to offer flexibility first in the way of output (method __output_ in class 
**_TweetEnricher_**), the way what are the actual enriching rules (the replacement dictionary coming out of _players_to_enriching_ 
function in _enriching.py_ file) and finally the possibility to relatively easily switch the design to multi-process or even multi-service
design in case the enriching becomes CPU intensive or just for scaling reasons.

Also the database is used as juts another service in the multi-service architecture of this small application, 
together with NBA and Twitter. The Python code communicate with the database via API only, no direct access to the db
(SELECTs, INSERTs etc.). This allows to hide from the application the DB implementation details, actual data structures can morph,
and the database can scale and offer redundancy without any changes to the application. Thanks to this approach the database can also - as 
any other service - also expand it's API to offer richer service, with just some care not to break the past contracts. 