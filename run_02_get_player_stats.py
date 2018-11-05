import logging
from src.data_layer import PlayerData
from src.configuration import season_str
from src.players_stats_grabber import PlayersStatsGrabber
import nba_py.player


def main():
    logging.info("Starting to gather players' stats  for year %s", season_str())
    psg = PlayersStatsGrabber()
    psg.execute(False)
    logging.info("Stats gathered")

if __name__ == '__main__':
    main()
