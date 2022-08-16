-- DROP SCHEMA public;

-- CREATE SCHEMA public AUTHORIZATION postgres;

\connect golf_db

-- drop sequence public.golfer_id_seq;

CREATE SEQUENCE public.golfer_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 900000
	START 100000
	CACHE 100
	NO CYCLE;-- public.alembic_version definition

GRANT USAGE, SELECT ON SEQUENCE public.golfer_id_seq TO golf;