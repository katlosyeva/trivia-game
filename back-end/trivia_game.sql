/*  
NOTES FOR GROUP 5 team members:

FLOW OF GAME: 

1. ASKS IF NEW PLAYER OR EXISTING AND STARTS GAME?
	- IF NEW: ask player to create a username and ADD TO Players table, and player_id is returned
    - IF EXISTING: player id is returned
    - INSERT player_id to games table
    - POPULATE database with questions (game_id, question_id, question_text, correct_answer, incorrect_answer_1,
          incorrect_answer_2, incorrect_answer_3)

3. RUN GAME():

   - AFTER EACH QUESTION ITERATION IN GAME where player_answer is retrieved:
       - answer of the player is compared with the correct answer from the database
        - AT SAME TIME: if answer is correct score of the player is increased by 1, and his new score is returned
*/

DROP DATABASE IF EXISTS trivia_game;

CREATE DATABASE trivia_game;

use trivia_game;
CREATE TABLE players (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  username varchar(40) NOT NULL
);

CREATE TABLE games (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  user_id int DEFAULT NULL,
  score int DEFAULT NULL,
  FOREIGN KEY (user_id) REFERENCES players (id)
);
CREATE TABLE questions (
  id int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  game_id int,
  question varchar(400),
  correct_answer varchar(200),
  answer_1 varchar(200),
  answer_2 varchar(200),
  answer_3 varchar(200),
  already_displayed boolean,
  FOREIGN KEY (game_id) REFERENCES games (id)
);


INSERT INTO players (username)
VALUES
	('Erika T'),
    ('Hannah M'),
    ('Kate L'),
    ('Helen V'),
    ('Iryna K'),
    ('Inna P');


INSERT INTO games (user_id, score)
VALUES
	(1, 8),
    (2, 10),
    (3, 12),
    (4, 7),
    (5, 13),
    (6, 9);
INSERT INTO questions (
                    game_id,
                    question,
                    correct_answer,
                    answer_1,
                    answer_2,
                    answer_3,
                    already_displayed
                ) VALUES (1,'In which city did American rap producer DJ Khaled originate from?', 'Miami', 'New York', 'Detroit', 'Atlanta', '0')
-- View tables:
SELECT * FROM players;
SELECT * FROM games;
SELECT * FROM questions;

-- Test leaderboard:
SELECT players.username, games.score
FROM players
JOIN games ON players.id = games.user_id
ORDER BY games.score DESC
LIMIT 10
