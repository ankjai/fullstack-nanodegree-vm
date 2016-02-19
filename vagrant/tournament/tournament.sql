-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

-- cleanUp
DROP TABLE game;
DROP TABLE player;
DROP TABLE tournament;

-- tournament table
CREATE TABLE tournament(
tournament_id INTEGER PRIMARY KEY,
tournament_name TEXT
);

-- player table
CREATE TABLE player(
player_id INTEGER PRIMARY KEY,
tournament_id INTEGER REFERENCES tournament,
player_name TEXT
);

-- game table
CREATE TABLE game(
game_id INTEGER PRIMARY KEY,
tournament_id INTEGER REFERENCES tournament,
first_player_id INTEGER REFERENCES tournament(tournament_id),
second_player_id INTEGER REFERENCES tournament(tournament_id)
);