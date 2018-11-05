import logging

logging.basicConfig(format='[%(asctime)s - %(name)s] - %(levelname)s: %(message)s', level=logging.INFO)

DB_CONNECTION = {
    "database": "nbadb",
    "user": "nba",
    "password": "nba",
    "host": "localhost",
    "port": "5432"
}

TWITTER_CONNECTION = {
    'consumer_key': '????',
    'consumer_secret': '????',
    'access_token': '????',
    'access_token_secret': '????'
}

PLAYERS_STATS_WORKER_COUNT = 10
ENRICHER_WORKER_COUNT = 4

SEASON = 2018 # the season to work with (starting year)
def season_str():
    # returns the proper sting representation for the season (e.g. 2017-18)
    return ("%d-%d" % (SEASON, SEASON - 1999))

TOP_CRITERIA = 3 # BEST_PLAYERS_CRITERIA_SCORE_PER_MATCH
#TOP_CRITERIA = 100 #RANDOM (allows to scan for some players even without any stats)
TOP_PLAYER_COUNT = 10

TWITTER_CHANNELS = [
    '19923144',   # @NBA
    '1373313666', # @NBAcom
] # If None there will be no filtering on channels
