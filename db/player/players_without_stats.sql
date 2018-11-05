CREATE OR REPLACE FUNCTION player.players_without_stats(
    IN  i_season_year       SMALLINT,
    OUT status              INTEGER,
    OUT status_text         TEXT,
    OUT person_id           INTEGER,
    OUT first_name          TEXT,
    OUT last_name           TEXT
) RETURNS SETOF RECORD AS
$$
-------------------------------------------------------------------------------
--
-- Function: player.players_without_stats(1)
--      Return all players that were active the given season and don't have any stats record
--
-- Parameters:
--      i_season_year       - The start year of the season the stats are for
--
-- Returns:
--      status              - Status code
--      status_text         - Status text
--      person_id           - Player's id
--      first_name          - First name of the player
--      last_name           - Last name of the player
--
-- Status codes:
--      200     - OK
--
-------------------------------------------------------------------------------
DECLARE
BEGIN
    RETURN QUERY
    SELECT 200, 'OK'::TEXT, pl.person_id, pl.first_name, pl.last_name
    FROM player.player pl LEFT JOIN
                    player.season_stats ss
                    ON pl.person_id = ss.person_id AND ss.season_year = i_season_year
    WHERE ss.person_id IS NULL AND
        pl.from_year <= i_season_year AND
        coalesce(pl.to_year, i_season_year) >= i_season_year;

    RETURN;
END;
$$
LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
