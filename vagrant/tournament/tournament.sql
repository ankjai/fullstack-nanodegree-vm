-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- cleanUp; enable lines below if you want to recreate
-- tables/views
--DROP TABLE standing CASCADE;
--DROP TABLE outcome CASCADE;
--DROP TABLE game CASCADE;
--DROP TABLE player CASCADE;
--DROP TABLE tournament CASCADE;

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
player_win_count INTEGER NOT NULL DEFAULT 0,
player_game_count INTEGER NOT NULL DEFAULT 0
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
            SET player_win_count = player_win_count + 1,
                player_game_count = player_game_count + 1
        WHERE player_id = NEW.winner_player_id;
        UPDATE standing
            SET player_game_count = player_game_count + 1
        WHERE player_id = NEW.loser_player_id;
        RETURN NEW;
    END IF;
END;
$trig_update_standing$ LANGUAGE plpgsql;

-- func_reset_standing
CREATE OR REPLACE FUNCTION func_reset_standing() RETURNS TRIGGER AS $trig_reset_standing$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        UPDATE standing
            SET player_win_count = 0, player_game_count = 0
        WHERE player_id = OLD.first_player_id OR player_id = OLD.second_player_id;
        RETURN NEW;
    END IF;
END;
$trig_reset_standing$ LANGUAGE plpgsql;



-- CREATE TRIGGERS
-- trig_insert_standing
DROP TRIGGER IF EXISTS trig_insert_standing ON player;
CREATE TRIGGER trig_insert_standing
AFTER INSERT ON player
FOR EACH ROW EXECUTE PROCEDURE func_insert_standing();

-- trig_update_standing
DROP TRIGGER IF EXISTS trig_update_standing ON outcome;
CREATE TRIGGER trig_update_standing
AFTER INSERT ON outcome
FOR EACH ROW EXECUTE PROCEDURE func_update_standing();

-- trig_update_standing
DROP TRIGGER IF EXISTS trig_reset_standing ON game;
CREATE TRIGGER trig_reset_standing
AFTER DELETE ON game
FOR EACH ROW EXECUTE PROCEDURE func_reset_standing();


-- CREATE VIEWS
-- vw_player_details
CREATE OR REPLACE VIEW vw_player_details AS
SELECT t.tournament_id, t.tournament_name, p.player_id, p.player_name, s.player_win_count, s.player_game_count
FROM tournament t
JOIN player p ON
t.tournament_id = p.tournament_id
JOIN standing s ON
p.player_id = s.player_id;

-- vw_game_details
-- though view not used in current use cases, can be used if we want to enhance functionality or
-- add additional game related use cases
CREATE OR REPLACE VIEW vw_game_details AS
SELECT t.tournament_id, t.tournament_name, g.game_id, g.first_player_id, g.second_player_id, o.game_draw, o.winner_player_id, o.loser_player_id
FROM tournament t
JOIN game g ON
t.tournament_id = g.tournament_id
JOIN outcome o ON
o.game_id = g.game_id;
