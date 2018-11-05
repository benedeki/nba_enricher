CREATE OR REPLACE FUNCTION player.season_stats_entry(
    IN  i_person_id         INTEGER,
    IN  i_season_year       SMALLINT,
    IN  i_points_scored     INTEGER DEFAULT NULL,
    IN  i_shots             INTEGER DEFAULT NULL,
    IN  i_time_played       INTERVAL DEFAULT NULL,
    IN  i_matches_played    INTEGER DEFAULT NULL,
    OUT status              INTEGER,
    OUT status_text         TEXT
)
    RETURNS RECORD AS
$$
-------------------------------------------------------------------------------
--
-- Function: player.season_stats_entry([Function_Param_Count])
--      Inserts or updates player's stats for the given season
--
-- Parameters:
--      i_person_id         - Player's id
--      i_season_year       - The start year of the season the stats are for
--      i_points_scored     - The number of points the player scored during the season
--      i_shots             - The number of shots the player tried to score
--      i_time_played       - Time spent in games during the season
--      i_matches_played    - The number of matches played by the player durign the season
--
-- Returns:
--      status              - Status code
--      status_text         - Status text
--
-- Status codes:
--      200     - OK, stats updated
--      201     - OK, stats created
--      404     - No such player
--
-------------------------------------------------------------------------------
DECLARE
BEGIN
    PERFORM 1
    FROM player.season_stats ss
    WHERE ss.person_id = i_person_id AND
        ss.season_year = i_season_year
    FOR UPDATE;

    IF FOUND THEN
        UPDATE player.season_stats
        SET points_scored = coalesce(i_points_scored, points_scored),
            shots = coalesce(i_shots, shots),
            time_played = coalesce(i_time_played, time_played),
            matches_played = coalesce(i_matches_played, matches_played)
        WHERE person_id = i_person_id AND
              season_year = i_season_year;
        status := 200;
        status_text := 'OK, stats updated';
    ELSE
        PERFORM 1
        FROM player.player pl
        WHERE pl.person_id = i_person_id;

        IF found THEN
            INSERT INTO player.season_stats (
                person_id, season_year, points_scored, shots,
                time_played, matches_played
            ) VALUES (
                i_person_id, i_season_year,i_points_scored, i_shots,
                i_time_played, i_matches_played
            );
            status := 201;
            status_text := 'OK, stats created';
        ELSE
            status = 404;
            status_text := 'No such player';
        END IF;
    END IF;

    RETURN;
END;
$$
LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
