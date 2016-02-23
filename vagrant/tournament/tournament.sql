-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- cleanUp
DROP TABLE standing;
DROP TABLE outcome;
DROP TABLE game;
DROP TABLE player;
DROP TABLE tournament;

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
first_player_id INTEGER NOT NULL REFERENCES player(player_id),
second_player_id INTEGER NOT NULL REFERENCES player(player_id)
);

-- outcome table
CREATE TABLE outcome(
game_id INTEGER NOT NULL REFERENCES game,
game_draw BOOLEAN NOT NULL DEFAULT FALSE,
winner_player_id INTEGER NOT NULL REFERENCES player(player_id),
loser_player_id INTEGER NOT NULL REFERENCES player(player_id)
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

-- func_update_standing
CREATE OR REPLACE FUNCTION func_update_standing() RETURNS TRIGGER AS $trig_update_standing$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        UPDATE standing
            SET player_win_count = player_win_count + 1
        WHERE player_id = NEW.winner_player_id;
        RETURN NEW;
    END IF;
END;
$trig_update_standing$ LANGUAGE plpgsql;



-- CREATE TRIGGERS
-- trig_insert_standing
CREATE TRIGGER trig_insert_standing
AFTER INSERT ON player
FOR EACH ROW EXECUTE PROCEDURE func_insert_standing();

-- trig_update_standing
CREATE TRIGGER trig_update_standing
AFTER INSERT ON outcome
FOR EACH ROW EXECUTE PROCEDURE func_update_standing();


-- CREATE VIEWS
--CREATE OR REPLACE VIEW vw_