CREATE SCHEMA part_conf;
GRANT USAGE ON SCHEMA part_conf TO public;

CREATE SEQUENCE IF NOT EXISTS part_conf.global_id START WITH 281474976710656 NO CYCLE;
COMMENT ON SEQUENCE part_conf.global_id IS 'Unique sequence over multiple servers where the top 16-bits define the server id';