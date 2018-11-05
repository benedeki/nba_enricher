import tweepy
from src.configuration import *
from src.data_layer import PlayerData
from src.enriching import players_to_enriching, player_full_name
from src.twitter_grabber import TwitterGrabber


def main():
    logging.info("Starting monitor for tweets...")
    # get players
    db = PlayerData()
    top_players = db.get_best_players(TOP_CRITERIA, SEASON, TOP_PLAYER_COUNT)
    # enriching
    enriching = players_to_enriching(top_players)
    logging.debug('Enriching: %s', enriching)
    scanned_players = []
    for player in top_players:
        scanned_players.append(player_full_name(player))
    logging.info('Scanning for players: %s', scanned_players)
    # twitter connection
    auth = tweepy.OAuthHandler(TWITTER_CONNECTION['consumer_key'], TWITTER_CONNECTION['consumer_secret'])
    auth.set_access_token(TWITTER_CONNECTION['access_token'], TWITTER_CONNECTION['access_token_secret'])
    api = tweepy.API(auth)
    stream = TwitterGrabber(api, ENRICHER_WORKER_COUNT, enriching)
    # ---listener = TwitterGrabber(ENRICHER_WORKER_COUNT, enriching)
    # ---stream = tweepy.Stream(auth=api.auth, listener=listener, tweet_mode='extended')
    if TWITTER_CHANNELS:
        track = None # Scan the channels and use internal search only
    else:
        track = list(enriching.keys())
    logging.debug('Tracking: %s', track)
    stream.filter(track=track, follow=TWITTER_CHANNELS)
    logging.info("... monitor shut down.")


if __name__ == '__main__':
    main()
