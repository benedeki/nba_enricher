import logging
from src.data_layer import PlayerData
from src.configuration import season_str
from nba_py.player import PlayerList


def main():
    logging.info("Starting to gather players for year %s", season_str())
    db = PlayerData()
    logging.debug("Connected to DB")
    pl = PlayerList()
    info = pl.info()
    pl_len = len(info)
    logging.info("%d players to process" % pl_len)
    index = 0
    for player in info:
        logging.debug("Processing player %s", player)
        db.add_player_from_dict(player)
        index += 1
        logging.info("Done %d/%d", index, pl_len)
    logging.info("All players gathered")

if __name__ == '__main__':
    main()
