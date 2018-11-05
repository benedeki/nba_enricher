CREATE OR REPLACE FUNCTION player.player_entry(
    IN  i_person_id         INTEGER,
    IN  i_first_name        TEXT,
    IN  i_last_name         TEXT,
    IN  i_player_code       TEXT,
    IN  i_from_year         SMALLINT,
    IN  i_to_year           SMALLINT,
    IN  i_twitter_handle    TEXT DEFAULT NULL,
    OUT status              INTEGER,
    OUT status_text         TEXT
) RETURNS RECORD AS
$$
-------------------------------------------------------------------------------
--
-- Function: player.player_entry(7)
--      Insert or updates player basic info
--
-- Parameters:
--      i_person_id         - Id of the player
--      i_first_name        - First name of the player
--      i_last_name         - Last name of the player
--      i_player_code       - Code of the player
--      i_from_year         - Start of player's career
--      i_to_year           - End of player's career
--      i_twitter_handle    - Player's twitter name; if NULL it will not update the existing info
--
-- Returns:
--      status              - Status code
--      status_text         - Status text
--
-- Status codes:
--      200     - OK, player updated
--      201     - OK, player added
--
-------------------------------------------------------------------------------
DECLARE
    _r      RECORD;
BEGIN
    SELECT pl.*
    FROM player.player pl
    WHERE pl.person_id = i_person_id
    INTO _r;

    IF FOUND THEN
        -- Update
        UPDATE player.player
        SET first_name = i_first_name,
            last_name = i_last_name,
            player_code = i_player_code,
            from_year = least(from_year, i_from_year),
            to_year = least(to_year, i_to_year),
            twitter_handle = coalesce(i_twitter_handle, twitter_handle)
        WHERE person_id = i_person_id;
        status = 200;
        status_text = 'OK, player updated';
    ELSE
        -- Insert
        INSERT INTO player.player (
            person_id, first_name, last_name, player_code,
            from_year, to_year, twitter_handle
        ) VALUES (
            i_person_id, i_first_name, i_last_name, i_player_code,
            i_from_year, i_to_year, i_twitter_handle
        );
        status = 201;
        status_text = 'OK, player added';
    END IF;

    RETURN;
END;
$$
LANGUAGE plpgsql VOLATILE SECURITY DEFINER;
