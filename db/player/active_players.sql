CREATE OR REPLACE FUNCTION player.active_players(
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
-- Function: player.active_players(1)
--      Return all players active in the given year
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
    FROM player.player pl
    WHERE pl.from_year <= i_season_year AND
        coalesce(pl.to_year, i_season_year) >= i_season_year;

    RETURN;
END;
$$
LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
