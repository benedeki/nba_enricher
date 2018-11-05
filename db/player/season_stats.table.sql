CREATE TABLE player.season_stats (
    id_season_stats         BIGINT NOT NULL DEFAULT part_conf.global_id(),
    person_id               INTEGER NOT NULL,
    season_year             SMALLINT NOT NULL,
    points_scored           INTEGER,
    shots                   INTEGER,
    time_played             INTERVAL,
    matches_played          INTEGER,
    CONSTRAINT pk_season_stats PRIMARY KEY (id_season_stats)
);

ALTER TABLE player.season_stats OWNER TO nba;

COMMENT ON TABLE player.season_stats IS 'Seasonal stats of players';
COMMENT ON COLUMN player.season_stats.id_season_stats IS 'Surrogate key';
COMMENT ON COLUMN player.season_stats.person_id IS 'Id of the player';
COMMENT ON COLUMN player.season_stats.season_year IS 'The start year of the season the stats are for';
COMMENT ON COLUMN player.season_stats.points_scored IS 'The number of points the player scored during the season';
COMMENT ON COLUMN player.season_stats.shots IS 'The number of shots the player tried to score';
COMMENT ON COLUMN player.season_stats.time_played IS 'Time spent in games during the season';
COMMENT ON COLUMN player.season_stats.matches_played IS 'The number of matches played by the player durign the season';

ALTER TABLE player.season_stats ADD CONSTRAINT unq_season_stats UNIQUE (season_year, person_id);
