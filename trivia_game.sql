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
  username varchar(40)
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
  question varchar(255),
  correct_answer varchar(50),
  answer_1 varchar(200),
  answer_2 varchar(200),
  answer_3 varchar(200),
  is_provided boolean,
  FOREIGN KEY (game_id) REFERENCES games (id)
);