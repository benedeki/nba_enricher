CREATE TABLE player.player (
    person_id       INTEGER NOT NULL,
    first_name      TEXT NOT NULL,
    last_name       TEXT NOT NULL,
    player_code     TEXT NOT NULL,
    twitter_handle  TEXT,
    from_year       SMALLINT,
    to_year         SMALLINT,
    CONSTRAINT pk_player PRIMARY KEY (person_id)
);

ALTER TABLE player.player OWNER TO nba;

COMMENT ON TABLE player.player IS 'List of players';
COMMENT ON COLUMN player.player.person_id IS 'Id of the player';
COMMENT ON COLUMN player.player.first_name IS 'First name of the player';
COMMENT ON COLUMN player.player.last_name IS 'Last name of the player';
COMMENT ON COLUMN player.player.player_code IS 'Code of the player';
COMMENT ON COLUMN player.player.twitter_handle IS 'Player''s twitter name';
COMMENT ON COLUMN player.player.from_year IS 'Start of player''s career';
COMMENT ON COLUMN player.player.to_year IS 'End of player''s career';

ALTER TABLE player.player ADD CONSTRAINT unq_player_player_code UNIQUE (player_code);
ALTER TABLE player.player ADD CONSTRAINT chck_player_year CHECK (from_year <= to_year OR to_year IS NULL);

CREATE INDEX idx_player_years ON player.player (from_year, to_year);