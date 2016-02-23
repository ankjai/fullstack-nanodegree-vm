-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- cleanUp
--DROP TABLE standing;
--DROP TABLE game;
--DROP TABLE player;
--DROP TABLE tournament;

-- CREATE TABLES
-- tournament table
CREATE TABLE tournament(
tournament_id SERIAL PRIMARY KEY,
tournament_name TEXT
);

-- player table
CREATE TABLE player(
player_id SERIAL PRIMARY KEY,
tournament_id INTEGER NOT NULL REFERENCES tournament,
player_name TEXT
);

-- game table
CREATE TABLE game(
game_id SERIAL PRIMARY KEY,
tournament_id INTEGER NOT NULL REFERENCES tournament,
first_player_id INTEGER NOT NULL REFERENCES tournament(tournament_id),
second_player_id INTEGER NOT NULL REFERENCES tournament(tournament_id)
);

-- standing table
CREATE TABLE standing(
player_id INTEGER NOT NULL REFERENCES player ON DELETE CASCADE,
player_win_count INTEGER NOT NULL DEFAULT 0
);


-- CREATE FUNCTIONS
-- func_insert_standing
CREATE OR REPLACE FUNCTION func_insert_standing() RETURNS TRIGGER AS $trig_insert_standing$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO standing(player_id) VALUES(NEW.player_id);
        RETURN NEW;
    END IF;
END;
$trig_insert_standing$ LANGUAGE plpgsql;


-- CREATE TRIGGERS
-- trig_insert_standing
CREATE TRIGGER trig_insert_standing
AFTER INSERT ON player
FOR EACH ROW EXECUTE PROCEDURE func_insert_standing();