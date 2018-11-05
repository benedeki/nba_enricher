CREATE OR REPLACE FUNCTION part_conf.global_id(
  OUT result          BIGINT
) RETURNS BIGINT AS
$$
    SELECT nextval('part_conf.global_id');
$$
LANGUAGE sql VOLATILE SECURITY DEFINER;

