import logging
import six
from queue import Queue
import nba_py.player

from .thread_on_command_queue import ThreadOnCommandQueue
from .data_layer import PlayerData
from .configuration import PLAYERS_STATS_WORKER_COUNT, SEASON, season_str


class PlayersStatsGrabberThread(ThreadOnCommandQueue):
    def __init__(self, thread_name, thread_id, queue):
        # type: (str, int, Queue) -> None
        ThreadOnCommandQueue.__init__(self, queue, thread_name)
        self. thread_id = thread_id
        self.db = PlayerData()

    def _command_get(self, person_id):
        # type: (int) -> None
        logging.debug('Getting stats of player %d' % person_id)
        info = nba_py.player.PlayerYearOverYearSplits(player_id=person_id).by_year()
        stats = None
        ss = season_str()
        for season_info in info:
            if season_info.get('GROUP_VALUE','') == ss:
                matches_played = season_info.get('GP', 0)
                if 'PTS' in season_info:
                    points_scored = int(season_info['PTS'] * matches_played) # TODO better source of the info
                else:
                    points_scored = None
                if 'FGA' in season_info:
                    shots = int(season_info['FGA'] * matches_played) # TODO better source of the info
                else:
                    shots = None
                if 'MIN' in season_info:
                    time_played = '%s minutes' % (season_info['MIN'] * matches_played) # TODO better source of the info
                else:
                    time_played = None
                logging.debug('Saving stats of player %d' % person_id)
                self.db.add_player_stats(person_id, SEASON, points_scored, shots, time_played, matches_played)
                logging.debug('Player %d done' % person_id)
                return
        logging.debug('No info found for player %d' % person_id)


class PlayersStatsGrabber:
    def execute(self, rescan_all_players = False):
        data_source = PlayerData()
        threads = []
        # create threads
        for i in range(PLAYERS_STATS_WORKER_COUNT):
            thread_name = 'Thread%d' % i
            thread_queue = Queue()
            thread = PlayersStatsGrabberThread(thread_name, i, thread_queue)
            threads.append((thread, thread_queue))
            thread.start()
        # add data
        db = PlayerData()
        if rescan_all_players:
            players = db.get_active_players(SEASON)
        else:
            players = db.get_players_without_stats(SEASON)
        # splitting players to the workers based on the hash of the person_id (could be done in several other ways)
        for player in players:
            person_id = int(player['person_id'])
            thread_id = person_id % PLAYERS_STATS_WORKER_COUNT # using person_id as hash
            threads[thread_id][1].put(('get', person_id))
        logging.debug('All data queued')
        # inform threads of end of data
        for i in range(PLAYERS_STATS_WORKER_COUNT):
            threads[i][1].put(('stop',None))
        # wait fot threads
        for i in range(PLAYERS_STATS_WORKER_COUNT):
            threads[i][1].join()
