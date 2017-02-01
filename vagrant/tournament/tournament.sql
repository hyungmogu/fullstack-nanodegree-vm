-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.

DROP DATABASE IF EXISTS tournament;

CREATE DATABASE tournament;

\c tournament

CREATE TABLE player (
	id SERIAL PRIMARY KEY,
	name TEXT NOT NULL
);

CREATE TABLE match_result (
	id SERIAL PRIMARY KEY,
	winner_id INT REFERENCES player(id),
	loser_id INT REFERENCES player(id)
); 

-- Count number of wins per player id
CREATE VIEW wins AS
SELECT t.id, COUNT(t.winner_id)
FROM (SELECT p.id AS id, m.winner_id AS winner_id FROM player p LEFT JOIN match_result m ON p.id = m.winner_id) AS t 
GROUP BY t.id; 
-- Count number of losses per player id
CREATE VIEW losses AS
SELECT t.id, COUNT(t.loser_id)
FROM (SELECT p.id AS id, m.loser_id AS loser_id FROM player p LEFT JOIN match_result m ON p.id = m.loser_id) AS t
GROUP BY t.id;
-- Combine wins and losses table
CREATE VIEW player_standings AS
SELECT t.id, t.name, t.wins, t.wins + losses.count AS matches
FROM (SELECT player.id, player.name, wins.count AS wins
FROM player JOIN wins ON player.id = wins.id) AS t
JOIN losses ON t.id = losses.id
ORDER BY t.wins DESC;
