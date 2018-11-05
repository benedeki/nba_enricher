CREATE OR REPLACE FUNCTION player.best_players(
    IN  i_player_count      INTEGER,
    IN  i_criteria          SMALLINT,
    IN  i_season_year       SMALLINT,
    OUT status              INTEGER,
    OUT status_text         TEXT,
    OUT person_id           INTEGER,
    OUT first_name          TEXT,
    OUT last_name           TEXT,
    OUT player_code         TEXT,
    OUT twitter_handle      TEXT,
    OUT points_scored       INTEGER
) RETURNS SETOF RECORD AS
$$
-------------------------------------------------------------------------------
--
-- Function: player.best_players(3)
--      Returns a set of best players of the seasons judged by the given criteria
--
-- Parameters:
--      i_player_count      - Limit on the number of players returned
--      i_criteria          - Index of the criteria used to compare the players
--            1....shot efficiency (points scored/shots executed)
--            2....time in play efficiency (points scored/time in game)
--            3....average match score (points scored/matches played)
--            100..random order
--      i_season_year       - The start year of the season the stats are for
--
-- Returns:
--      status              - Status code
--      status_text         - Status text
--      person_id           - Player's id
--      first_name          - First name of the player
--      last_name           - Last name of the player
--      player_code         - Code of the player
--      twitter_handle      - Player's twitter name; if NULL it will not update the existing info
--
-- Status codes:
--      200     - OK
--      500     - Player counts has to be positive number
--      501     - Invalid criteria
--
-------------------------------------------------------------------------------
DECLARE
BEGIN
    IF i_player_count <= 0 THEN
        status := 500;
        status_text = 'Player counts has to be positive number';
        RETURN NEXT;
        RETURN;
    END IF;

    status := 200;
    status_text := 'OK';
    IF i_criteria = 1 THEN
        RETURN QUERY
        SELECT 200, 'OK'::TEXT, pl.person_id, pl.first_name,
            pl.last_name, pl.player_code, pl.twitter_handle, ss.points_scored
        FROM player.player pl INNER JOIN
            player.season_stats ss ON pl.person_id = ss.person_id AND ss.season_year = i_season_year
        ORDER BY
            ss.points_scored / nullif(ss.shots, 0)
        LIMIT i_player_count;
    ELSEIF i_criteria = 2 THEN
        RETURN QUERY
        SELECT 200, 'OK'::TEXT, pl.person_id, pl.first_name,
            pl.last_name, pl.player_code, pl.twitter_handle, ss.points_scored
        FROM player.player pl INNER JOIN
                 player.season_stats ss ON pl.person_id = ss.person_id AND ss.season_year = i_season_year
        ORDER BY
                 ss.points_scored / nullif(EXTRACT(EPOCH FROM ss.time_played), 0)
        LIMIT i_player_count;
    ELSEIF i_criteria = 3 THEN
        RETURN QUERY
        SELECT 200, 'OK'::TEXT, pl.person_id, pl.first_name,
            pl.last_name, pl.player_code, pl.twitter_handle, ss.points_scored
        FROM player.player pl INNER JOIN
                 player.season_stats ss ON pl.person_id = ss.person_id AND ss.season_year = i_season_year
        ORDER BY
                 ss.points_scored / nullif(ss.matches_played, 0)
        LIMIT i_player_count;
    ELSEIF i_criteria = 100 THEN
        RETURN QUERY
        SELECT 200, 'OK'::TEXT, x.person_id, x.first_name,
               x.last_name, x.player_code, x.twitter_handle, x.points_scored
        FROM (
            SELECT 200, 'OK'::TEXT, pl.person_id, pl.first_name,
                   pl.last_name, pl.player_code, pl.twitter_handle, ss.points_scored,
                   random() as random
            FROM player.player pl LEFT JOIN
                     player.season_stats ss ON pl.person_id = ss.person_id AND ss.season_year = i_season_year
            ) x
        ORDER BY
                 x.random
        LIMIT i_player_count;
    ELSE
        status := 501;
        status_text = 'Invalid criteria';
        RETURN NEXT;
        RETURN;
    END IF;
END;
$$
LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
