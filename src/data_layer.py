import six
import psycopg2
from psycopg2.extras import RealDictCursor
import logging

from .configuration import DB_CONNECTION

BEST_PLAYERS_CRITERIA_SHOT_EFFICIENCY = 1
BEST_PLAYERS_CRITERIA_PLAY_EFFICIENCY = 2
BEST_PLAYERS_CRITERIA_SCORE_PER_MATCH = 3
BEST_PLAYERS_CRITERIA_RANDOM          = 100


class PlayerData:
    def __init__(self, connection = DB_CONNECTION):
        # type: (dict) -> None
        self._connection = psycopg2.connect(**connection)
        self._connection.autocommit = True
        logging.debug('Autocommit: %s', self._connection.autocommit)

    def add_player(self, person_id, first_name, last_name, player_code, from_year, to_year):
        # type: (int, str, str, str, int, int) -> str
        cur = self._connection.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT status, status_text FROM player.player_entry(%(i_person_id)s, %(i_first_name)s, %(i_last_name)s, %(i_player_code)s, %(i_from_year)s::SMALLINT, %(i_to_year)s::SMALLINT)",
                    {"i_person_id": person_id,
                     "i_first_name": first_name,
                     "i_last_name": last_name,
                     "i_player_code": player_code,
                     "i_from_year": from_year,
                     "i_to_year": to_year})
        rows = cur.fetchall()
        row_count = len(rows)
        if row_count != 1:
            raise Exception('DB interface player.player_entry returned wrong number of results (1 expected): %s' % row_count)
        if rows[0]['status'] == 200:
            result = rows[0]['status_text']
        elif rows[0]['status'] == 201:
            result = rows[0]['status_text']
        else:
            raise Exception('DB interface player.player_entry failed with: [%s] %s' % (rows[0]['status'], rows[0]['status_text']))
        logging.debug(result)
        return result

    def add_player_from_dict(self, player_data):
        # type: (dict) -> str
        names_list = player_data.get('DISPLAY_LAST_COMMA_FIRST', '').split(',',1)
        if len(names_list) == 2:
            last_name, first_name = names_list
        elif len(names_list) == 1:
            first_name = names_list[0]
            last_name = ''
        else:
            first_name = ''
            last_name = ''
        person_id = player_data['PERSON_ID']
        player_code = player_data.get('PLAYERCODE','')
        from_year = player_data.get('FROM_YEAR',1970)
        to_year = player_data.get('TO_YEAR', None)
        return self.add_player(person_id, first_name.strip(), last_name.strip(), player_code, from_year, to_year)

    def add_player_stats(self, person_id, season_year, points_scored = None, shots = None, time_played = None, matches_played = None):
        # type: (int, int, int, int, str, int) -> str
        cur = self._connection.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT status, status_text FROM player.season_stats_entry(%(i_person_id)s, %(i_season_year)s::SMALLINT, %(i_points_scored)s, %(i_shots)s, %(i_time_played)s::INTERVAL, %(i_matches_played)s)",
                    {"i_person_id": person_id,
                     "i_season_year": season_year,
                     "i_points_scored": points_scored,
                     "i_shots": shots,
                     "i_time_played": time_played,
                     "i_matches_played": matches_played})
        rows = cur.fetchall()
        row_count = len(rows)
        if row_count != 1:
            raise Exception('DB interface player.season_stats_entry returned wrong number of results (1 expected): %s' % row_count)
        if rows[0]['status'] == 200:
            result = rows[0]['status_text']
        elif rows[0]['status'] == 201:
            result = rows[0]['status_text']
        else:
            raise Exception('DB interface player.season_stats_entry failed with: [%s] %s' % (rows[0]['status'], rows[0]['status_text']))
        return result

    def get_best_players(self, criteria, season_year, limit = 10):
        # type: (int, int, int) -> list

        # this prevents the redefinition of the "constants" and makes it harder to mess-up the DB call
        criteria_numbers = {
            BEST_PLAYERS_CRITERIA_SHOT_EFFICIENCY: 1,
            BEST_PLAYERS_CRITERIA_PLAY_EFFICIENCY: 2,
            BEST_PLAYERS_CRITERIA_SCORE_PER_MATCH: 3,
            BEST_PLAYERS_CRITERIA_RANDOM: 100,
        }

        cur = self._connection.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT * FROM player.best_players(%(i_player_count)s, %(i_criteria)s::SMALLINT, %(i_season_year)s::SMALLINT)",
                    {"i_player_count": limit,
                     "i_criteria": criteria_numbers[criteria],
                     "i_season_year": season_year})
        return cur.fetchall()

    def get_active_players(self, season_year):
        # type: (int) -> list
        cur = self._connection.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT * FROM player.active_players(%(i_season_year)s::SMALLINT)",
                    {"i_season_year": season_year})
        return cur.fetchall()

    def get_players_without_stats(self, season_year):
        # type: (int) -> list
        cur = self._connection.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT * FROM player.players_without_stats(%(i_season_year)s::SMALLINT)",
                    {"i_season_year": season_year})
        return cur.fetchall()

    def last_names_counts(self, last_names):
        # type: (list) -> dict
        cur = self._connection.cursor(cursor_factory = RealDictCursor)
        cur.execute("SELECT * FROM player.last_names_counts(%(i_last_names)s)",
                    {"i_last_names": last_names})
        result = {}
        for row in cur.fetchall():
            result[row['last_name']] = row['frequency_count']

        return result
