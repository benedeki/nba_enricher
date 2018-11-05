CREATE OR REPLACE FUNCTION player.last_names_counts(
    IN  i_last_names        TEXT[],
    OUT status              INTEGER,
    OUT status_text         TEXT,
    OUT last_name           TEXT,
    OUT frequency_count     INTEGER
) RETURNS SETOF RECORD AS
$$
-------------------------------------------------------------------------------
--
-- Function: player.last_names_counts(1)
--      Returns how many players of given last name are there
--
-- Parameters:
--      i_last_names                - skypename of the user
--
-- Returns:
--      status              - Status code
--      status_text         - Status text
--      last_name           - Name for the input list
--      frequency_count     - Number of times the last name appear in the list
--
-- Status codes:
--      200     - OK
--
-------------------------------------------------------------------------------
DECLARE
BEGIN
    RETURN QUERY
    SELECT 200, 'OK'::TEXT, pp.last_name, count(1)::INTEGER
    FROM player.player pp
    WHERE pp.last_name = ANY(i_last_names)
    GROUP BY pp.last_name;
END;
$$
LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
